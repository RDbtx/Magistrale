#include <stdio.h>
#include <stdlib.h>
#include "platform.h"
#include "xil_printf.h"
#include "xuartps.h"
#include <xtime_l.h>
#include "shared.h"
#include <time.h>
#include "saturate.h"
#include <math.h>

#define n_bias0 64
#define n_weights0 50176
#define n_bias1 32
#define n_weights1 2048
#define n_bias2 10
#define n_weights2 320

// -------------------------------------------------------------------------------------------------

#define FIXED2FLOAT(a, qf) (((float) (a)) / (1 << qf))
#define FLOAT2FIXED(a, qf) ((int8_t) round((a) * (1 << qf)))

// -------------------------------------------------------------------------------------------------

/* ------------------------------------------------------------ */
/*						Legacy Definitions					    */
/* ------------------------------------------------------------ */

static inline void relu_forward(DATA *input, DATA *output, int size);

// -------------------------------------------------------------------------------------------------

/* ------------------------------------------------------------ */
/*						New Optimized Utilities				    */
/* ------------------------------------------------------------ */

#define GEMM0_WLEN 50176
#define GEMM1_WLEN 2048
#define GEMM2_WLEN 512
#define GEMM3_WLEN 160

#define GEMM0_BLEN 64
#define GEMM1_BLEN 32
#define GEMM2_BLEN 16
#define GEMM3_BLEN 10

#define LAYERS 4

u32 compute_execution_cycles(u32 start, u32 end) {
    /*
     * Computes the number of execution cycles elapsed between two timer readings.
     *
     * Inputs:
     * - start: timer value captured at the beginning of the measured section.
     * - end: timer value captured at the end of the measured section.
     *
     * Outputs:
     * - Returns the number of elapsed cycles between start and end.
     */
    return (u32)(end - start);
}

DATA *receive_biases(int bias_array_len) {
    /*
     * Receives the bias vector from UART and stores it in dynamically allocated memory.
     * Each bias value is received as an 8-bit signed value (Q1.7 format).
     * The function also measures and reports the reception time in clock cycles.
     *
     * Inputs:
     * - bias_array_len: number of bias elements to receive.
     *
     * Outputs:
     * - *bias: a pointer to the allocated bias array.
     */
    u32 start, end;
    DATA *biases = (DATA *) malloc(bias_array_len * sizeof(DATA));

    start = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    for (int i = 0; i < bias_array_len; i++) {
        biases[i] = (DATA) inbyte();
    }
    end = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    u32 cycles = compute_execution_cycles(start, end);
    xil_printf("Biases loaded! = [%lu] cycles\r\n", cycles);
    return biases;
}

DATA *receive_weights(int weights_array_len) {
    /*
     * Receives the weight matrix from UART and stores it in dynamically allocated memory.
     * Each weight value is received as an 8-bit signed value (Q1.7 format).
     * The function also measures and reports the reception time in clock cycles.
     *
     * Inputs:
     * - weights_array_len: total number of weight elements to receive.
     *
     * Outputs:
     * - *weights: a pointer to the allocated weight array.
     */
    u32 start, end;
    DATA *weights = (DATA *) malloc(weights_array_len * sizeof(DATA));

    start = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    for (int i = 0; i < weights_array_len; i++) {
        weights[i] = (DATA) inbyte();
    }
    end = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    u32 cycles = compute_execution_cycles(start, end);
    xil_printf("Weights loaded! = [%lu] cycles\r\n", cycles);
    return weights;
}

DATA *receive_optimized_image(int image_width, int image_height) {
    /*
     * Receives an optimized image from UART.
     * The image is transmitted using 8-bit unsigned values (Q0.8 format),
     * reducing memory footprint and transmission bandwidth.
     *
     * Inputs:
     * - image_width:  width of the image in pixels.
     * - image_height: height of the image in pixels.
     *
     * Outputs:
     * - image: a pointer to the allocated image buffer.
     *
     */
    u32 start, end;
    int imglen = image_width * image_height;
    DATA *image = (DATA *) malloc(imglen * sizeof(DATA));

    start = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    for (int i = 0; i < imglen; i++) {
        uint8_t pixel = (uint8_t) inbyte();
        image[i] = (DATA) pixel; //image data is received in Q0.8 format
    }
    end = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    u32 cycles = compute_execution_cycles(start, end);
    xil_printf("Receiving Image = [%lu] cycles\r\n", cycles);

    return image;
}

