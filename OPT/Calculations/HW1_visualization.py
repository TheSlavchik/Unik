import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y) + 0.1*(X**2 + Y**2)

# Создаем фигуру
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Строим поверхность
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
fig.colorbar(surf)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D поверхность')
plt.savefig("surface.png")
plt.show()

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y) + 0.1*(X**2 + Y**2)

# 2. Построение линий уровня
plt.figure(figsize=(8, 6))
# levels определяет количество линий или конкретные значения
cp = plt.contour(X, Y, Z, levels=20, cmap='viridis')
plt.annotate('', xy=(-1.13656, 1), xytext=(2, 1),
             arrowprops=dict(facecolor='red', shrink=0, width=2, headwidth=8))

# Вектор x2: из (-1.13656, 1) в (-1.13656, 0)
plt.annotate('', xy=(-1.13656, 0), xytext=(-1.13656, 1),
             arrowprops=dict(facecolor='blue', shrink=0, width=2, headwidth=8))

# Опционально: отметим сами точки, чтобы их было лучше видно
plt.plot([2, -1.13656, -1.13656], [1, 1, 0], 'ko', markersize=4)
# 3. Оформление
plt.clabel(cp, inline=True, fontsize=8) # Добавляет подписи значений на линии
plt.colorbar(cp) # Добавляет шкалу цветов
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.savefig("level_lines.png")
plt.show()