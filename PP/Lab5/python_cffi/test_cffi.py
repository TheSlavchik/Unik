from cffi import FFI

class TestCFFI:
    def __init__(self, lib_path='./libvector_dot.dylib'):
        self.ffi = FFI()
        self.ffi.cdef("""
            #define VEC_LEN 4
            typedef struct {
                double result;
                int error;
            } DotResult;
            
            DotResult dot_product(const double *a, const double *b);
        """)
        self.lib = self.ffi.dlopen(lib_path)

    def dot_product(self, a, b):
        a_ptr = self.ffi.new("double[]", a)
        b_ptr = self.ffi.new("double[]", b)
        
        result = self.lib.dot_product(a_ptr, b_ptr)
        
        if result.error:
            raise ValueError("NULL pointer in C function")
            
        return result.result
    
    def run_test(self, pairs):
        return [self.dot_product(a, b) for a, b in pairs]

# ops = VectorOps()
# res = ops.dot_product([1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0])