void parallel_FC_forward(DATA *input, DATA *output, int in_s, int out_s, DATA *weights, DATA *bias, int qf) {
    /*
     * Executes a FC layer forward pass using two-core parallelism.
     * The master writes pointers and layer parameters into shared memory, launches
     * the worker, computes its half of the outputs, then waits for the
     * worker to compute the remaining half before completing. The results are
     * then stored inside the output structure passed as an input parameter.
     *
     * Inputs:
     * - input:   pointer to the input activation vector (length = in_s).
     * - output:  pointer to the output activation vector (length = out_s).
     * - in_s:    number of input features.
     * - out_s:   number of output neurons.
     * - weights: pointer to the weight matrix
     * - bias:    pointer to the bias vector
     * - qf:      number of fractional bits.
     *
     */
    u32 timer_start, timer_end;
    int start = 0;
    int end = out_s / 2;

    // Shared memory setup
    SHARED->input = input;
    SHARED->output = output;
    SHARED->weights = weights;
    SHARED->bias = bias;

    SHARED->in_s = in_s;
    SHARED->out_s = out_s;
    SHARED->qf = qf;

    SHARED->done0 = 0; // master not done
    SHARED->done1 = 0; // worker not done
    SHARED->start = 1; // worker can start


    // Master will compute the first half
    timer_start = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    for (int hkern = start; hkern < end; hkern++) {
        int32_t mac = ((int32_t) SHARED->bias[hkern]) << qf;
        for (int wkern = 0; wkern < in_s; wkern++) {
            mac += (int32_t) SHARED->input[wkern] * (int32_t) SHARED->weights[hkern * in_s + wkern];
        }
        SHARED->output[hkern] = (DATA) saturate(mac >> qf);
    }
    // Wait for worker
    while (SHARED->done1 == 0) {
        /* busy-wait */
    }


    // Reset start flag for next layer
    SHARED->start = 0;


    // wait worker acknowledge
    while (SHARED->done1 == 1) {
        /* busy-wait */
    }

    timer_end = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    u32 cycles = compute_execution_cycles(timer_start, timer_end);
    xil_printf("Forwarding, dim [%d x %d] = [%lu] cycles\r\n", in_s, out_s, cycles);
}

void free_support_data(DATA *weights[], DATA *biases[]) {
    /*
     * Frees dynamically allocated weights and biases buffers for all layers.
     *
     * Inputs:
     * - weights: array of pointers to weights buffers.
     * - biases:  array of pointers to biases buffers.
     */
    for (int i = 0; i < LAYERS; i++) {
        if (weights[i] != NULL) {
            free(weights[i]);
            weights[i] = NULL;
        }
        if (biases[i] != NULL) {
            free(biases[i]);
            biases[i] = NULL;
        }
    }
}

// -------------------------------------------------------------------------------------------------

/* ------------------------------------------------------------ */
/*		 Optimized Main for 8 bit files (Q1.7 format)           */
/* ------------------------------------------------------------ */

