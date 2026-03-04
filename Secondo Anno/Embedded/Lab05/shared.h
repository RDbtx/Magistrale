// shared.h
#ifndef SHARED_H
#define SHARED_H

#include "xil_types.h"
#include <stdint.h>

#define SHARED_BASE 0x2F100000U

typedef int8_t DATA; // Change from short int (16-bit) to int8_t (8-bit)

typedef struct {
    // ---- FC parameters ----
    DATA *input; // pointer to input vector
    DATA *output; // pointer to output vector
    DATA *weights; // pointer to weights matrix
    DATA *bias; // pointer to bias vector

    int in_s; // input size
    int out_s; // output size
    int qf; // quantization factor

    /* ---- Synchronization ---- */
    volatile u32 start; // master sets to 1
    volatile u32 done0; // set by master
    volatile u32 done1; // worker sets to 1
} shared_mem_t;

#define SHARED ((volatile shared_mem_t *)SHARED_BASE)

#endif // SHARED_H
