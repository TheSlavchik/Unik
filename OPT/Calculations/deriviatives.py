import sympy as sp

def iteriation(f_input):
    x = sp.Symbol('x')
    point_value = float(input("Введите точку x: "))
    
    f = sp.sympify(f_input)
    f_prime = sp.diff(f, x)
    f_double_prime = sp.diff(f, x, 2)

    print(f"\nФункция: {f}")
    print(f"Первая производная: {f_prime}")
    print(f"Вторая производная: {f_double_prime}")

    func = sp.lambdify(x, f, 'math')
    grad = sp.lambdify(x, f_prime, 'math')
    hess = sp.lambdify(x, f_double_prime, 'math')

    for i in range(8):
        val_f = func(point_value)
        val_f_prime = grad(point_value)
        val_f_double_prime = hess(point_value)
        
        new_point = point_value - (val_f_prime / val_f_double_prime)
        
        print(f"{i+1} & {point_value:.5f} & {val_f:.5f} & {val_f_prime:.5f} & {val_f_double_prime:.5f} & {new_point:.5f} \\\ \hline")
        point_value = new_point

if __name__ == "__main__":
    iteriation("sin(2 - x) * cos(1) + 0.1*((2-x)**2+1)")
    iteriation("sin(-1.13656) * cos(1-x) + 0.1*((-1.13656)**2+(1-x)**2)")