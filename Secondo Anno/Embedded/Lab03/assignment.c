/******************************************************************************
*
* Copyright (C) 2009 - 2014 Xilinx, Inc.  All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* Use of the Software is limited solely to applications:
* (a) running on a Xilinx device, or
* (b) that interact with a Xilinx device through a bus or interconnect.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
* Except as contained in this notice, the name of the Xilinx shall not be used
* in advertising or otherwise to promote the sale, use or other dealings in
* this Software without prior written authorization from Xilinx.
*
******************************************************************************/

/*
 * helloworld.c: simple test application
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */

#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xil_io.h"
#include "xiicps.h"
#include "timer_ps.h"
#include <stdlib.h>
#include <math.h>
/* I2S Register offsets */
#define I2S_RESET_REG 		0x00
#define I2S_CTRL_REG 		0x04
#define I2S_CLK_CTRL_REG 	0x08
#define I2S_FIFO_STS_REG 	0x20
#define I2S_RX_FIFO_REG 	0x28
#define I2S_TX_FIFO_REG 	0x2C

#define FIFO_ISR ( 0x00)
#define FIFO_IER ( 0x04)
#define FIFO_TDFV ( 0x0C)
#define FIFO_RDFO ( 0x1C)
#define FIFO_TDR ( 0x2C)
#define FIFO_TDFD ( 0x10)
#define FIFO_TLR ( 0x14)


#define FIFO_RLR ( 0x24)
#define FIFO_RDFD ( 0x20)
#define FIFO_RDR ( 0x30)

/* IIC address of the SSM2603 device and the desired IIC clock speed */
#define IIC_SLAVE_ADDR		0b0011010
#define IIC_SCLK_RATE		100000


#define AUDIO_IIC_ID XPAR_XIICPS_0_DEVICE_ID
#define AUDIO_CTRL_BASEADDR XPAR_AXI_I2S_ADI_0_S00_AXI_BASEADDR
#define SCU_TIMER_ID XPAR_SCUTIMER_DEVICE_ID


#define SWI_BASE_ADDR XPAR_AXI_GPIO_2_BASEADDR
#define LED_BASE_ADDR XPAR_AXI_GPIO_1_BASEADDR
#define BUT_BASE_ADDR XPAR_AXI_GPIO_0_BASEADDR

#define AUDIO_FIFO XPAR_AXI_FIFO_MM_S_0_BASEADDR

#define FIR_FIFO XPAR_AXI_FIFO_MM_S_1_BASEADDR

#define GLOBAL_TMR_BASEADDR XPAR_PS7_GLOBALTIMER_0_S_AXI_BASEADDR

/* ------------------------------------------------------------ */
/*	       Low-Pass and High-Pass filter coefficients        	*/
/* ------------------------------------------------------------ */

#define coeffLP -0.008747420411798365, -0.01352684070757768, -0.021069157456114974, -0.02821205662046602, -0.03288466862750655, -0.032820056352546804, -0.026015856418133178, -0.011326253746998683, 0.01118086152569252, 0.039926269347420495, 0.07195575020178693, 0.10331516426959793, 0.12972205191226951, 0.14735052987683003, 0.15353880775461448, 0.14735052987683003, 0.12972205191226951, 0.10331516426959793, 0.07195575020178693, 0.039926269347420495, 0.01118086152569252, -0.011326253746998683, -0.026015856418133178, -0.032820056352546804, -0.03288466862750655, -0.02821205662046602, -0.021069157456114974, -0.01352684070757768, -0.008747420411798365
#define N_LP 29
#define coeffHP   0.05946436587252379,   -0.08266255914551396,  -0.032374303236116855,   0.00216595808715192,   0.02865430955587078,   0.045067235048989344,   0.04435253660179216,   0.02016730464237364,   -0.027703198625664668,   -0.0913071374380985, -0.15595705304807897, -0.2038996657538856,   0.7782265468798992,   -0.2038996657538856,   -0.15595705304807897,   -0.0913071374380985,   -0.027703198625664668,   0.02016730464237364,   0.04435253660179216,   0.045067235048989344,   0.02865430955587078,   0.00216595808715192,   -0.032374303236116855,   -0.08266255914551396,   0.05946436587252379
#define N_HP 25

