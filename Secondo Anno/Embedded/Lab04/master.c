#include "xparameters.h"
#include "xil_cache.h"
#include "xil_printf.h"
#include "xtime_l.h"
#include "shared.h"
#include "xil_io.h"


u32 compute_time(u32 start, u32 end) {
    return end - start;
}

void vec_add_serial(u32 *restrict c, const u32 *restrict a, const u32 *restrict b, int n) {
    for (int i = 0; i < n; ++i) {
        c[i] = a[i] + b[i];
    }
}

// Parallel Implementation
void main_parallel(void) {
    u32 t_start, t_end;

    // Disable caches to avoid coherency issues for this simple exercise.
    Xil_ICacheDisable();
    Xil_DCacheDisable();
    int i;

    // Initialize data in shared memory
    for (i = 0; i < ARRAY_SIZE; ++i) {
        SHARED->A[i] = i;
        SHARED->B[i] = 2 * i;
    }

    // Init flags
    SHARED->done0 = 0;
    SHARED->done1 = 0;
    SHARED->start = 0;

    while (Xil_In32(XPAR_AXI_GPIO_2_BASEADDR) == 0); //wait for the start on button


    // Signal core 1 to start
    SHARED->start = 1;
    t_start = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    // Core 0 processes first half
    for (i = 0; i < ARRAY_SIZE / 2; ++i) {
        SHARED->C[i] = SHARED->A[i] + SHARED->B[i];
    }
    SHARED->done0 = 1;

    // Wait until core 1 finishes
    while (SHARED->done1 == 0) {
        // busy-wait
    }

    t_end = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);

    // Check correctness
    int errors = 0;
    for (i = 0; i < ARRAY_SIZE; ++i) {
        u32 expected = SHARED->A[i] + SHARED->B[i];
        if (SHARED->C[i] != expected) {
            errors++;
            if (errors < 10) {
                xil_printf("Mismatch at %d: got %lu, expected %lu\r\n",
                           i,
                           (unsigned long) SHARED->C[i],
                           (unsigned long) expected);
                int idx = i;
                xil_printf("Debug at %d: A=%lu, B=%lu, C=%lu, expected=%lu\r\n",
                           idx,
                           (unsigned long) SHARED->A[idx],
                           (unsigned long) SHARED->B[idx],
                           (unsigned long) SHARED->C[idx],
                           (unsigned long) (SHARED->A[idx] + SHARED->B[idx]));
            }
        }
    }


    xil_printf("Errors = %d, start = %x, end = %x, duration = %x\r\n",
               errors, t_start, t_end, compute_time(t_start, t_end));

    while (1) {
        // Idle loop
    }
}

// Serial Implementation
void main_serial() {
    u32 t_start, t_end;
    Xil_ICacheDisable();
    Xil_DCacheDisable();
    int i;

    static u32 A[ARRAY_SIZE];
    static u32 B[ARRAY_SIZE];
    static u32 C[ARRAY_SIZE];

    // Initialize data in shared memory
    for (i = 0; i < ARRAY_SIZE; ++i) {
        A[i] = i;
        B[i] = 2 * i;
    }
    t_start = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);
    vec_add_serial(C, A, B, ARRAY_SIZE);
    t_end = Xil_In32(GLOBAL_TMR_BASEADDR + GTIMER_COUNTER_LOWER_OFFSET);

    int errors = 0;
    for (i = 0; i < ARRAY_SIZE; ++i) {
        u32 expected = A[i] + B[i];
        if (C[i] != expected) {
            errors++;
            if (errors < 10) {
                xil_printf("Mismatch at %d: got %lu, expected %lu\r\n",
                           i,
                           (unsigned long) C[i],
                           (unsigned long) expected);
                int idx = i;
                xil_printf("Debug at %d: A=%lu, B=%lu, C=%lu, expected=%lu\r\n",
                           idx,
                           (unsigned long) A[idx],
                           (unsigned long) B[idx],
                           (unsigned long) C[idx],
                           (unsigned long) (A[idx] + B[idx]));
            }
        }
    }

    xil_printf("Errors = %d, start = %x, end = %x, duration = %x\r\n",
               errors, t_start, t_end, compute_time(t_start, t_end));
}

int main() {
    main_serial();
    return 0;
}
