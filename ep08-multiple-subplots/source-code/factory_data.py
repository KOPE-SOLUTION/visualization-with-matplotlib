"""Synthetic production data shared by the EP8 examples."""

import numpy as np


def create_shift_data(seed=8):
    """Return reproducible data for one eight-hour production shift."""
    rng = np.random.default_rng(seed)

    minutes = np.arange(0, 480, 10)
    shift_hour = minutes / 60

    production_cycle = np.sin(
        2 * np.pi * (minutes + 30) / 480
    )

    line_a = (
        90
        + 7 * production_cycle
        + rng.normal(0, 2.0, minutes.size)
    )
    line_b = (
        85
        + 6
        * np.sin(
            2 * np.pi * (minutes + 70) / 480
        )
        + rng.normal(0, 2.2, minutes.size)
    )
    line_c = (
        93
        + 5
        * np.sin(
            2 * np.pi * (minutes + 10) / 480
        )
        + rng.normal(0, 1.8, minutes.size)
    )

    motor_temperature = (
        54
        + 0.032 * minutes
        + 1.8
        * np.sin(
            2 * np.pi * minutes / 180
        )
        + rng.normal(0, 0.6, minutes.size)
    )

    vibration = np.clip(
        1.9
        + 0.0025 * minutes
        + 0.25
        * np.sin(
            2 * np.pi * minutes / 120
        )
        + rng.normal(0, 0.09, minutes.size),
        0,
        None,
    )

    defect_rate = np.clip(
        1.8
        + 0.045 * (motor_temperature - 54)
        + 0.22
        * np.sin(
            2 * np.pi * minutes / 160
        )
        + rng.normal(0, 0.12, minutes.size),
        0,
        None,
    )

    return {
        "minutes": minutes,
        "shift_hour": shift_hour,
        "line_a": line_a,
        "line_b": line_b,
        "line_c": line_c,
        "motor_temperature": motor_temperature,
        "vibration": vibration,
        "defect_rate": defect_rate,
    }
