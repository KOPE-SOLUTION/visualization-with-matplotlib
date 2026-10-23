"""Count cleaning jobs within explicit five-minute bins."""

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

from housekeeping_data import load_jobs
from plot_helpers import TIME_BINS, lesson_theme, add_note


def build_figure():
    jobs = load_jobs()
    with lesson_theme():
        fig, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
        sns.histplot(data=jobs, x="cleaning_min", bins=TIME_BINS,
                     color="tab:blue", edgecolor="white", ax=ax)
        ax.set(title="Distribution of Cleaning Time", xlabel="Cleaning time (min)",
               ylabel="Number of jobs", xticks=TIME_BINS, xlim=(20, 55))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        add_note(fig)
    return fig


if __name__ == "__main__":
    build_figure()
    plt.show()
