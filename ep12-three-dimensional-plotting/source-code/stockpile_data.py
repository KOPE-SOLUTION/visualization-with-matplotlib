"""Small synthetic stockpile surveys in metres; not engineering measurements."""

import numpy as np


def load_grid():
    """Return x positions, y positions, and heights indexed by [y row, x column]."""
    x = np.array([0, 5, 10, 15, 20])
    y = np.array([0, 5, 10, 15])
    height = np.array([
        [0.3, 0.8, 1.2, 0.9, 0.2],
        [0.6, 3.4, 6.2, 3.9, 0.5],
        [0.5, 4.1, 7.5, 4.6, 0.6],
        [0.2, 0.7, 1.0, 0.6, 0.2],
    ])
    return x, y, height


def load_profile():
    """Return five points along y = 5 m, ordered by increasing x."""
    x, y, height = load_grid()
    return x, np.full(x.size, y[1]), height[1].copy()


def load_irregular():
    """Return a separate synthetic survey with irregular XY positions."""
    x = np.array([0, 6, 13, 20, 2, 9, 17, 0, 7, 12, 20])
    y = np.array([0, 1, 0, 0, 6, 5, 7, 15, 13, 10, 15])
    height = np.array([0.3, 1.0, 1.1, 0.2, 1.2, 5.8, 2.7, 0.2, 2.5, 6.8, 0.2])
    return x, y, height