#define inputTest_250 0, 33, 65, 98, 131, 163, 195, 227, 259, 290, 321, 352, 383, 413, 442, 471, 500, 528, 556, 582, 609, 634, 659, 684, 707, 730, 752, 773, 793, 813, 831, 849, 866, 882, 897, 911, 924, 936, 947, 957, 966, 974, 981, 987, 991, 995, 998, 999, 1000, 999, 998, 995, 991, 987, 981, 974, 966, 957, 947, 936, 924, 911, 897, 882, 866, 849, 831, 813, 793, 773, 752, 730, 707, 684, 659, 634, 609, 582, 556, 528, 500, 471, 442, 413, 383, 352, 321, 290, 259, 227, 195, 163, 131, 98, 65, 33, 0, -33, -65, -98, -131, -163, -195, -227, -259, -290, -321, -352, -383, -413, -442, -471, -500, -528, -556, -582, -609, -634, -659, -684, -707, -730, -752, -773, -793, -813, -831, -849, -866, -882, -897, -911, -924, -936, -947, -957, -966, -974, -981, -987, -991, -995, -998, -999, -1000, -999, -998, -995, -991, -987, -981, -974, -966, -957, -947, -936, -924, -911, -897, -882, -866, -849, -831, -813, -793, -773, -752, -730, -707, -684, -659, -634, -609, -582, -556, -528, -500, -471, -442, -413, -383, -352, -321, -290, -259, -227, -195, -163, -131, -98, -65, -33, 0, 33, 65, 98, 131, 163, 195, 227
#define resultLP 0, 0, -1, -2, -4, -8, -12, -17, -23, -28, -32, -34, -32, -26, -15, 0, 21, 46, 75, 105, 137, 169, 201, 231, 260, 288, 315, 340, 365, 389, 413, 436, 459, 481, 503, 524, 544, 564, 584, 603, 621, 638, 655, 671, 687, 701, 715, 728, 741, 752, 763, 773, 782, 791, 798, 805, 810, 815, 819, 822, 824, 825, 826, 825, 824, 822, 819, 815, 810, 805, 798, 791, 782, 773, 763, 752, 741, 728, 715, 701, 687, 671, 655, 638, 621, 603, 584, 564, 544, 524, 503, 481, 459, 436, 413, 389, 365, 341, 316, 291, 265, 239, 213, 187, 161, 134, 107, 81, 54, 27, 0, -27, -54, -81, -107, -134, -161, -187, -213, -239, -265, -291, -316, -341, -365, -389, -413, -436, -459, -481, -503, -524, -544, -564, -584, -603, -621, -638, -655, -671, -687, -701, -715, -728, -741, -752, -763, -773, -782, -791, -798, -805, -810, -815, -819, -822, -824, -825, -826, -825, -824, -822, -819, -815, -810, -805, -798, -791, -782, -773, -763, -752, -741, -728, -715, -701, -687, -671, -655, -638, -621, -603, -584, -564, -544, -524, -503, -481, -459, -436, -413, -389, -365, -341, -316, -291, -265, -239, -213, -187
#define resultHP 0, 1, 1, 0, -2, -3, -2, 0, 2, 4, 3, -3, -15, -3, 1, 3, 1, -1, -4, -5, -4, -3, -2, -1, -3, -3, -4, -4, -4, -4, -4, -5, -5, -6, -6, -6, -6, -6, -6, -7, -7, -7, -8, -8, -8, -8, -8, -8, -8, -8, -8, -9, -9, -8, -9, -8, -9, -9, -9, -9, -9, -9, -9, -9, -9, -8, -9, -8, -9, -9, -8, -8, -8, -8, -8, -8, -8, -8, -8, -7, -7, -7, -6, -6, -6, -6, -6, -6, -5, -5, -4, -4, -4, -4, -4, -3, -3, -3, -3, -2, -2, -2, -1, -1, 0, -1, -1, 0, 0, 0, 1, 1, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 8, 9, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 8, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 6, 6, 6, 6, 6, 6, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 1, 1


float LP[] = {coeffLP};
float HP[] = {coeffHP};


#define global_timer_ticks 333500000
#define CPU_frequency 667000000

