"""Optional exploration: smoothing, fitted trend, and a two-variable pair grid."""

import matplotlib.pyplot as plt
import seaborn as sns

from housekeeping_data import load_jobs
from plot_helpers import ROOM_ORDER, PALETTE, lesson_theme, label_relationship


def build_patterns():
    jobs = load_jobs()
    with lesson_theme():
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), layout="constrained")
        for bandwidth in [0.5, 1.5]:
            sns.kdeplot(data=jobs, x="cleaning_min", bw_adjust=bandwidth, cut=0,
                        label=f"bw_adjust = {bandwidth}", ax=axes[0])
        axes[0].set(title="KDE: Two Smoothing Settings", xlabel="Cleaning time (min)",
                    ylabel="Estimated density (1/min)")
        axes[0].legend()
        # regplot still uses ci=None; its API differs from barplot(errorbar=None).
        sns.regplot(data=jobs, x="area_m2", y="cleaning_min", ci=None,
                    scatter_kws={"s": 55}, line_kws={"color": "tab:red"}, ax=axes[1])
        axes[1].set_title("Linear Fit to All 18 Jobs")
        label_relationship(axes[1])
        fig.supxlabel("Synthetic data | Exploratory patterns, not causal conclusions", fontsize=9)
    return fig


def build_pairs():
    jobs = load_jobs()
    with lesson_theme():
        g = sns.pairplot(
            jobs, vars=["area_m2", "cleaning_min"], hue="room_type",
            hue_order=ROOM_ORDER, palette=PALETTE, diag_kind="hist", height=2.8,
        )
        g.legend.set_title("Room type")
        labels = {"area_m2": "Room area (m²)", "cleaning_min": "Cleaning time (min)"}
        for ax in g.axes.flat:
            ax.set_xlabel(labels.get(ax.get_xlabel(), ax.get_xlabel()))
            ax.set_ylabel(labels.get(ax.get_ylabel(), ax.get_ylabel()))
        g.figure.subplots_adjust(top=0.88, bottom=0.14)
        g.figure.suptitle("Pairwise Views of the Same Jobs", y=0.98)
        g.figure.supxlabel("Synthetic hotel data | 18 cleaning jobs", fontsize=9)
    return g


if __name__ == "__main__":
    build_patterns()
    build_pairs()
    plt.show()