int main() {
    init_platform();

    Xil_ICacheDisable();
    Xil_DCacheDisable();

    SHARED->start = 0;
    SHARED->done0 = 0;
    SHARED->done1 = 0;

    //UART setup
    XUartPs Uart_1_PS;
    u16 DeviceId_1 = XPAR_PS7_UART_1_DEVICE_ID;
    int Status_1;
    XUartPs_Config *Config_1;
    Config_1 = XUartPs_LookupConfig(DeviceId_1);
    if (NULL == Config_1) {
        return XST_FAILURE;
    }
    /*the default configuration is stored in Config and it can be used to initialize the controller */
    Status_1 = XUartPs_CfgInitialize(&Uart_1_PS, Config_1, Config_1->BaseAddress);
    if (Status_1 != XST_SUCCESS) {
        return XST_FAILURE;
    }
    // Set the BAUD rate
    u32 BaudRate = (u32) 115200;
    Status_1 = XUartPs_SetBaudRate(&Uart_1_PS, BaudRate);
    if (Status_1 != (s32) XST_SUCCESS) {
        return XST_FAILURE;
    }


    u32 start, end;

    DATA *weights[LAYERS];
    DATA *biases[LAYERS];

    const int wlen[LAYERS] = {GEMM0_WLEN,GEMM1_WLEN,GEMM2_WLEN,GEMM3_WLEN};
    const int blen[LAYERS] = {GEMM0_BLEN,GEMM1_BLEN,GEMM2_BLEN,GEMM3_BLEN};

    DATA out_gemm0[GEMM0_BLEN];
    DATA in_gemm1[GEMM0_BLEN];
    DATA out_gemm1[GEMM1_BLEN];
    DATA in_gemm2[GEMM1_BLEN];
    DATA out_gemm2[GEMM2_BLEN];
    DATA in_gemm3[GEMM2_BLEN];
    DATA out_gemm3[GEMM3_BLEN];

    xil_printf("\r\nWaiting for biases and weights...\r\n");

    for (int i = 0; i < LAYERS; i++) {
        xil_printf("Upload Gemm%d weights:\r\n", i);
        weights[i] = receive_weights(wlen[i]);
        xil_printf("Upload Gemm%d biases:\r\n", i);
        biases[i] = receive_biases(blen[i]);
    }

    while (1) {
        xil_printf("\r\nWaiting for the image...\r\n");
        start = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
        DATA *image = receive_optimized_image(28, 28);


        parallel_FC_forward(image, out_gemm0, 784, 64, weights[0], biases[0], 8);
        relu_forward(out_gemm0, in_gemm1, 64);
        parallel_FC_forward(in_gemm1, out_gemm1, 64, 32, weights[1], biases[1], 8);
        relu_forward(out_gemm1, in_gemm2, 32);
        parallel_FC_forward(in_gemm2, out_gemm2, 32, 16, weights[2], biases[2], 8);
        relu_forward(out_gemm2, in_gemm3, 16);
        parallel_FC_forward(in_gemm3, out_gemm3, 16, 10, weights[3], biases[3], 8);
        resultsProcessing(out_gemm3, 10);

        end = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
        u32 cycles = compute_execution_cycles(start, end);
        xil_printf("Total cycles = [%lu] cycles\r\n", cycles);
        free(image);
    }
    free_support_data(weights, biases);
    cleanup_platform();
    return 0;
}

// -------------------------------------------------------------------------------------------------

/* ------------------------------------------------------------ */
/*						Legacy NN Functions					    */
/* ------------------------------------------------------------ */

static inline void relu_forward(DATA *input, DATA *output, int size) {
    u32 start, end;
    int i = 0;
    start = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    for (i = 0; i < size; i++) {
        DATA v = input[i];
        v = v > 0 ? v : 0;
        output[i] = v;
    }
    end = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    u32 cycles = compute_execution_cycles(start, end);
    xil_printf("Relu, dim [%d] = [%lu] cycles\r\n", size, cycles);
}

#define SIZEWA 10

int resultsProcessing(DATA *results, int size) {
	// only argmax.
    int top0 = 0;
    int8_t max_val = results[0];

    xil_printf("Scores: 0=%d, 1=%d, 2=%d, 3=%d, 4=%d, 5=%d, 6=%d, 7=%d, 8=%d, 9=%d\r\n",
               results[0], results[1], results[2], results[3], results[4],
               results[5], results[6], results[7], results[8], results[9]);
    for (int i = 1; i < size; i++) {
        if (results[i] > max_val) {
            max_val = results[i];
            top0 = i;
        }
    }

    xil_printf("OUTPUT= %d (Score: %d)\r\n", top0, max_val);
    return top0;
}
