import numpy as np

def get_axes(n) -> list[np.ndarray]:
    axes = []
    for i in range(n):
        e_i = np.zeros(n)
        e_i[i] = 1.0
        axes.append(e_i)
    return axes