XIicPs Iic;


int AudioRegSet(XIicPs *IIcPtr, u8 regAddr, u16 regData) {
    int Status;
    u8 SendBuffer[2];

    SendBuffer[0] = regAddr << 1;
    SendBuffer[0] = SendBuffer[0] | ((regData >> 8) & 0b1);

    SendBuffer[1] = regData & 0xFF;

    Status = XIicPs_MasterSendPolled(IIcPtr, SendBuffer,
                                     2, IIC_SLAVE_ADDR);
    if (Status != XST_SUCCESS) {
        xil_printf("IIC send failed\n\r");
        return XST_FAILURE;
    }
    /*
     * Wait until bus is idle to start another transfer.
     */
    while (XIicPs_BusIsBusy(IIcPtr)) {
        /* NOP */
    }
    return XST_SUCCESS;
}

/***	AudioInitialize(u16 timerID,  u16 iicID, u32 i2sAddr)
**
**	Parameters:
**		timerID - DEVICE_ID for the SCU timer
**		iicID 	- DEVICE_ID for the PS IIC controller connected to the SSM2603
**		i2sAddr - Physical Base address of the I2S controller
**
**	Return Value: int
**		XST_SUCCESS if successful
**
**	Errors:
**
**	Description:
**		Initializes the Audio demo. Must be called once and only once before calling
**		AudioRunDemo
**
*/

int AudioInitialize(u16 timerID, u16 iicID, u32 i2sAddr) //, u32 i2sTransmAddr, u32 i2sReceivAddr)
{
    int Status;
    XIicPs_Config *Config;
    u32 i2sClkDiv;

    TimerInitialize(timerID);

    /*
     * Initialize the IIC driver so that it's ready to use
     * Look up the configuration in the config table,
     * then initialize it.
     */
    Config = XIicPs_LookupConfig(iicID);
    if (NULL == Config) {
        return XST_FAILURE;
    }

    Status = XIicPs_CfgInitialize(&Iic, Config, Config->BaseAddress);
    if (Status != XST_SUCCESS) {
        return XST_FAILURE;
    }

    /*
     * Perform a self-test to ensure that the hardware was built correctly.
     */
    Status = XIicPs_SelfTest(&Iic);
    if (Status != XST_SUCCESS) {
        return XST_FAILURE;
    }

    /*
     * Set the IIC serial clock rate.
     */
    Status = XIicPs_SetSClk(&Iic, IIC_SCLK_RATE);
    if (Status != XST_SUCCESS) {
        return XST_FAILURE;
    }


    /*
     * Write to the SSM2603 audio codec registers to configure the device. Refer to the
     * SSM2603 Audio Codec data sheet for information on what these writes do.
     */
    Status = AudioRegSet(&Iic, 15, 0b000000000); //Perform Reset
    TimerDelay(75000);
    Status |= AudioRegSet(&Iic, 6, 0b000110000); //Power up
    Status |= AudioRegSet(&Iic, 0, 0b000010111);
    Status |= AudioRegSet(&Iic, 1, 0b000010111);
    Status |= AudioRegSet(&Iic, 2, 0b101111001);
    Status |= AudioRegSet(&Iic, 4, 0b000010000);
    Status |= AudioRegSet(&Iic, 5, 0b000000000);
    Status |= AudioRegSet(&Iic, 7, 0b000001010); //Changed so Word length is 24
    Status |= AudioRegSet(&Iic, 8, 0b000000000); //Changed so no CLKDIV2
    TimerDelay(75000);
    Status |= AudioRegSet(&Iic, 9, 0b000000001);
    Status |= AudioRegSet(&Iic, 6, 0b000100000);
    Status = AudioRegSet(&Iic, 4, 0b000010000);

    if (Status != XST_SUCCESS) {
        return XST_FAILURE;
    }

    i2sClkDiv = 1; //Set the BCLK to be MCLK / 4
    i2sClkDiv = i2sClkDiv | (31 << 16); //Set the LRCLK's to be BCLK / 64

    Xil_Out32(i2sAddr + I2S_CLK_CTRL_REG, i2sClkDiv); //Write clock div register

    Xil_Out32(AUDIO_CTRL_BASEADDR + I2S_RESET_REG, 0b110); //Reset RX and TX FIFOs
    Xil_Out32(AUDIO_CTRL_BASEADDR + I2S_CTRL_REG, 0b011); //Enable RX Fifo and TX FIFOs, disable mute
    return XST_SUCCESS;
}

