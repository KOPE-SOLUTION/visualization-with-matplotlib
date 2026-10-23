"""Generate lesson PNGs without a GUI, independently of the working directory."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from points_and_profile import build_figure as build_points
from surface_views import build_overview, build_view_comparison
from contour_comparison import build_figure as build_contours
from irregular_surface import build_figure as build_irregular


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "plots",
        help="Destination folder for the five PNG figures.",
    )
    output_dir = parser.parse_args().output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    builders = {
        "points-and-profile.png": build_points,
        "grid-to-surface.png": build_overview,
        "view-angles.png": build_view_comparison,
        "contour-comparison.png": build_contours,
        "irregular-surface.png": build_irregular,
    }
    with plt.style.context("default"):
        for filename, build in builders.items():
            fig = build()
            try:
                destination = output_dir / filename
                # Keep the full canvas so 3D labels and the figure title are retained.
                fig.savefig(destination, dpi=150)
                print(destination)
            finally:
                plt.close(fig)


if __name__ == "__main__":
    main()
