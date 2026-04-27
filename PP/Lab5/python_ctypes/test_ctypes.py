import ctypes
import os

class DotResult(ctypes.Structure):
    _fields_ = [
        ("result", ctypes.c_double),
        ("error", ctypes.c_int)
    ]

class TestCtypes:
    def __init__(self, lib_name="libvector_dot.dylib"):
        lib_path = os.path.abspath(lib_name)
        self.lib = ctypes.CDLL(lib_path)
        
        self.lib.dot_product.argtypes = [
            ctypes.POINTER(ctypes.c_double), 
            ctypes.POINTER(ctypes.c_double)
        ]
        self.lib.dot_product.restype = DotResult

    def dot_product(self, a, b):
        if len(a) != len(b):
            raise ValueError("Vectors must have the same length")
        
        size = len(a)
        a_arr = (ctypes.c_double * size)(*a)
        b_arr = (ctypes.c_double * size)(*b)
        
        res = self.lib.dot_product(a_arr, b_arr)
        
        if res.error:
            raise ValueError("C function error: possible NULL pointer or computation issue")
            
        return res.result

    def run_test(self, pairs):
        return [self.dot_product(a, b) for a, b in pairs]
