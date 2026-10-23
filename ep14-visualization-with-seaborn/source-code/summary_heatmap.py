"""Summarize mean time by room type and period, then display that table."""

import matplotlib.pyplot as plt
import seaborn as sns

from housekeeping_data import load_jobs
from plot_helpers import ROOM_ORDER, PERIOD_ORDER, lesson_theme


def make_summary(jobs):
    return jobs.pivot_table(
        index="room_type", columns="period", values="cleaning_min", aggfunc="mean",
    ).reindex(index=ROOM_ORDER, columns=PERIOD_ORDER)


def build_figure():
    summary = make_summary(load_jobs())
    with lesson_theme():
        fig, ax = plt.subplots(figsize=(7.5, 4.8), layout="constrained")
        sns.heatmap(summary, annot=True, fmt=".1f", cmap="YlGnBu", vmin=20, vmax=55,
                    linewidths=1, cbar_kws={"label": "Mean time (min)"}, ax=ax)
        ax.set(title="Mean Cleaning Time by Room Type and Period",
               xlabel="Period", ylabel="Room type")
        ax.tick_params(axis="y", labelrotation=0)
        fig.supxlabel("Synthetic data | 3 jobs per cell", fontsize=9)
    return fig


if __name__ == "__main__":
    build_figure()
    plt.show()
