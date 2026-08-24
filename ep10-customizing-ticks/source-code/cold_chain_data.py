"""Synthetic cold-chain logistics data shared by the EP10 examples."""

import numpy as np


def create_cold_chain_day(seed=10):
    """Return reproducible sensor data for one synthetic operating day."""
    rng = np.random.default_rng(seed)

    hours = np.arange(0, 24.01, 0.25)

    ambient_temperature = (
        29
        + 5 * np.sin(2 * np.pi * (hours - 8) / 24)
        + rng.normal(0, 0.35, hours.size)
    )

    cold_room_temperature = (
        -20
        + 0.18 * np.sin(2 * np.pi * hours / 6)
        + rng.normal(0, 0.12, hours.size)
    )

    door_open = (
        (hours >= 10.0)
        & (hours <= 10.75)
    )
    cold_room_temperature[door_open] += np.linspace(
        0.5,
        2.2,
        door_open.sum(),
    )

    recovery = (
        (hours > 10.75)
        & (hours <= 12.0)
    )
    cold_room_temperature[recovery] += np.linspace(
        1.8,
        0,
        recovery.sum(),
    )

    compressor_load = np.clip(
        48
        + 9 * (cold_room_temperature + 20)
        + 5 * np.sin(2 * np.pi * hours / 4)
        + rng.normal(0, 2.0, hours.size),
        20,
        100,
    )

    relative_humidity = np.clip(
        72
        + 2.5 * np.sin(2 * np.pi * (hours + 1) / 8)
        + 5 * door_open.astype(float)
        + rng.normal(0, 0.8, hours.size),
        55,
        90,
    )

    return {
        "hours": hours,
        "ambient_temperature": ambient_temperature,
        "cold_room_temperature": cold_room_temperature,
        "compressor_load": compressor_load,
        "relative_humidity": relative_humidity,
        "door_open": door_open,
    }

