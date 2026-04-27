import array
from vector_wrapper import py_dot_product

def run_test_cython(pairs):
    results = []
    for a, b in pairs:
        a_arr = array.array('d', a)
        b_arr = array.array('d', b)
        results.append(py_dot_product(a_arr, b_arr))
    return results