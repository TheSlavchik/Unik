# cython: language_level=3
from vector_wrapper cimport dot_product, DotResult

def py_dot_product(double[:] a, double[:] b):
    if a.shape[0] != 4 or b.shape[0] != 4:
        raise ValueError("Vectors must be of length 4")
    
    cdef DotResult res = dot_product(&a[0], &b[0])
    
    if res.error:
        return None
    return res.result
