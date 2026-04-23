from dataclasses import dataclass
import time
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from scipy.optimize import minimize
from typing import Callable, Literal

@dataclass
class Constraint:
    type_: Literal["eq", "ineq"]
    func: Callable 

class BarrierOptimizer:
    def __init__(self, f: Callable, x_0: np.ndarray, constraints: list[Constraint], eps: float):
        self.f = f
        self.x_0 = np.asarray(x_0, dtype=float)
        self.constraints = constraints 
        self.eps = eps
        self.r = 1.0
        self.beta = 0.5

    def get_barrier_function(self, x: np.ndarray, r: float) -> float:
        penalty = 0
        for c in self.constraints:
            val = c.func(x)
            if c.type_ == "ineq":
                if val >= 0: return 1e10 
                penalty -= np.log(-val)
            elif c.type_ == "eq":
                penalty += (1.0 / (r**2)) * (val**2) 
        return self.f(x) + r * penalty

    def minimize(self):
        self.__report = []
        start_time = time.time()
        curr_x = self.x_0
        curr_r = self.r
        
        while True:
            res = minimize(self.get_barrier_function, curr_x, args=(curr_r,), method='Nelder-Mead')
            new_x = res.x
            self.__report.append({'r': curr_r, 'x_k': curr_x.copy(), 'x_next': new_x.copy(), 'f_x': self.f(new_x)})
            if curr_r < self.eps: break
            curr_x, curr_r = new_x, curr_r * self.beta
            
        self.__duration = time.time() - start_time
        return curr_x

    def get_report_table(self, precision: int = 4):
        tb = PrettyTable()
        tb.field_names = ['Iter', 'r', 'x_res', 'f(x)']
        for i, rep in enumerate(self.__report):
            tb.add_row([i, round(rep['r'], 6), np.round(rep['x_next'], precision), round(rep['f_x'], precision)])
        tb.add_row([f"Время выполнения: {self.__duration}", '-', '-', '-'])
        return tb

    def plot_history(self, margin=1.5):
        path = np.array([r['x_k'] for r in self.__report] + [self.__report[-1]['x_next']])
        x_min, x_max = path[:, 0].min() - margin, path[:, 0].max() + margin
        y_min, y_max = path[:, 1].min() - margin, path[:, 1].max() + margin
        
        X1, X2 = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
        Z = np.array([self.f(np.array([x, y])) for x, y in zip(np.ravel(X1), np.ravel(X2))]).reshape(X1.shape)

        plt.figure(figsize=(10, 7))
        plt.contour(X1, X2, Z, levels=30, cmap='viridis', alpha=0.3)

        for i, c in enumerate(self.constraints):
            G = np.array([c.func(np.array([x, y])) for x, y in zip(np.ravel(X1), np.ravel(X2))]).reshape(X1.shape)
            color = 'red' if c.type_ == 'ineq' else 'blue'
            plt.contour(X1, X2, G, levels=[0], colors=color, linewidths=2)
            plt.fill_between([], [], color=color, alpha=0.1, label=f'Ограничение {i+1} ({c.type_})')

        plt.plot(path[:, 0], path[:, 1], 'bo-', markersize=4, label='Траектория')
        plt.scatter(path[0,0], path[0,1], c='green', s=100, label='Старт', zorder=5)
        plt.scatter(path[-1,0], path[-1,1], c='red', marker='*', s=200, label='Финиш', zorder=5)
        plt.legend(); plt.grid(True, alpha=0.3); plt.show()

