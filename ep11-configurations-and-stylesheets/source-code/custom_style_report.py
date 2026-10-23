"""Create a weekly water report using the stylesheet shipped with this lesson."""

from pathlib import Path

import matplotlib.pyplot as plt

from report_helpers import make_report
from water_data import create_water_week


STYLE_PATH = (
    Path(__file__).resolve().parents[1] / "styles" / "water-report.mplstyle"
)


def build_report():
    days, produced, distributed = create_water_week()
    with plt.style.context(["default", STYLE_PATH]):
        fig, ax = make_report(days, produced, distributed)
    return fig, ax


def main():
    with plt.style.context(["default", STYLE_PATH]):
        fig, ax = build_report()
        plt.show()


if __name__ == "__main__":
    main()
