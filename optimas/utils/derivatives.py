def derivative(func, x, h=1e-6):
    return (
        -func(x + 2*h) + 8*func(x + h) 
        - 8*func(x - h) + func(x - 2*h)
    ) / (12 * h)

def second_derivative(func, x, h=1e-6):
    return (
        -func(x + 2*h) + 16*func(x + h) - 30*func(x) 
        + 16*func(x - h) - func(x - 2*h)
    ) / (12 * h**2)