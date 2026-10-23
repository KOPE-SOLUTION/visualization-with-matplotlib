"""Compare 3D level curves with a 2D height map of the same grid."""

import numpy as np
import matplotlib.pyplot as plt

from plot_helpers import configure_3d
from stockpile_data import load_grid


def build_figure():
    x, y, height = load_grid()
    X, Y = np.meshgrid(x, y)
    levels = [1, 3, 5, 7]
    fig = plt.figure(figsize=(12, 5.5), layout="constrained")
    ax3d = fig.add_subplot(1, 2, 1, projection="3d")
    ax2d = fig.add_subplot(1, 2, 2)

    ax3d.contour(X, Y, height, levels=levels, cmap="viridis", vmin=0, vmax=8)
    configure_3d(ax3d, "3D contours at 1, 3, 5, 7 m")

    filled = ax2d.contourf(
        X, Y, height, levels=np.arange(0, 9), cmap="viridis", vmin=0, vmax=8,
    )
    lines = ax2d.contour(
        X, Y, height, levels=levels, colors="0.2", linewidths=0.8,
    )
    ax2d.clabel(lines, levels=[3, 5, 7], fmt="%g m", fontsize=9)
    ax2d.set(
        title="2D height map",
        xlabel="X position (m)", ylabel="Y position (m)",
        xlim=(0, 20), ylim=(0, 15),
        xticks=x, yticks=y,
    )
    ax2d.set_aspect("equal")
    fig.colorbar(filled, ax=ax2d, shrink=0.75, pad=0.05, label="Height (m)")
    fig.suptitle("Same Survey — Contours in 3D and 2D")
    return fig


if __name__ == "__main__":
    with plt.style.context("default"):
        build_figure()
        plt.show()
