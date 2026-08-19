"""Synthetic solar-farm data shared by the EP9 examples."""

import numpy as np


def create_solar_day(seed=9):
    """Return reproducible operating data for one synthetic solar day."""
    rng = np.random.default_rng(seed)

    hours = np.arange(5.5, 18.5 + 1 / 60, 1 / 6)
    sunrise = 5.75
    sunset = 18.25

    daylight_phase = np.clip(
        (hours - sunrise) / (sunset - sunrise),
        0,
        1,
    )
    solar_shape = np.sin(np.pi * daylight_phase) ** 1.45
    clear_sky_power = 5200 * solar_shape

    morning_cloud = 0.28 * np.exp(
        -((hours - 9.1) / 0.35) ** 2
    )
    afternoon_cloud = 0.42 * np.exp(
        -((hours - 14.3) / 0.45) ** 2
    )
    cloud_factor = np.clip(
        1 - morning_cloud - afternoon_cloud,
        0.35,
        1,
    )

    maintenance_mask = (
        (hours >= 12.0)
        & (hours <= 12.4)
    )
    operating_factor = np.ones(hours.size)
    operating_factor[maintenance_mask] = 0.68

    ac_power = np.clip(
        clear_sky_power
        * cloud_factor
        * operating_factor
        + rng.normal(0, 55, hours.size) * solar_shape,
        0,
        None,
    )

    irradiance = np.clip(
        980 * solar_shape * cloud_factor
        + rng.normal(0, 14, hours.size),
        0,
        None,
    )

    ambient_temperature = (
        24
        + 10 * solar_shape
        + rng.normal(0, 0.35, hours.size)
    )
    inverter_temperature = (
        ambient_temperature
        + 7
        + 8 * ac_power / 5200
        + rng.normal(0, 0.45, hours.size)
    )

    energy_kwh = np.cumsum(ac_power) * (10 / 60)

    return {
        "hours": hours,
        "clear_sky_power": clear_sky_power,
        "ac_power": ac_power,
        "irradiance": irradiance,
        "ambient_temperature": ambient_temperature,
        "inverter_temperature": inverter_temperature,
        "maintenance_mask": maintenance_mask,
        "energy_kwh": energy_kwh,
    }


def nearest_index(values, target):
    """Return the index of the value nearest to target."""
    return int(np.abs(values - target).argmin())
