import numpy as np
import matplotlib.pyplot as plt


def make_field(x, y):
    hill = np.exp(-((x + 1.0) ** 2 + (y - 0.8) ** 2))
    valley = 0.8 * np.exp(-((x - 1.2) ** 2 + (y + 0.7) ** 2) / 0.7)
    ripple = 0.15 * np.sin(2 * x) * np.cos(2 * y)
    return hill - valley + ripple


x = np.linspace(-3, 3, 160)
y = np.linspace(-3, 3, 140)
X, Y = np.meshgrid(x, y)
Z = make_field(X, Y)

fig, ax = plt.subplots(figsize=(7, 6))
lines = ax.contour(X, Y, Z, levels=12, colors="black", linewidths=0.8)
ax.clabel(lines, inline=True, fontsize=8, fmt="%.2f")

ax.set(
    title="Contour lines",
    xlabel="x position",
    ylabel="y position",
    aspect="equal",
)
plt.show()
