#include "xparameters.h"
#include "xil_cache.h"
#include "xil_printf.h"
#include "shared.h"
#include "xil_io.h"

int main(void) {
    int i;

    // Disable caches for this exercise (same reason as core 0).
    Xil_ICacheDisable();
    Xil_DCacheDisable();

    while (Xil_In32(XPAR_AXI_GPIO_2_BASEADDR) == 0); //wait for the start on button

    // Wait until core 0 sets start flag
    while (SHARED->start == 0) {
        // busy-wait
    }

    // Process second half of the array
    for (i = ARRAY_SIZE / 2; i < ARRAY_SIZE; ++i) {
        SHARED->C[i] = SHARED->A[i] + SHARED->B[i];
    }

    SHARED->done1 = 1;

    while (1) {
        // Idle loop
    }

    return 0;
}
