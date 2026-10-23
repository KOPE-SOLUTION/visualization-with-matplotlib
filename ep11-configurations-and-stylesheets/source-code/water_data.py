"""Small synthetic daily-volume dataset for a water utility."""

import numpy as np


def create_water_week():
    """Return days, produced volume, and distributed volume in m³/day."""
    days = np.arange(1, 8)
    produced = np.array([4100, 4250, 4180, 4460, 4520, 4300, 4400])
    distributed = np.array([3900, 4020, 4050, 4250, 4310, 4120, 4210])
    return days, produced, distributed
