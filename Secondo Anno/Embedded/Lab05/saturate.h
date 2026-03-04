// saturate.h
#ifndef SRC_SATURATE_H_
#define SRC_SATURATE_H_


#include <stdint.h>

// Limits for signed 8-bit (-128 to 127)
#define _MAX_ 127
#define _MIN_ -128

static inline int32_t saturate(int32_t mac) {
    /*
     * Saturates a 32-bit value to the signed 8-bit range.
     * This is used after right-shifting the accumulator to bring it back to the
     * DATA range int8_t.
     *
     * Inputs:
     * - mac: 32-bit value to be saturated (usually a shifted MAC accumulator).
     *
     * Outputs:
     * - mac: 32-bit input value modified to [-128, 127] as int32_t.
     */
    if (mac > _MAX_) return _MAX_;
    if (mac < _MIN_) return _MIN_;
    return mac;
}

#endif /* SRC_SATURATE_H_ */
