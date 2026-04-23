import numpy as np

def get_gradient(f: callable, x_0: np.ndarray, eps: float = 1e-6):
    x_0 = np.asarray(x_0)
    grad = np.zeros_like(x_0, dtype=float)
    x_eps = x_0.astype(float)
    
    for i in range(len(x_0)):
        old_val = x_eps[i]

        x_eps[i] = old_val + eps
        f_plus = f(x_eps)
        
        x_eps[i] = old_val - eps
        f_minus = f(x_eps)
        
        grad[i] = (f_plus - f_minus) / (2 * eps)

        x_eps[i] = old_val
        
    return grad