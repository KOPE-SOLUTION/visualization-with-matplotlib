"""Render all five README figures, using a path relative to this script by default."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from service_report import build_dashboard, build_individual_figures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "assets" / "plots")
    output_dir = parser.parse_args().output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    figures = build_individual_figures()
    try:
        figures["service-center-dashboard.png"] = build_dashboard()
        for filename, fig in figures.items():
            path = output_dir / filename
            fig.savefig(path, dpi=150)
            print(path)
    finally:
        for fig in figures.values():
            plt.close(fig)


if __name__ == "__main__":
    main()
