"""Compare default appearance, object settings, and temporary defaults."""

import matplotlib as mpl
import matplotlib.pyplot as plt

from report_helpers import make_report
from water_data import create_water_week


def main():
    days, produced, distributed = create_water_week()

    with plt.style.context("default"):
        fig, ax = make_report(days, produced, distributed)
        ax.set_title("Default Appearance")
        plt.show()

        fig, ax = make_report(days, produced, distributed)
        ax.set_facecolor("whitesmoke")
        ax.grid(alpha=0.30)
        for line in ax.lines:
            line.set_linewidth(3)
        ax.set_title("Settings on Individual Objects")
        plt.show()

        previous_width = mpl.rcParams["lines.linewidth"]
        print("Before context:", previous_width)

        # New objects inside the block receive these temporary defaults.
        with mpl.rc_context({"lines.linewidth": 3, "axes.grid": True}):
            fig, ax = make_report(days, produced, distributed)
            ax.set_title("Temporary Defaults with rc_context")
            print("Inside context:", mpl.rcParams["lines.linewidth"])
            plt.show()

        print("After context:", mpl.rcParams["lines.linewidth"])
        assert mpl.rcParams["lines.linewidth"] == previous_width


if __name__ == "__main__":
    main()
