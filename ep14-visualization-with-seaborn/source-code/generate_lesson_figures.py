"""Generate seven lesson PNGs off-screen, independent of the working directory."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from relationships import build_scatter_comparison, build_facets
from distributions import build_figure as build_distribution
from category_comparison import build_figure as build_categories
from summary_heatmap import build_figure as build_heatmap
from optional_views import build_patterns, build_pairs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "assets" / "plots")
    output_dir = parser.parse_args().output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    builders = {
        "scatter-groups.png": build_scatter_comparison,
        "cleaning-distribution.png": build_distribution,
        "room-type-comparison.png": build_categories,
        "period-facets.png": lambda: build_facets().figure,
        "mean-time-heatmap.png": build_heatmap,
        "optional-patterns.png": build_patterns,
        "pairwise-views.png": lambda: build_pairs().figure,
    }
    with plt.style.context("default"):
        for filename, build in builders.items():
            fig = build()
            try:
                path = output_dir / filename
                fig.savefig(path, dpi=150)
                print(path)
            finally:
                plt.close(fig)


if __name__ == "__main__":
    main()
