import vector_lib

def run_test_cpython(pairs):
    results = []
    for a, b in pairs:
        results.append(vector_lib.dot_product(list(a), list(b)))
    return results
