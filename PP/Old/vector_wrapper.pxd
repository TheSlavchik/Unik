cdef extern from "vector_dot.h":
    ctypedef struct DotResult:
        double result
        int error

    DotResult dot_product(const double *a, const double *b)
