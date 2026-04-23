import time
from typing import Literal
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from scipy.optimize import minimize_scalar
from utils import get_gradient, linearize_function

class GradientProjectionsOptimizer():

    f: callable
    x_0: np.ndarray
    A: np.ndarray
    P: np.ndarray
    eps: float
    __report: list[dict]
    __duration: float

    def __init__(self, f: callable, x_0: np.ndarray, A: np.ndarray, b: np.ndarray, eps: float):
        self.f = f
        self.A = np.asarray(A, dtype=float)
        self.b = np.asarray(b, dtype=float)
        self.P = self.calculate_projection_matrix()
        self.x_0 = self.project_point_to_constraints(np.asarray(x_0, dtype=float))
        self.eps = eps
        self.__report = []
        self.__duration = 0.0
    
    def calculate_projection_matrix(self):
        A = self.A
        I = np.eye(A.shape[1])
        A_AT_inv = np.linalg.inv(A @ A.T)
        P = I - A.T @ A_AT_inv @ A
        return P
    
    def project_point_to_constraints(self, x):
        A, b = self.A, self.b
        correction = A.T @ np.linalg.inv(A @ A.T) @ (A @ x - b)
        return x - correction
    
    def minimize(self, max_iter=100):
        self.__report = []
        start_time = time.time()
        
        A, b = self.A, self.b
        diff = A @ self.x_0 - b
        if np.linalg.norm(diff) > 1e-9:
            correction = A.T @ np.linalg.inv(A @ A.T) @ diff
            x_k = self.x_0 - correction
        else:
            x_k = self.x_0.copy()
        
        for i in range(max_iter):
            grad_f = get_gradient(self.f, x_k) 
            S_k = -(self.P @ grad_f)
            S_k_flat = np.array(S_k).flatten()

            if np.linalg.norm(S_k) <= self.eps:
                self.__report.append({
                    'x_k': x_k,
                    'x_k1': x_k,
                    'alpha': 0.0,
                    's': S_k_flat
                })
                self.__duration = time.time() - start_time
                lam = np.linalg.inv(self.A @ self.A.T) @ self.A @ grad_f
                return x_k, np.array(lam).flatten()

            alpha_max = float('inf')
            for k in range(len(self.b)):
                ak_T = self.A[k]
                ak_T_Sk = np.dot(ak_T, S_k_flat)
                if ak_T_Sk > 1e-10: 
                    dist = (self.b[k] - np.dot(ak_T, x_k)) / ak_T_Sk
                    alpha_max = min(alpha_max, max(0.0, float(dist)))

            f_lin = linearize_function(self.f, x_k, S_k_flat)
            res_alpha = minimize_scalar(
                f_lin, 
                bounds=(0, alpha_max if alpha_max != float('inf') else 100), 
                method='bounded'
            )
            alpha_k = res_alpha.x
            x_next = x_k + alpha_k * S_k_flat

            self.__report.append({
                'x_k': x_k,
                'x_k1': x_next,
                'alpha': alpha_k,
                's': S_k_flat
            })
            
            x_k = x_next
            
        self.__duration = time.time() - start_time
        return x_k, None

    def get_report_table(self, r: int = 6):
        if not self.__report: return "Сначала запустите minimize()"
        tb = PrettyTable()
        tb.field_names = ['i', 'x_k', 'alpha', 'S_k', 'x_k1']
        for i, rep in enumerate(self.__report):
            tb.add_row([
                i, 
                np.round(rep['x_k'], r),  
                np.round(rep['alpha'], r), 
                np.round(rep['s'], r), 
                np.round(rep['x_k1'], r)
            ])
        tb.add_row([f"Время: {self.__duration:.4f}s", '-', '-', '-', '-'])
        return tb

    def get_report_plot(self, margin=1.0, 
        levels_start: int = -1, levels_stop: int = 5, 
        levels_count: int = 20, 
        levels_type: Literal['linspace', 'logspace'] = 'logspace',
        show_points_levels: bool = False):
    
        if not self.__report: return "Сначала запустите minimize()"
        
        path_x = [rep['x_k'][0] for rep in self.__report] + [self.__report[-1]['x_k1'][0]]
        path_y = [rep['x_k'][1] for rep in self.__report] + [self.__report[-1]['x_k1'][1]]
        path_x.append(self.__report[-1]['x_k1'][0])
        path_y.append(self.__report[-1]['x_k1'][1])

        x_min, x_max = min(path_x) - margin, max(path_x) + margin
        y_min, y_max = min(path_y) - margin, max(path_y) + margin

        X1, X2 = np.meshgrid(np.linspace(x_min, x_max, 150), np.linspace(y_min, y_max, 150))
        Z = np.array([self.f(np.array([x1, x2])) for x1, x2 in zip(np.ravel(X1), np.ravel(X2))]).reshape(X1.shape)

        plt.figure(figsize=(10, 8))

        levels_dict = {
            'linspace': np.linspace(levels_start, levels_stop, levels_count), 
            'logspace': np.logspace(levels_start, levels_stop, levels_count)
        }
        main_levels = levels_dict[levels_type]

        contours = plt.contour(X1, X2, Z, levels=main_levels, alpha=0.3, cmap='viridis', linestyles='dashed')
        plt.clabel(contours, inline=True, fontsize=8)

        if show_points_levels:
            points_z = [self.f(item['x_k']) for item in self.__report]
            points_z.append(self.f(self.__report[-1]['x_k1']))
            specific_levels = sorted(list(set(points_z)))
            p_contours = plt.contour(X1, X2, Z, levels=specific_levels, colors='red', linewidths=1.5, alpha=0.8)
            plt.clabel(p_contours, inline=True, fontsize=9, fmt='%.2f')

        x_lin = np.linspace(x_min, x_max, 100)
        for i in range(len(self.b)):
            a1, a2 = self.A[i, 0], self.A[i, 1]
            if abs(a2) > 1e-5:
                y_lin = (self.b[i] - a1 * x_lin) / a2
                plt.plot(x_lin, y_lin, color='black', linestyle='--', linewidth=2, label=f'Ограничение {i+1}')
            else:
                plt.axvline(x=self.b[i]/a1, color='black', linestyle='--', linewidth=2)

        plt.plot(path_x, path_y, 'ro-', markersize=4, label='Траектория', linewidth=1, alpha=0.6)

        text_offset = margin * 0.05
        for i, (xv, yv) in enumerate(zip(path_x[:-1], path_y[:-1])):
            plt.text(xv + text_offset, yv + text_offset, f'$x_{{{i}}}$', fontsize=9, fontweight='bold')

        for item in self.__report:
            xk = item['x_k']
            xk1 = item['x_k1']
            plt.quiver(xk[0], xk[1], xk1[0] - xk[0], xk1[1] - xk[1], 
                    angles='xy', scale_units='xy', scale=1, 
                    color='blue', width=0.003, alpha=0.5)

        plt.xlabel('$x_1$')
        plt.ylabel('$x_2$')
        plt.title('Иллюстрация метода проекции градиента' + (' (с линиями уровня точек)' if show_points_levels else ''))
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.show()

    def get_func_plot(self, margin=2.0):
        if not self.__report: return "Нет данных"
        
        path_x = [item['x_k'][0] for item in self.__report]
        path_y = [item['x_k'][1] for item in self.__report]
        
        x_min, x_max = min(path_x) - margin, max(path_x) + margin
        y_min, y_max = min(path_y) - margin, max(path_y) + margin

        X1, X2 = np.meshgrid(np.linspace(x_min, x_max, 60), np.linspace(y_min, y_max, 60))
        Z = np.array([self.f(np.array([x1, x2])) for x1, x2 in zip(np.ravel(X1), np.ravel(X2))]).reshape(X1.shape)

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.6, antialiased=True)

        z_min, z_max = Z.min(), Z.max()
        for i in range(len(self.b)):
            a1, a2 = self.A[i, 0], self.A[i, 1]
            if abs(a2) > 1e-5:
                x_c = np.linspace(x_min, x_max, 10)
                XC, ZC = np.meshgrid(x_c, np.linspace(z_min, z_max, 10))
                YC = (self.b[i] - a1 * XC) / a2
                ax.plot_surface(XC, YC, ZC, color='red', alpha=0.2)
    
        path_z = [self.f(item['x_k']) for item in self.__report]
        path_z.append(self.f(self.__report[-1]['x_k1']))
        full_path_x = path_x + [self.__report[-1]['x_k1'][0]]
        full_path_y = path_y + [self.__report[-1]['x_k1'][1]]
        
        ax.plot(full_path_x, full_path_y, path_z, 'ro-', markersize=5, linewidth=2, label='Траектория')
        
        ax.set_xlabel('$x_1$'); ax.set_ylabel('$x_2$'); ax.set_zlabel('$f(x)$')
        ax.set_title('3D визуализация')
        plt.show()

    def get_func_contour_plot(self, x_range=(-5, 5), y_range=(-5, 5), levels=20):
        x = np.linspace(x_range[0], x_range[1], 200)
        y = np.linspace(y_range[0], y_range[1], 200)
        X1, X2 = np.meshgrid(x, y)
        Z = np.array([self.f(np.array([x1, x2])) for x1, x2 in zip(np.ravel(X1), np.ravel(X2))]).reshape(X1.shape)

        plt.figure(figsize=(10, 8))
        contours = plt.contour(X1, X2, Z, levels=levels, cmap='viridis')
        plt.clabel(contours, inline=True, fontsize=8, fmt='%.1f')
        plt.xlabel('$x_1$'); plt.ylabel('$x_2$')
        plt.title('Линии уровня целевой функции')
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.show()
