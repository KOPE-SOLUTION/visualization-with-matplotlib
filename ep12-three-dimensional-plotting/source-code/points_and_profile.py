"""Compare five separate 3D points with an ordered survey profile."""

import matplotlib.pyplot as plt

from plot_helpers import configure_3d
from stockpile_data import load_profile


def build_figure():
    x, y, height = load_profile()
    fig, axes = plt.subplots(
        1, 2, figsize=(12, 5.5),
        subplot_kw={"projection": "3d"},
        layout="constrained",
    )
    axes[0].scatter(x, y, height, s=65, color="tab:blue", depthshade=False)
    axes[1].plot(x, y, height, marker="o", linewidth=2, color="tab:blue")
    configure_3d(axes[0], "Five survey points")
    configure_3d(axes[1], "Connected profile at Y = 5 m")
    fig.suptitle("Cement Plant Stockyard — Synthetic Survey")
    return fig


if __name__ == "__main__":
    with plt.style.context("default"):
        build_figure()
        plt.show()
