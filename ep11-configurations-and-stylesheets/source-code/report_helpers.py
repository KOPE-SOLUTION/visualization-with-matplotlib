"""Shared plotting code; colors and line widths come from the active style."""

import matplotlib.pyplot as plt


def draw_water_axes(ax, days, produced, distributed):
    """Draw the same data and axis limits on an existing Axes."""
    ax.plot(days, produced, marker="o", label="Produced")
    ax.plot(
        days,
        distributed,
        marker="s",
        linestyle="--",
        label="Distributed",
    )
    ax.set(
        title="Water Production and Distribution",
        xlabel="Day",
        ylabel="Volume (m³/day)",
        xticks=days,
        xlim=(0.7, 7.3),
        ylim=(3600, 4800),
    )
    ax.legend(loc="upper left")


def make_report(days, produced, distributed):
    """Create a Figure and Axes using the current appearance settings."""
    fig, ax = plt.subplots(figsize=(9, 4.5), layout="constrained")
    draw_water_axes(ax, days, produced, distributed)
    return fig, ax
