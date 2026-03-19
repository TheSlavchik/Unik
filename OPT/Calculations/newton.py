import numpy as np
import matplotlib.pyplot as plt

# Исходная функция
def f(x):
    return -np.log(x) - np.log(1 - x)

# Первая производная
def df(x):
    return -1/x + 1/(1-x)

# Вторая производная (Гессиан для 1D)
def ddf(x):
    return 1/(x**2) + 1/((1-x)**2)

# Квадратичная аппроксимация (парабола Ньютона)
def newton_quad(x, x_n):
    return f(x_n) + df(x_n)*(x - x_n) + 0.5*ddf(x_n)*(x - x_n)**2

# Параметры визуализации
x_plot = np.linspace(0.01, 0.99, 400)
current_x = 0.15  # Начальная точка
iterations = 3
colors = ['red', 'blue', 'green']

plt.figure(figsize=(10, 6))
plt.plot(x_plot, f(x_plot), 'k', lw=2, label='f(x) = -ln(x) - ln(1-x)')

for i in range(iterations):
    # Диапазон для отрисовки локальной параболы
    x_range = np.linspace(max(0.01, current_x - 0.15), min(0.99, current_x + 0.15), 100)
    plt.plot(x_range, newton_quad(x_range, current_x), '--', color=colors[i], 
             label=f'Парабола в x_{i}={current_x:.2f}')
    plt.scatter([current_x], [f(current_x)], color=colors[i], zorder=5)
    
    # Шаг Ньютона: x = x - f'/f''
    current_x = current_x - df(current_x) / ddf(current_x)

plt.axvline(0.5, color='gray', linestyle=':', label='Оптимум (x=0.5)')
plt.title('Визуализация итераций метода Ньютона')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(1, 5)
plt.show()
