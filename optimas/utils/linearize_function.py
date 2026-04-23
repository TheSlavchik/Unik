import numpy as np

def linearize_function(f: callable, x_k: np.ndarray, direction: np.ndarray):
    def linear_f(l: float) -> float:
        return f(x_k + l * direction)
    return linear_f