void I2SFifoWrite(u32 i2sBaseAddr, u32 audioData) {
    Xil_Out32(i2sBaseAddr + 0x10, audioData); // write DATA
    Xil_Out32(i2sBaseAddr + 0x14, 4); // write the length of the DATA (4 bytes)

    //xil_printf("%x\n", Xil_In32(i2sBaseAddr + 0x00));
    while ((Xil_In32(i2sBaseAddr + 0x00) & 0x08000000) != 0x08000000) { ; } // waits for the transmission completes
    Xil_Out32(i2sBaseAddr + 0x00, 0x08000000); // ack the transmission complete
}

u32 I2SFifoRead(u32 i2sBaseAddr) {
    while (Xil_In32(i2sBaseAddr + 0x1C) == 0) { ; } // waits for a sample in the FIFO
    int data = Xil_In32(i2sBaseAddr + 0x20); // read the sample from the FIFO
    return data;
}

void initialize_FIFO(u32 fifoAddr) {
    Xil_Out32(AUDIO_FIFO + 0x2c, 0);

    // init
    xil_printf("FIFO_ISR:  0x%08x\n", Xil_In32(fifoAddr + FIFO_ISR));
    print("write FIFO_ISR\n\r");
    Xil_Out32(fifoAddr + FIFO_ISR, 0xFFFFFFFF);
    xil_printf("FIFO_ISR:  0x%08x\n", Xil_In32(fifoAddr + FIFO_ISR));
    xil_printf("FIFO_IER:  0x%08x\n", Xil_In32(fifoAddr + FIFO_IER));
    xil_printf("FIFO_TDFV: 0x%08x\n", Xil_In32(fifoAddr + FIFO_TDFV));
    xil_printf("FIFO_RDFO: 0x%08x\n", Xil_In32(fifoAddr + FIFO_RDFO));

    print("Write IER\n\r");
    Xil_Out32(fifoAddr + FIFO_IER, 0x0C000000);

    print("Write TDR\n\r");
    Xil_Out32(fifoAddr + FIFO_TDR, 0x00000000);


    xil_printf("FIFO_ISR:  0x%08x\n", Xil_In32(fifoAddr + FIFO_ISR));
    print("write FIFO_ISR\n\r");
    Xil_Out32(fifoAddr + FIFO_ISR, 0xFFFFFFFF);
    xil_printf("FIFO_ISR:  0x%08x\n", Xil_In32(fifoAddr + FIFO_ISR));
    xil_printf("FIFO_IER:  0x%08x\n", Xil_In32(fifoAddr + FIFO_IER));
    xil_printf("FIFO_TDFV: 0x%08x\n", Xil_In32(fifoAddr + FIFO_TDFV));
    xil_printf("FIFO_RDFO: 0x%08x\n", Xil_In32(fifoAddr + FIFO_RDFO));


    print("write FIFO_IER\n");
    Xil_Out32(fifoAddr + FIFO_IER, 0x04100000);
    xil_printf("FIFO_ISR:  0x%08x\n", Xil_In32(fifoAddr + FIFO_ISR));
    print("write FIFO_ISR\n");
    Xil_Out32(fifoAddr + FIFO_ISR, 0x00100000);
}

// -------------------------------------------------------------------------------------------------

/* ------------------------------------------------------------ */
/*		                   Added Utility Functions              */
/* ------------------------------------------------------------ */


