"""Display the same weekly report with five built-in styles."""

import matplotlib.pyplot as plt

from report_helpers import make_report
from water_data import create_water_week


def main():
    days, produced, distributed = create_water_week()
    style_names = ["default", "ggplot", "bmh", "dark_background", "grayscale"]

    for style_name in style_names:
        # Reset within the context so settings do not mix with a previous style.
        with plt.style.context(["default", style_name]):
            fig, ax = make_report(days, produced, distributed)
            ax.set_title(f"Water Utility — {style_name}")
            plt.show()


if __name__ == "__main__":
    main()
