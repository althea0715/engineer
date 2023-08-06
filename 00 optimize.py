# %%

from torch.autograd.functional import hessian, jacobian
from scipy.optimize import minimize
import torch
import time
from functools import partial

import matplotlib.pyplot as plt
import numpy as np


def full_rosen(data: list, a: float, b: float) -> float:
    x = data[0]
    y = data[1]
    return (a-x)**2 + b*(y-x**2)**2


rosen = partial(full_rosen, a=1, b=10)

xx = np.linspace(-2.0, 2.0, 100)
yy = np.linspace(-1.0, 3.0, 100)
X, Y = np.meshgrid(xx, yy)
Z = rosen([X, Y])

plt.figure(figsize=(7, 4))

ax = plt.subplot(121, projection='3d')
ax.plot_surface(X, Y, Z, cmap="jet")
ax.set_title("3D Resen")

ax = plt.subplot(122)
ax.contour(X, Y, Z, 200, cmap="jet")
ax.set_aspect("equal")
ax.scatter(1, 1, color="r")
ax.annotate("Minimum", (1, 1), (0, 2),
            arrowprops=dict(arrowstyle="->"), ha="center")
ax.set_title("2D Resen")

plt.suptitle("$f(x,y) = (1-x)^2 + 10(y-x^2)^2$")
plt.tight_layout()
plt.show()


# %%


def full_rosen(data, a: float, b: float) -> float:
    x = data[0]
    y = data[1]
    return (a-x)**2 + b*(y-x**2)**2


rosen = partial(full_rosen, a=1, b=10)


x = np.linspace(-2.0, 2.0, 100)
y = np.linspace(-1.0, 3.0, 100)
xx, yy = np.meshgrid(x, y)
zz = rosen([xx, yy])

plt.figure()

ax = plt.subplot(121, projection='3d')
ax.plot_surface(xx, yy, zz, cmap="jet")

ax = plt.subplot(122)
ax.contour(xx, yy, zz, 200, cmap="jet")
ax.set_aspect("equal")

plt.tight_layout()
plt.show()


# %%
methods = ["Nelder-Mead",
           "Powell",
           "CG",
           "BFGS",
           "Newton-CG",
           "L-BFGS-B",
           "TNC",
           "COBYLA",
           "SLSQP",
           "trust-constr",
           "dogleg",
           "trust-ncg",
           "trust-exact",
           "trust-krylov"]


class MinimizeCallback:
    def __init__(self):
        self.values = []

    def __call__(self, x, status=None):
        self.values.append(x)

    def get_values(self) -> tuple[x, y]:

        values = np.array(self.values)

        return values[:, 0], values[:, 1]

    def reset(self):
        self.values.clear()


callback = MinimizeCallback()

optim_results = {}

for method in methods:

    try:
        begin_perf = time.perf_counter()
        minimize(rosen, [-2, -1], callback=callback, method=method)
        end_perf = time.perf_counter()
        new_x, new_y = np.array(callback.get_values())
        optim_results[method] = {"X": new_x,
                                 "Y": new_y, "Perf": end_perf - begin_perf}

    except ValueError as e:
        print(method, e)

    except TypeError as e:
        print(method, e)

    callback.reset()


# %%

plt.figure(figsize=(16, 20))

for i, method in enumerate(methods, start=1):
    ax = plt.subplot(5, 4, i)

    ax.contour(xx, yy, zz, 200, cmap="jet")

    if res := optim_results.get(method):
        ax.plot(res["X"], res["Y"], "ro-", markersize=5)
        ax.set_title(f"{method} (iter:{len(res['X'])})")
        ax.annotate(f"{res['X'][-1]:.4f}, {res['Y'][-1]:.4f}", xy=(0.5,
                    0.95), xycoords="axes fraction", ha="center", va="center")
        ax.annotate(f"Process Time : {res['Perf']:.4f}", xy=(
            0.5, 0.90), xycoords="axes fraction", ha="center", va="center")
    else:
        ax.set_title(f"{method} (Can't Calculate)")

    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 3)

    ax.set_aspect("equal")


plt.suptitle("Results : No Jacobian")
plt.tight_layout()

plt.show()
# %%


def jac(x): return jacobian(rosen, torch.Tensor(x)).numpy()


optim_results = {}

for method in methods:

    try:
        begin_perf = time.perf_counter()
        minimize(rosen, [-2, -1], callback=callback, method=method, jac=jac)
        end_perf = time.perf_counter()
        new_x, new_y = np.array(callback.get_values())
        optim_results[method] = {"X": new_x,
                                 "Y": new_y, "Perf": end_perf - begin_perf}

    except ValueError as e:
        print(method, e)

    except TypeError as e:
        print(method, e)

    callback.reset()

# %%


plt.figure(figsize=(16, 20))

for i, method in enumerate(methods, start=1):
    ax = plt.subplot(5, 4, i)

    ax.contour(xx, yy, zz, 200, cmap="jet")

    if res := optim_results.get(method):
        ax.plot(res["X"], res["Y"], "ro-", markersize=5)
        ax.set_title(f"{method} (iter:{len(res['X'])})")
        ax.annotate(f"{res['X'][-1]:.4f}, {res['Y'][-1]:.4f}", xy=(0.5,
                    0.95), xycoords="axes fraction", ha="center", va="center")
        ax.annotate(f"Process Time : {res['Perf']:.4f}", xy=(
            0.5, 0.90), xycoords="axes fraction", ha="center", va="center")
    else:
        ax.set_title(f"{method} (Can't Calculate)")

    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 3)

    ax.set_aspect("equal")


plt.suptitle("Results : No Hessian")
plt.tight_layout()

plt.show()

# %%


def hess(x): return hessian(rosen, torch.Tensor(x)).numpy()


optim_results = {}

for method in methods:

    try:

        begin_perf = time.perf_counter()
        minimize(rosen, [-2, -1], callback=callback,
                 method=method, jac=jac, hess=hess)
        end_perf = time.perf_counter()
        new_x, new_y = np.array(callback.get_values())
        optim_results[method] = {"X": new_x,
                                 "Y": new_y, "Perf": end_perf - begin_perf}

    except ValueError as e:
        print(method, e)

    except TypeError as e:
        print(method, e)

    callback.reset()

# %%

plt.figure(figsize=(16, 20))

for i, method in enumerate(methods, start=1):
    ax = plt.subplot(5, 4, i)

    ax.contour(xx, yy, zz, 200, cmap="jet")

    if res := optim_results.get(method):
        ax.plot(res["X"], res["Y"], "ro-", markersize=5)
        ax.set_title(f"{method} (iter:{len(res['X'])})")
        ax.annotate(f"{res['X'][-1]:.4f}, {res['Y'][-1]:.4f}", xy=(0.5,
                    0.95), xycoords="axes fraction", ha="center", va="center")

        ax.annotate(f"Process Time : {res['Perf']:.4f}", xy=(
            0.5, 0.90), xycoords="axes fraction", ha="center", va="center")

    else:
        ax.set_title(f"{method} (Can't Calculate)")

    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 3)

    ax.set_aspect("equal")


plt.suptitle("Results")
plt.tight_layout()

plt.show()
