"""Compare a plain scatter plot, semantic grouping, and period facets."""

import matplotlib.pyplot as plt
import seaborn as sns

from housekeeping_data import load_jobs
from plot_helpers import ROOM_ORDER, PERIOD_ORDER, PALETTE, lesson_theme, label_relationship, add_note


def build_scatter_comparison():
    jobs = load_jobs()
    with lesson_theme():
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharex=True, sharey=True,
                                 layout="constrained")
        sns.scatterplot(data=jobs, x="area_m2", y="cleaning_min",
                        color="tab:blue", s=85, ax=axes[0])
        sns.scatterplot(data=jobs, x="area_m2", y="cleaning_min",
                        hue="room_type", hue_order=ROOM_ORDER, palette=PALETTE,
                        s=85, ax=axes[1])
        axes[0].set_title("One color for all jobs")
        axes[1].set_title("hue = room_type")
        axes[1].legend(title="Room type", loc="upper left")
        for ax in axes:
            label_relationship(ax)
        add_note(fig)
    return fig


def build_facets():
    jobs = load_jobs()
    with lesson_theme():
        # relplot creates and owns its Figure; there is no plt.subplots() here.
        g = sns.relplot(
            data=jobs, x="area_m2", y="cleaning_min",
            hue="room_type", hue_order=ROOM_ORDER, palette=PALETTE,
            col="period", col_order=PERIOD_ORDER, kind="scatter",
            s=85, height=4.5, aspect=1.05,
        )
        g.set_axis_labels("Room area (m²)", "Cleaning time (min)")
        g.set_titles("{col_name}")
        g.set(xlim=(18, 47), ylim=(18, 56))
        g.legend.set_title("Room type")
        g.figure.subplots_adjust(top=0.82, bottom=0.18)
        g.figure.suptitle("Hotel Housekeeping - Compare Periods", y=0.98)
        g.figure.supxlabel("Synthetic data | 9 jobs in each period", fontsize=9)
    return g


if __name__ == "__main__":
    build_scatter_comparison()
    build_facets()
    plt.show()
