"""Show individual observations, box summaries, and group means together."""

import matplotlib.pyplot as plt
import seaborn as sns

from housekeeping_data import load_jobs
from plot_helpers import ROOM_ORDER, lesson_theme, add_note


def build_figure():
    jobs = load_jobs()
    with lesson_theme():
        fig, axes = plt.subplots(1, 2, figsize=(11, 5), layout="constrained")
        sns.boxplot(data=jobs, x="room_type", y="cleaning_min", order=ROOM_ORDER,
                    color="lightblue", width=0.5, ax=axes[0])
        # Each group has distinct times, so no random horizontal jitter is needed.
        sns.stripplot(data=jobs, x="room_type", y="cleaning_min", order=ROOM_ORDER,
                      color="0.2", jitter=False, size=6, ax=axes[0])
        sns.barplot(data=jobs, x="room_type", y="cleaning_min", order=ROOM_ORDER,
                    errorbar=None, color="tab:blue", ax=axes[1])
        axes[0].set(title="Distribution + Individual Jobs", ylabel="Cleaning time (min)",
                    ylim=(15, 56))
        axes[1].set(title="Mean Cleaning Time", ylabel="Mean time (min)", ylim=(0, 56))
        axes[1].bar_label(axes[1].containers[0], fmt="%.1f", padding=3)
        for ax in axes:
            ax.set_xlabel("Room type")
        add_note(fig)
    return fig


if __name__ == "__main__":
    build_figure()
    plt.show()
