# %%

import matplotlib.pyplot as plt
import numpy as np


def full_rosen(data: tuple[float, float], a: float, b: float) -> float:
    x = data[0]
    y = data[1]
    return (a-x)**2 + b*(y-x**2)**2


def rosen(x): return full_rosen(x, a=1, b=10)


xx = np.linspace(-2.0, 2.0, 100)
yy = np.linspace(-1.0, 3.0, 100)
X, Y = np.meshgrid(xx, yy)
Z = rosen([X, Y])

plt.figure(figsize=(4, 2.5))

ax = plt.subplot(121, projection='3d')
ax.plot_surface(X, Y, Z, cmap="jet")
ax.set_title("3D Resen")
ax.axis("off")

ax = plt.subplot(122)
ax.contour(X, Y, Z, 200, cmap="jet")
ax.set_aspect("equal")
ax.scatter(1, 1, color="r")
ax.annotate("Minimum\n(1, 1)", (1, 1), (0, 2),
            arrowprops=dict(arrowstyle="->"), ha="center")
ax.set_title("2D Resen")

plt.suptitle("$f(x,y) = (1-x)^2 + 10(y-x^2)^2$")
plt.tight_layout()
plt.show()
