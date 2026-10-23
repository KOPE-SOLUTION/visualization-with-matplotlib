"""Side-by-side figures with fixed data and scales."""

import matplotlib as mpl
import matplotlib.pyplot as plt

from custom_style_report import STYLE_PATH
from report_helpers import draw_water_axes
from water_data import create_water_week


def build_style_comparison():
    days, produced, distributed = create_water_week()
    with plt.style.context("default"):
        fig = plt.figure(figsize=(12, 4.6), layout="constrained")
        styles = [("default", "Default"), (STYLE_PATH, "Water Report Style")]

        for position, (style, title) in enumerate(styles, start=1):
            # Axes and lines must be created while the chosen style is active.
            with plt.style.context(["default", style]):
                ax = fig.add_subplot(1, 2, position)
                draw_water_axes(ax, days, produced, distributed)
                ax.set_title(title)

        fig.suptitle("Same Data, Different Appearance", fontsize=16)
    return fig


def build_context_comparison():
    days, produced, distributed = create_water_week()
    with plt.style.context("default"):
        fig = plt.figure(figsize=(14, 4.5), layout="constrained")
        default_width = mpl.rcParams["lines.linewidth"]

        ax = fig.add_subplot(1, 3, 1)
        draw_water_axes(ax, days, produced, distributed)
        ax.set_title(f"Before: {default_width:g} pt")

        with mpl.rc_context({"lines.linewidth": 4}):
            ax = fig.add_subplot(1, 3, 2)
            draw_water_axes(ax, days, produced, distributed)
            ax.set_title("Inside context: 4 pt")

        ax = fig.add_subplot(1, 3, 3)
        draw_water_axes(ax, days, produced, distributed)
        ax.set_title(f"After: {mpl.rcParams['lines.linewidth']:g} pt")
        fig.suptitle("Temporary Defaults with rc_context", fontsize=16)
    return fig


def main():
    build_style_comparison()
    build_context_comparison()
    plt.show()


if __name__ == "__main__":
    main()