void filter(int *L, int *R, int filter_len, const float *filter, int *bufferL, int *bufferR) {
    /*
     * Applies a filter to a stereo sample (L and R).
     * The function shifts the buffers by one position, inserts the new samples,
     * performs the dot product with the filter coefficients, and updates L and R in place.
     *
     * Inputs:
     * - L:          pointer to the left channel sample.
     * - R:          pointer to the right channel sample.
     * - filter_len: length of filter and buffers.
     * - filter:     pointer to filter coefficients array.
     * - bufferL:    pointer to left channel buffer.
     * - bufferR:    pointer to right channel buffer.
     *
     * Outputs:
     * - *L: filtered left sample.
     * - *R: filtered right sample.
     */
    for (int k = filter_len - 1; k > 0; k--) {
        bufferL[k] = bufferL[k - 1];
        bufferR[k] = bufferR[k - 1];
    }

    bufferL[0] = *L;
    bufferR[0] = *R;

    float sumL = 0;
    float sumR = 0;

    for (int i = 0; i < filter_len; i++) {
        sumL += bufferL[i] * filter[i];
        sumR += bufferR[i] * filter[i];
    }

    *L = (int) sumL;
    *R = (int) sumR;
}

void free_buffers(int *bufferLLP, int *bufferLHP, int *bufferRLP, int *bufferRHP) {
    /*
     * Frees the four dynamically allocated filter buffers.
     *
     * Inputs:
     * - bufferLLP: pointer to left buffer used for LP filtering.
     * - bufferLHP: pointer to left buffer used for HP filtering.
     * - bufferRLP: pointer to right buffer used for LP filtering.
     * - bufferRHP: pointer to right buffer used for HP filtering.
     *
     */
    free(bufferLLP);
    free(bufferLHP);
    free(bufferRLP);
    free(bufferRHP);
}

int compute_execution_cycles(u32 start, u32 end) {
    /*
     * Computes the number of elapsed cycles between two readings.
     *
     * Inputs:
     * - start: timer value captured at the beginning.
     * - end:   timer value captured at the end.
     *
     * Outputs:
     * - cycles: elapsed cycles.
     *
     */
    u32 cycles = (u32)(end - start);
    xil_printf("\nCycles required to filter a single sample: %u cycles\n", cycles);
    return cycles;
}

int compute_available_cycles(int execution_cycles, int *sampling_frequency_out) {
    /*
     * Computes an estimated sampling frequency and available processing cycles per sample
     * based on the measured execution time of a single filtering operation.
     *
     * Inputs:
     * - execution_cycles: measured global-timer cycles for one filtered sample.
     * - sampling_frequency_out: pointer where the computed sampling frequency is stored.
     *
     * Outputs:
     * - available_cycles: available processing cycles per sample.
     */
    int sampling_frequency = (CPU_frequency / 2) / execution_cycles;
    *sampling_frequency_out = sampling_frequency;
    xil_printf("Sampling frequency: %d Hz\n", sampling_frequency);
    int available_cycles = CPU_frequency / sampling_frequency;
    xil_printf("Available processing cycles: %d for each sample\n", available_cycles);

    return available_cycles;
}


int compute_max_taps(int execution_cycles, int available_cycles, int filter_type) {
    /*
     * Estimates the maximum number of filter taps that can be executed in real-time
     * for the current sampling frequency, based on measured execution cycles.
     *
     * Inputs:
     * - execution_cycles: measured global-timer ticks for one filter execution.
     * - available_cycles: available ticks per sample at the computed sampling frequency.
     * - filter_type: current number of taps (N_LP, N_HP, or 1 for no filter).
     *
     * Outputs:
     * - Returns the estimated maximum number of taps that can run in real time.
     */
    int cycles_per_tap = execution_cycles / filter_type;
    int max_taps = available_cycles / cycles_per_tap;
    xil_printf("Filter taps that can be performed real time: %d\n", max_taps);

    return max_taps;
}

