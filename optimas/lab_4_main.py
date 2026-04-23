import numpy as np
from PenaltyOptimization import BarrierOptimizer, Constraint, PenaltyOptimizer


f_target = lambda x: (x[0]-2)**2 + (x[1] + 3)**2 + 4*x[1] - 1


constraints_v1 = [
    Constraint(type_="ineq", func=lambda x: x[0]**2 + x[1]),
    Constraint(type_="ineq", func=lambda x: x[0] - 2*x[1] - 8)
]

opt = BarrierOptimizer(f_target, x_0=[0.5, -1.5], constraints=constraints_v1, eps=0.05)
opt.minimize()
print(opt.get_report_table())
opt.plot_history()




opt = PenaltyOptimizer(f_target, x_0=[3, -6], constraints=constraints_v1, eps=0.05)
opt.minimize()
print(opt.get_report_table())
opt.plot_history()

