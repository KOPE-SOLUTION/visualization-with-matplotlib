"""Fictional telecom sites and a single synthetic network snapshot."""

import numpy as np


def load_sites():
    """Return fresh arrays, ordered by site: name, lon, lat, users, traffic."""
    names = np.array(["Site A", "Site B", "Site C", "Site D", "Site E", "Site F"])
    longitude = np.array([99.2, 100.6, 102.4, 100.1, 101.3, 102.3])
    latitude = np.array([16.8, 16.3, 16.4, 14.5, 14.1, 13.2])
    connected_users = np.array([120, 240, 180, 360, 300, 150])
    traffic_mbps = np.array([180, 420, 310, 680, 540, 260])
    return names, longitude, latitude, connected_users, traffic_mbps
