"""Compare points, wireframe, surface, and camera angles for one height grid."""

import numpy as np
import matplotlib.pyplot as plt

from plot_helpers import configure_3d
from stockpile_data import load_grid


def build_overview():
    x, y, height = load_grid()
    X, Y = np.meshgrid(x, y)
    fig, axes = plt.subplots(
        1, 3, figsize=(16, 5.8),
        subplot_kw={"projection": "3d"},
        layout="constrained",
    )
    points = axes[0].scatter(
        X.ravel(), Y.ravel(), height.ravel(),
        c=height.ravel(), cmap="viridis", vmin=0, vmax=8,
        s=40, depthshade=False,
    )
    axes[1].plot_wireframe(X, Y, height, color="tab:blue", linewidth=1.4)
    axes[2].plot_surface(
        X, Y, height, cmap="viridis", vmin=0, vmax=8,
        edgecolor="0.25", linewidth=0.5,
    )
    for ax, title in zip(axes, ["20 grid points", "Wireframe", "Surface"]):
        configure_3d(ax, title)
    # Both coloured panels use the same numeric colour range.
    fig.colorbar(
        points, ax=axes.tolist(), orientation="horizontal",
        shrink=0.42, pad=0.06, aspect=35, label="Height (m)",
    )
    fig.suptitle("One Height Grid — Three Representations")
    return fig


def build_view_comparison():
    x, y, height = load_grid()
    X, Y = np.meshgrid(x, y)
    fig, axes = plt.subplots(
        1, 2, figsize=(12, 5.8),
        subplot_kw={"projection": "3d"},
        layout="constrained",
    )
    for ax, elev, azim in zip(axes, [25, 60], [-60, 30]):
        surface = ax.plot_surface(
            X, Y, height, cmap="viridis", vmin=0, vmax=8,
            edgecolor="0.25", linewidth=0.5,
        )
        configure_3d(ax, f"elev={elev}, azim={azim}", elev=elev, azim=azim)
    fig.colorbar(
        surface, ax=axes.tolist(), orientation="horizontal",
        shrink=0.45, pad=0.06, aspect=30, label="Height (m)",
    )
    fig.suptitle("Same Heights and Axis Limits — Different Views")
    return fig


if __name__ == "__main__":
    with plt.style.context("default"):
        build_overview()
        build_view_comparison()
        plt.show()