void check_settings(int *last_switch,
                    int *filter_type,
                    int *execution_cycles,
                    int *sampling_frequency,
                    int *available_cycles,
                    int *cycles_per_tap,
                    int *max_taps,
                    int *counter,
                    volatile int *gpio_switch_data,
                    int *bufferLL, int *bufferRL,
                    int *bufferLH, int *bufferRH) {
    /*
     * Checks the state of the GPIO switches and updates filter mode and measurement state.
     * If the switch value changes, the function updates the selected filter type,
     * resets all filters' buffers, and resets all measurement variables/counters.
     *
     * Inputs:
     * - last_switch: pointer to the previously stored switch value.
     * - filter_type: pointer to the current filter type.
     * - execution_cycles: pointer to the last measured execution cycles.
     * - sampling_frequency: pointer to the computed sampling frequency.
     * - available_cycles: pointer to the available cycles.
     * - cycles_per_tap: pointer to cycles-per-tap.
     * - max_taps: pointer to max taps estimate.
     * - counter: pointer to sample counter.
     * - gpio_switch_data: pointer to GPIO switch register.
     * - bufferLL, bufferRL: LP buffers for L/R channels.
     * - bufferLH, bufferRH: HP buffers for L/R channels.
     *
     */
    if (*gpio_switch_data != *last_switch) {
        // change filter mode
        if (*gpio_switch_data == 1) {
            xil_printf("Switch value = %d | LP FILTER ON\n\r", *gpio_switch_data);
            *filter_type = N_LP;
        } else if (*gpio_switch_data == 3) {
            xil_printf("Switch value = %d | HP FILTER ON\n\r", *gpio_switch_data);
            *filter_type = N_HP;
        } else {
            xil_printf("Switch value = %d | NO FILTER\n\r", *gpio_switch_data);
            *filter_type = 1;
        }

        // reset filter buffers
        memset(bufferLL, 0, N_LP * sizeof(int));
        memset(bufferRL, 0, N_LP * sizeof(int));
        memset(bufferLH, 0, N_HP * sizeof(int));
        memset(bufferRH, 0, N_HP * sizeof(int));

        // reset measurements variables
        *execution_cycles = 0;
        *sampling_frequency = 0;
        *available_cycles = 0;
        *cycles_per_tap = 0;
        *max_taps = 0;
        *counter = 0;

        *last_switch = *gpio_switch_data;
    }
}

volatile int *gpio_switch_data = (int *) 0x41220000;

// -------------------------------------------------------------------------------------------------

/* ------------------------------------------------------------ */
/*		                    Main                                */
/* ------------------------------------------------------------ */

int main() {
    init_platform();

    Xil_ICacheDisable();
    Xil_DCacheDisable();

    AudioInitialize(SCU_TIMER_ID, AUDIO_IIC_ID, AUDIO_CTRL_BASEADDR);

    initialize_FIFO(AUDIO_FIFO);
    initialize_FIFO(FIR_FIFO);

    int SampleL, SampleR;


    // using calloc because it inatializes all the arrays to zero
    int *bufferLL = (int *) calloc(N_LP, sizeof(int));
    int *bufferRL = (int *) calloc(N_LP, sizeof(int));
    int *bufferLH = (int *) calloc(N_HP, sizeof(int));
    int *bufferRH = (int *) calloc(N_HP, sizeof(int));

    int last_switch = *gpio_switch_data;
    int counter = 0;
    u32 times[2];
    //times[0] contains the starting time instant of the filtering function
    //times[1] contains the final time instant of the filtering function
    int execution_cycles;
    int sampling_frequency;
    int available_cycles;
    int cycles_per_tap;
    int max_taps;
    int filter_type = 1;

    while (1) {
        check_settings(&last_switch, &filter_type, &execution_cycles, &sampling_frequency, &available_cycles,
                       &cycles_per_tap, &max_taps, &counter, gpio_switch_data, bufferLL, bufferRL, bufferLH, bufferRH);

        SampleL = I2SFifoRead(AUDIO_FIFO);
        SampleR = I2SFifoRead(AUDIO_FIFO);

        if (counter == 300) times[0] = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);

        if (counter == 301) {
            times[1] = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);

            // first task
            execution_cycles = compute_execution_cycles(times[0], times[1]);

            // second task
            available_cycles = compute_available_cycles(execution_cycles, &sampling_frequency);

            // third task
            max_taps = compute_max_taps(execution_cycles, available_cycles, filter_type);
        }


        if (*gpio_switch_data == 1) filter(&SampleL, &SampleR, N_LP, LP, bufferLL, bufferRL);
        else if (*gpio_switch_data == 3) filter(&SampleL, &SampleR, N_HP, HP, bufferLH, bufferRH);

        I2SFifoWrite(AUDIO_FIFO, SampleL);
        I2SFifoWrite(AUDIO_FIFO, SampleR);

        counter += 1;
    }

    free_buffers(bufferLL, bufferRL, bufferLH, bufferRH);
    cleanup_platform();
    return 0;
}
