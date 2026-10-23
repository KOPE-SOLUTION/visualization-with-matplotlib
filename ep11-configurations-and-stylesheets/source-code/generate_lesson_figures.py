"""Generate README figures; output paths are independent of the working directory."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from custom_style_report import STYLE_PATH, build_report
from style_comparison import build_context_comparison, build_style_comparison


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "plots",
        help="Directory for generated PNG files.",
    )
    output_dir = parser.parse_args().output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    figures = {
        "style-comparison.png": build_style_comparison(),
        "rc-context-scope.png": build_context_comparison(),
    }
    with plt.style.context(["default", STYLE_PATH]):
        figures["water-report.png"], _ = build_report()
        for filename, fig in figures.items():
            destination = output_dir / filename
            fig.savefig(destination, dpi=160, facecolor=fig.get_facecolor())
            plt.close(fig)
            print(destination)


if __name__ == "__main__":
    main()
