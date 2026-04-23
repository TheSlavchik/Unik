import time
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from scipy.optimize import minimize
from typing import Callable, Literal, List
from dataclasses import dataclass

@dataclass
class Constraint:
    type_: Literal["eq", "ineq"]
    func: Callable

class PenaltyOptimizer:
    def __init__(self, f: Callable, x_0: np.ndarray, constraints: List[Constraint], eps: float, p: int = 2):
        self.f = f
        self.x_0 = np.asarray(x_0, dtype=float)
        self.constraints = constraints
        self.eps = eps
        self.p = p
        self.r = 1.0
        self.beta = 10.0
        self.__report = []
        self.__duration = 0.0

    def get_penalty_function(self, x: np.ndarray, r: float) -> float:
        penalty_sum = 0
        for c in self.constraints:
            val = c.func(x)
            if c.type_ == "ineq":
                penalty_sum += (max(0, val)) ** self.p
            else:
                penalty_sum += (abs(val)) ** self.p
        
        return self.f(x) + r * penalty_sum

    def minimize(self):
        self.__report = []
        start_time = time.time()
        curr_x = self.x_0
        curr_r = self.r
        
        while True:
            res = minimize(self.get_penalty_function, curr_x, args=(curr_r,), method='Nelder-Mead')
            new_x = res.x
            
            current_penalty_val = self.get_penalty_function(new_x, curr_r) - self.f(new_x)
            
            self.__report.append({
                'r': curr_r,
                'x_k': curr_x.copy(),
                'x_next': new_x.copy(),
                'f_x': self.f(new_x),
                'penalty': current_penalty_val
            })

            if current_penalty_val < self.eps:
                break
            
            curr_x = new_x
            curr_r *= self.beta
            
        self.__duration = time.time() - start_time
        return curr_x

    def get_report_table(self, precision: int = 4):
        tb = PrettyTable()
        tb.field_names = ['Iter', 'r', 'x_res', 'f(x)', 'Penalty (r*alpha)']
        for i, rep in enumerate(self.__report):
            tb.add_row([
                i, 
                round(rep['r'], 2),
                np.round(rep['x_next'], precision),
                round(rep['f_x'], precision),
                f"{rep['penalty']:.6f}"
            ])
        tb.add_row([f"Время выполнения: {self.__duration}", '-', '-', '-', '-'])
        return tb
    
    def plot_history(self, margin=2.0, levels_count=25):
        if not self.__report:
            return "Сначала запустите minimize()"

        path = np.array([r['x_k'] for r in self.__report] + [self.__report[-1]['x_next']])
        
        x_min, x_max = path[:, 0].min() - margin, path[:, 0].max() + margin
        y_min, y_max = path[:, 1].min() - margin, path[:, 1].max() + margin
        X1, X2 = np.meshgrid(np.linspace(x_min, x_max, 150), np.linspace(y_min, y_max, 150))

        Z = np.array([self.f(np.array([x1, x2])) for x1, x2 in zip(np.ravel(X1), np.ravel(X2))]).reshape(X1.shape)

        plt.figure(figsize=(10, 8))

        contours = plt.contour(X1, X2, Z, levels=levels_count, cmap='viridis', alpha=0.3)
        plt.clabel(contours, inline=True, fontsize=8)

        for i, c in enumerate(self.constraints):
            G = np.array([c.func(np.array([x1, x2])) for x1, x2 in zip(np.ravel(X1), np.ravel(X2))]).reshape(X1.shape)
            color = 'red' if c.type_ == 'ineq' else 'blue'
            plt.contour(X1, X2, G, levels=[0], colors=color, linewidths=2)

            if c.type_ == 'ineq':
                plt.contourf(X1, X2, G, levels=[0, 1e10], colors=color, alpha=0.1)

        plt.plot(path[:, 0], path[:, 1], 'ro-', markersize=5, label='Траектория (внешний штраф)', linewidth=1.5)
        
        for i, pt in enumerate(path[:-1]):
            plt.text(pt[0], pt[1], f' {i}', fontsize=9, color='black', fontweight='bold')

        plt.scatter(path[0, 0], path[0, 1], c='black', s=120, label='Старт (x0)', zorder=5)
        plt.scatter(path[-1, 0], path[-1, 1], c='green', marker='*', s=250, label='Финиш (x*)', zorder=6)

        plt.title(f"Метод штрафных функций (Внешние точки)\nПараметр r увеличивается: 1 -> {self.__report[-1]['r']}")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.legend()
        plt.grid(True, alpha=0.2)
        plt.show()
