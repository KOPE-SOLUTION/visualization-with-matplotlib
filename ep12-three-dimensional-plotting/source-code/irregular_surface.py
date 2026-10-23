"""Optional example: triangulate an irregular synthetic survey."""

import matplotlib.pyplot as plt

from plot_helpers import configure_3d
from stockpile_data import load_irregular


def build_figure():
    x, y, height = load_irregular()
    fig, axes = plt.subplots(
        1, 2, figsize=(12, 5.8),
        subplot_kw={"projection": "3d"},
        layout="constrained",
    )
    points = axes[0].scatter(
        x, y, height, c=height, cmap="viridis",
        vmin=0, vmax=8, s=60, depthshade=False,
    )
    axes[1].plot_trisurf(
        x, y, height, cmap="viridis", vmin=0, vmax=8,
        edgecolor="0.25", linewidth=0.6,
    )
    configure_3d(axes[0], "11 irregular survey points")
    configure_3d(axes[1], "Triangulated surface")
    fig.colorbar(
        points, ax=axes.tolist(), orientation="horizontal",
        shrink=0.45, pad=0.06, aspect=30, label="Height (m)",
    )
    fig.suptitle("Triangles Connect Samples — Not Additional Measurements")
    return fig


if __name__ == "__main__":
    with plt.style.context("default"):
        build_figure()
        plt.show()
