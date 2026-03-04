#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xil_cache.h"
#include "xil_types.h"
#include "shared.h"
#include "saturate.h"

void worker_loop(void) {
    /*
     * Worker core loop for the two-core parallel FC forward pass.
     * The worker waits for the master to raise the start flag, reads the layer
     * parameters from shared memory, computes the second half of the FC outputs,
     * then signals completion by setting done1.
     * Finally, it waits for the master to drop the start flag and acknowledges
     * by clearing done1 before returning to the wait state.
     *
     */
    while (1) {
        // wait for start
        while (SHARED->start == 0) {
            /* busy-wait */
        }

        // Read parameters
        int in_s = SHARED->in_s;
        int out_s = SHARED->out_s;
        int qf = SHARED->qf;

        int start = out_s / 2;
        int end = out_s;

        for (int hkern = start; hkern < end; hkern++) {
            int32_t mac = ((int32_t) SHARED->bias[hkern]) << qf;
            for (int wkern = 0; wkern < in_s; wkern++) {
                // Q1.7 * Q1.7 = Q2.14 Product
                mac += (int32_t) SHARED->input[wkern] * (int32_t) SHARED->weights[hkern * in_s + wkern];
            }

            // Shift right by qf and saturate to return to Q1.7
            SHARED->output[hkern] = (DATA) saturate(mac >> qf);
        }

        // Computation completed
        SHARED->done1 = 1;

        // Wait for master start drop
        while (SHARED->start == 1) {
            /* busy-wait */
        }

        //Acknowledge
        SHARED->done1 = 0;
    }
}

int main(void) {
    Xil_ICacheDisable();
    Xil_DCacheDisable();

    worker_loop();
    return 0;
}
