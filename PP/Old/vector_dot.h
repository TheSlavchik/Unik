#ifndef VECTOR_DOT_H
#define VECTOR_DOT_H

#define VEC_LEN 4

typedef struct {
    double result;
    int error;
} DotResult;

DotResult dot_product(const double *a, const double *b);

#endif