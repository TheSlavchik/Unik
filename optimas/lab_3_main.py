import sympy as sp
import numpy as np

from ConditionalOptimization import LagrangeOptimizer, GradientProjectionsOptimizer

# Вариант 11
# f(x, y) = x - y
# phi(x, y) = x^2 + y^2 - 2 = 0

x, y = sp.symbols('x y')
    
# optimizer = LagrangeOptimizer(
#     f= x - y, 
#     phi= x ** 2 + y ** 2 - 2, 
#     fvars=[x, y]
# )  

# print(optimizer.minimize())


#Для демки
# f(x, y) = x^2 + y^2
# phi(x, y) = 2x - y - 2

optimizer = LagrangeOptimizer(
    f= (x - 2) ** 2 + y**2, 
    phi= 2*x - y - 2, 
    fvars=[x, y]
)  
res = optimizer.minimize()
print(f"Метод множетелей Лагранжа: \nТочка: {res['point']}\nМножетели: {res['lambda']}\n")


def f(x):
    return (x[0] - 2) ** 2 + x[1] ** 2

optimizer = GradientProjectionsOptimizer(
    f=f, 
    x_0=(1,1),
    A=[[2,-1]],
    b=[2],
    eps=0.01
)
res = optimizer.minimize()
print(f"Метод проекций градиента:\nТочка: {res[0]}\nМножетели: {res[1]}")
print(optimizer.get_report_table())
optimizer.get_report_plot()


















# def f(x):
#     return (np.cos(x[0]) + np.cos(x[1]) + 
#             np.cos(x[0] - x[1]) + 0.05 * (x[0]**2 + x[1]**2)) 

# A = np.array([[1.0, -1.5]])
# b = np.array([3.0])

# x_0 = np.array([6.0, 2.0])

# optimizer = GradientProjectionsOptimizer(
#     f=f, 
#     x_0=x_0,
#     A=A,
#     b=b,
#     eps=0.01
# )
# print(optimizer.minimize())

# print(optimizer.get_report_table())
# optimizer.get_report_plot(
#                 margin=5.0, 
#                 levels_start=-20, 
#                 levels_stop=20, 
#                 levels_count=45, 
#                 levels_type='linspace',
#                 show_points_levels=True
#             )
# optimizer.get_func_plot()
