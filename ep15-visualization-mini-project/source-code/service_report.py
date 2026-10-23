"""Build and optionally export a daily, four-panel service-center report."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from service_data import load_jobs, summarize_jobs, WAIT_TARGET
from service_plots import plot_intake, plot_service_time, plot_wait_distribution, plot_wait_by_hour

REPORT_STYLE = {
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
}


def summary_note(jobs, wait_target=WAIT_TARGET):
    total_jobs = len(jobs)
    mean_wait = jobs["wait_min"].mean()
    over_target = int((jobs["wait_min"] > wait_target).sum())
    return (
        f"Synthetic data | {total_jobs} jobs | Mean wait: {mean_wait:.1f} min | "
        f"Wait > {wait_target:g} min: {over_target}/{total_jobs}"
    )


def build_dashboard(jobs=None, wait_target=WAIT_TARGET):
    if jobs is None:
        jobs = load_jobs()
    if not np.isfinite(wait_target) or wait_target < 0:
        raise ValueError("wait_target must be a finite, non-negative number.")
    hourly_jobs, mean_service = summarize_jobs(jobs)
    with plt.style.context("default"), plt.rc_context(REPORT_STYLE):
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
        try:
            plot_intake(axes[0, 0], hourly_jobs)
            plot_service_time(axes[0, 1], mean_service)
            plot_wait_distribution(axes[1, 0], jobs, wait_target)
            plot_wait_by_hour(axes[1, 1], jobs, wait_target)
            fig.suptitle("Auto Service Center - Daily Overview", fontsize=17, fontweight="bold")
            fig.supxlabel(summary_note(jobs, wait_target), fontsize=10)
        except Exception:
            plt.close(fig)
            raise
    return fig


def build_individual_figures():
    jobs = load_jobs()
    hourly_jobs, mean_service = summarize_jobs(jobs)
    specifications = [
        ("hourly-intake.png", plot_intake, hourly_jobs),
        ("mean-service-time.png", plot_service_time, mean_service),
        ("wait-distribution.png", plot_wait_distribution, jobs),
        ("wait-by-hour.png", plot_wait_by_hour, jobs),
    ]
    figures = {}
    with plt.style.context("default"), plt.rc_context(REPORT_STYLE):
        for filename, plot, data in specifications:
            fig, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
            plot(ax, data)
            fig.supxlabel("Synthetic auto service data | 24 jobs", fontsize=9)
            figures[filename] = fig
    return figures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="PNG destination; relative paths use the current directory.")
    parser.add_argument("--wait-target", type=float, default=WAIT_TARGET,
                        help="Illustrative waiting-time target in minutes, not an industry standard.")
    parser.add_argument("--no-show", action="store_true", help="Render without opening a plot window.")
    args = parser.parse_args()
    if args.no_show:
        plt.switch_backend("Agg")
    if args.output is not None and args.output.suffix.lower() != ".png":
        parser.error("--output must have a .png extension")
    fig = build_dashboard(wait_target=args.wait_target)
    try:
        print(summary_note(load_jobs(), args.wait_target))
        if args.output is not None:
            output_path = args.output.resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(output_path, dpi=150)
            print(f"Saved: {output_path}")
        if not args.no_show:
            plt.show()
    finally:
        plt.close(fig)


if __name__ == "__main__":
    main()
