"""Create the four lesson PNGs using an off-screen renderer."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from site_locations import build_figure as build_locations
from network_report import build_figure as build_report
from map_extent import build_figure as build_extent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "plots",
        help="Folder for the four PNG figures.",
    )
    output_dir = parser.parse_args().output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    builders = {
        "site-locations.png": build_locations,
        "traffic-map.png": lambda: build_report(show_users=False),
        "network-report.png": build_report,
        "map-extent.png": build_extent,
    }
    with plt.style.context("default"):
        for filename, build in builders.items():
            fig = build()
            try:
                destination = output_dir / filename
                fig.savefig(destination, dpi=150)
                print(destination)
            finally:
                plt.close(fig)


if __name__ == "__main__":
    main()
