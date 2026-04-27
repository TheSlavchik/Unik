import numpy as np
import random

VEC_LEN = 4
NUM_CALLS = 100000

def generate_test_data(seed=740):
    random.seed(seed)
    np.random.seed(seed)
    
    vectors = []
    for i in range(NUM_CALLS + 1):
        vec = tuple(random.uniform(-1000, 1000) for _ in range(VEC_LEN))
        vectors.append(vec)
    
    pairs = [(vectors[i], vectors[i+1]) for i in range(NUM_CALLS)]
    return pairs
