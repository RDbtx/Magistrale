#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xuartps.h"
#include <math.h>


// -------------------------------------------------------------------------------------------------

/* ------------------------------------------------------------ */
/*		                    Image Management                    */
/* ------------------------------------------------------------ */

int is_a_num(unsigned char element) {
    /*
     * This function controls whether the incoming byte
     * is a number comprised between 0 and 9, a space or a /n.
     * It is used to parse the header element in order to
     * process images with different dimensions.
     *
     * Input:
     * - element: the currently parsed header byte.
     *
     * Outputs:
     * - "element - '0'": if the element is a number, the function returns its integer value.
     * - "-2": if the element is a space or a newline, the program returns -2.
     * - "-1": if the element is none of the aforementioned Ascii character, the program returns -1.
     *
     */

    if (element >= '0' && element <= '9')
        return element - '0';
    if (element == ' ' || element == '\n')
        return -2;
    return -1;
}

unsigned char *compute_dimensions(int *width, int *height, int *header_len) {
    /*
     * This function is used to parse the PPM image header It extracts the image
     * dimensions  and the full header content.
     *
     * Inputs:
     * - width: pointer to an integer where the computed image width will be stored.
     * - height: pointer to an integer where the computed image height will be stored.
     * - header_len: pointer to an integer that will store the length of the header.
     *
     * Outputs:
     * - header: a pointer to the array where the header is stored.
     *
     */
    unsigned char byte;
    int reading_width = 1;
    int done_reading_dims = 0;
    int val;

    *width = 0;
    *height = 0;
    *header_len = 0;

    unsigned char *header = (unsigned char *) malloc(32);

    // Skip the first three bytes since they are P6\n.
    for (int i = 0; i < 3; i++) {
        byte = XUartPs_RecvByte(XPAR_PS7_UART_1_BASEADDR);
        header[*header_len] = byte;
        (*header_len)++;
    }

    while (1) {
        byte = XUartPs_RecvByte(XPAR_PS7_UART_1_BASEADDR);
        header[*header_len] = byte;
        (*header_len)++;
        val = is_a_num(byte);

        // width and height parsing
        if (!done_reading_dims) {
            if (val >= 0) {
                if (reading_width)
                    *width = (*width * 10) + val;
                else
                    *height = (*height * 10) + val;
            } else if (val == -2) {
                if (reading_width)
                    reading_width = 0;
                else
                    done_reading_dims = 1;
            }
        } else {
            // final values parsing.
            if (done_reading_dims && byte == '\n')
                break;
        }
    }
    return header;
}


unsigned char *receive_image(int *width, int *height, unsigned char **header, int *header_len) {
    /*
     * This function receives the entire image content.
     * It first calls compute_dimensions() to read and parse the header,
     * obtaining the image width, height, and header length. It then allocates
     * enough memory to store the image pixels and receives them through a for loop.
     *
     * Inputs:
     * - width: pointer to an integer where the image width will be stored.
     * - height: pointer to an integer where the image height will be stored.
     * - header: pointer to a pointer where the header buffer will be stored.
     * - header_len: pointer to an integer where the header length will be stored.
     *
     * Outputs:
     * - image: a pointer to the dynamically allocated image buffer.
     *
     */

    *header = compute_dimensions(width, height, header_len);
    int img_size = (*width) * (*height) * 3;
    unsigned char *image = (unsigned char *) malloc(img_size);
    for (int i = 0; i < img_size; i++) {
        image[i] = XUartPs_RecvByte(XPAR_PS7_UART_1_BASEADDR);
    }

    return image;
}


void send_image(unsigned char *image, unsigned char *header, int headerlen, int width, int height) {
    /*
     * The send_image function is used to send the processed image content
     * to the XUart board. It firstly sends the header then the image
     * through two for loops.
     *
     * Inputs:
     * - image: a pointer to the image array.
     * - header: a pointer to the header array.
     * - headerlen: the length of the header.
     * - width: the width of the image.
     * - height: the height of the image.
     *
     */

    for (int i = 0; i < headerlen; i++)
        XUartPs_SendByte(XPAR_PS7_UART_1_BASEADDR, header[i]);

    for (int i = 0; i < 3 * width * height; i++)
        XUartPs_SendByte(XPAR_PS7_UART_1_BASEADDR, image[i]);
}

