"""Shared category order and temporary plot styling."""

from contextlib import contextmanager

import matplotlib.pyplot as plt
import seaborn as sns

ROOM_ORDER = ["Standard", "Deluxe", "Suite"]
PERIOD_ORDER = ["Morning", "Afternoon"]
PALETTE = {"Standard": "tab:blue", "Deluxe": "tab:orange", "Suite": "tab:green"}
TIME_BINS = [20, 25, 30, 35, 40, 45, 50, 55]


@contextmanager
def lesson_theme():
    """Apply Seaborn styling without changing the caller's lasting rcParams."""
    with plt.rc_context():
        sns.set_theme(style="whitegrid")
        yield


def label_relationship(ax):
    ax.set(xlabel="Room area (m²)", ylabel="Cleaning time (min)",
           xlim=(18, 47), ylim=(18, 56))


def add_note(fig):
    fig.supxlabel("Synthetic hotel data | 18 cleaning jobs", fontsize=9)
