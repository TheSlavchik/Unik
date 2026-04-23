# cython: boundscheck=False, wraparound=False, nonecheck=False

cdef extern from "vector_dot.h":
    int VEC_LEN
    cdef struct DotResult:
        double result
        int error
    
    DotResult dot_product(const double *a, const double *b)

def dot_product_cython(a, b):
    cdef double[:] a_view = a
    cdef double[:] b_view = b
    
    cdef double a_arr[4]
    cdef double b_arr[4]
    
    for i in range(4):
        a_arr[i] = a_view[i]
        b_arr[i] = b_view[i]
    
    cdef DotResult res = dot_product(a_arr, b_arr)
    
    if res.error:
        raise ValueError("NULL pointer in C function")
    
    return res.result

def run_test_cython():
    from test_data import generate_test_data
    pairs = generate_test_data()
    results = []
    for a, b in pairs:
        results.append(dot_product_cython(a, b))
    return results