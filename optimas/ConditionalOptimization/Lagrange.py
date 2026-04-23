import sympy as sp

class LagrangeOptimizer():

    def __init__(self, f, phi, fvars):
        self.f = f
        self.phi = phi
        self.vars = fvars
        self.lam = sp.symbols('lambda')
        self.u = self.f - self.lam * self.phi

    def minimize(self):
        system = [sp.diff(self.u, v) for v in self.vars]
        system.append(self.phi)
        solutions = sp.solve(system, self.vars + [self.lam], dict=True)

        return min([
            {
                'point': {v: float(sol[v]) for v in self.vars},
                'lambda': float(sol[self.lam]),
                'f_value': float(self.f.subs(sol)),
            }
            for sol in solutions
        ], key = lambda x: x['f_value'])
    