void negate(unsigned char *image, int width, int height) {
    /*
     * This function is used to generate the negative of the image
     * by inverting all its pixel intensity values.
     *
     * Inputs:
     * - image: a pointer to the image array.
     * - width: the width of the image.
     * - height: the height of the image.
     *
     */
    int img_end = 3 * width * height;

    for (int i = 0; i < img_end; i++)
        image[i] = 255 - image[i];
}

void line_stretch(unsigned char *image, int width, int height) {
    /*
     * This function performs linear contrast stretching on the image.
     * It scales pixel values between the I_min and I_max
     * intensity levels.
     *
     * Inputs:
     * - image: pointer to the image array.
     * - width: image width.
     * - height: image height.
     *
     */
    int img_end = 3 * width * height;


    unsigned char I_max = image[0];
    unsigned char I_min = image[0];


    for (int i = 0; i < img_end; i++) {
        if (image[i] > I_max) I_max = image[i];
        if (image[i] < I_min) I_min = image[i];
    }


    float scale;
    int diff = I_max - I_min;
    if ((diff) == 0) scale = 255;
    else scale = 255.0f / (float) diff;

    for (int i = 0; i < img_end; i++) {
        unsigned char lin_stretched_elem = (unsigned char) round(((double) image[i] - (double) I_min) * (double) scale);
        image[i] = lin_stretched_elem;
    }
}


void equalize_hist(unsigned char *image, int width, int height) {
    /*
     * This function is used perform histogram_equalization of the
     * image.
     *
     * Inputs:
     * - image: a pointer to the image array.
     * - width: the width of the image.
     * - height: the height of the image.
     *
     */
    unsigned int hist[256];
    unsigned int cdf[256];
    unsigned char map[256];
    int total_channel_pixels = width * height;

    // equalizes separately all the channels
    for (int channel = 0; channel < 3; channel++) {
        for (int i = 0; i < 256; i++)
            hist[i] = 0;

        for (int i = 0; i < total_channel_pixels; i++)
            hist[image[3 * i + channel]]++;

        cdf[0] = hist[0];
        for (int i = 1; i < 256; i++)
            cdf[i] = cdf[i - 1] + hist[i];

        unsigned int cdf_min = 0;
        for (int i = 0; i < 256; i++) {
            if (cdf[i] != 0) {
                cdf_min = cdf[i];
                break;
            }
        }

        for (int i = 0; i < 256; i++) {
            unsigned int num = (cdf[i] - cdf_min) * 255;
            unsigned int den = total_channel_pixels - cdf_min;

            if (den == 0) den = 1;

            map[i] = (unsigned char) round((double) num / (double) (den));
        }

        for (int i = 0; i < total_channel_pixels; i++)
            image[3 * i + channel] = map[image[3 * i + channel]];
    }
}


void free_image(unsigned char *image) {
    /*
     * The free_image function unallocates the memory that is currently allocated
     * to store the image bytes.
     *
     * Inputs:
     * -image = pointer to the array where the image is stored.
     *
     */
    free(image);
}

void free_header(unsigned char *header) {
    /*
     * The free_header function unallocates the memory that is currently allocated
     * to store the image's header bytes.
     *
     * Inputs:
     * -header = pointer to the array where the image 's header is stored.
     *
     */
    free(header);
}


// -------------------------------------------------------------------------------------------------

/* ------------------------------------------------------------ */
/*		                    Main                                */
/* ------------------------------------------------------------ */


int main() {
    init_platform();
    XUartPs Uart_1_PS;
    u16 DeviceId_1 = XPAR_PS7_UART_1_DEVICE_ID;
    int Status_1;
    XUartPs_Config *Config_1;
    Config_1 = XUartPs_LookupConfig(DeviceId_1);
    if (NULL == Config_1) {
        return XST_FAILURE;
    }
    Status_1 = XUartPs_CfgInitialize(&Uart_1_PS, Config_1, Config_1->BaseAddress);
    if (Status_1 != XST_SUCCESS) {
        return XST_FAILURE;
    }
    u32 BaudRate = (u32) 115200;
    Status_1 = XUartPs_SetBaudRate(&Uart_1_PS, BaudRate);
    if (Status_1 != (s32) XST_SUCCESS) {
        return XST_FAILURE;
    }

    int width, height, header_len;
    unsigned char *header;
    unsigned char *image = receive_image(&width, &height, &header, &header_len);

    //decomment one of these functions in order to use it

    //negate(image, width, height);
    //line_stretch(image, width, height);
    //equalize_hist(image, width, height);


    send_image(image, header, header_len, width, height);

    free_image(image);
    free_header(header);

    cleanup_platform();
    return 0;
}
