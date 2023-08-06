# %%

import torch
from torch.autograd.functional import hessian, jacobian


def full_rosen(data: tuple[float, float], a: float, b: float) -> float:
    x = data[0]
    y = data[1]
    return (a-x)**2 + b*(y-x**2)**2


def rosen(x): return full_rosen(x, a=1, b=10)
def jac(x): return jacobian(rosen, torch.Tensor(x)).numpy()
def hess(x): return hessian(rosen, torch.Tensor(x)).numpy()
