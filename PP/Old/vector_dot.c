#include <stddef.h>
#include "vector_dot.h"

DotResult dot_product(const double *a, const double *b) {
    DotResult res;
    res.result = 0.0;
    res.error = 0;

    if (a == NULL || b == NULL) {
        res.error = 1;
        return res;
    }

    res.result = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];

    return res;
}
