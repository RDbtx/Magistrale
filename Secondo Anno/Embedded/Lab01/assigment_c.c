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

#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"

volatile int *gpio_led_data = 0x40000000;
volatile int *gpio_switch_data = 0x40010000;
volatile int *gpio_button_data = 0x40020000;

volatile int *IER = (volatile int *) 0x41200008;
volatile int *MER = (volatile int *) 0x4120001C;

volatile int *IISR = (volatile int *) 0x41200000;
volatile int *IIAR = (volatile int *) 0x4120000C;

volatile int *GGIER_1 = (volatile int *) 0x4001011C;
volatile int *GIER_1 = (volatile int *) 0x40010128;
volatile int *GISR_1 = (volatile int *) 0x40010120;

volatile int *GGIER_2 = (volatile int *) 0x4002011C;
volatile int *GIER_2 = (volatile int *) 0x40020128;
volatile int *GISR_2 = (volatile int *) 0x40020120;

volatile int finale_matricola = 9; // Riccardo Deidda M: 70/90/00639


void myISR(void) __attribute__((interrupt_handler));

int main(void) {
    // 0) Clear stale pendings
    //	*IER  = 0;
    //	*MER  = 0;
    //    *GISR_1 = 0xFFFFFFFF;
    //    *GISR_2 = 0xFFFFFFFF;
    //    *IIAR   = 0xFFFFFFFF;
    //    (void)*GISR_1; (void)*GISR_2; (void)*IIAR;

    // 1) (Optional) set inputs if these are input channels (TRI=1s)
    *(volatile int *) (0x40010000 + 0x4) = 0xFFFFFFFF; // GPIO1 TRI
    *(volatile int *) (0x40020000 + 0x4) = 0xFFFFFFFF; // GPIO2 TRI


    //    // 2) Enable device interrupts
    *GIER_2 = 0x1;
    *GIER_1 = 0x1;
    *GGIER_1 = 0x80000000;
    *GGIER_2 = 0x80000000;
    //
    //
    //    // 3) Enable INTC lines (match wiring!) ///jisbn74
    *IER = 0x3; // enable IRQ0 and IRQ1 (use 0x2 if only GPIO2 is wired)
    *MER = 0x3; //0b11     // ME | HIE

    microblaze_enable_interrupts();

    while (1) {
    }
}


void myISR(void) {
    unsigned p = *IISR; // Snapshot of interrupt status

    // ---- SWITCH INTERRUPT ----
    if (p & 0x1) {
        // GPIO1 on INTC[0] (Switches)
        *GISR_1 = 0x1; // Clear interrupt flag for GPIO1
        *IIAR = 0x1; // Acknowledge the interrupt for GPIO1

        int msb_index = -1;

        // Find the position of the MSB
        for (int i = 3; i >= 0; i--) {
            if ((*gpio_switch_data) & (1 << i)) {
                msb_index = i;
                break;
            }
        }

        // show normal MSB
        if (msb_index >= 0)
            *gpio_led_data = msb_index;
        else
            *gpio_led_data = 0;
    }

    // ---- BUTTON INTERRUPT ----
    if (p & 0x2) {
        // GPIO2 on INTC[1] (Button)
        *GISR_2 = 0x1; // Clear interrupt flag for GPIO2
        *IIAR = 0x2; // Acknowledge the interrupt for GPIO2

        // if button is pressed, show continuously ~(led + Student ID) until switches are modified
        if (*gpio_button_data == 1) {
            *gpio_led_data = *gpio_led_data + finale_matricola;
            *gpio_led_data = ~(*gpio_led_data);
        }
    }
}
