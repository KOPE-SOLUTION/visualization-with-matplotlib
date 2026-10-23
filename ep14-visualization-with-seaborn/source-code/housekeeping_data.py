"""Small, fictional hotel housekeeping dataset; one row is one cleaning job."""

import pandas as pd


def load_jobs():
    """Return a new DataFrame with 18 jobs, without network access or randomness."""
    records = [
        ("Standard", "Morning", 20, 22),
        ("Standard", "Morning", 22, 24),
        ("Standard", "Morning", 24, 26),
        ("Standard", "Afternoon", 21, 25),
        ("Standard", "Afternoon", 23, 29),
        ("Standard", "Afternoon", 25, 30),
        ("Deluxe", "Morning", 28, 30),
        ("Deluxe", "Morning", 30, 34),
        ("Deluxe", "Morning", 32, 32),
        ("Deluxe", "Afternoon", 29, 33),
        ("Deluxe", "Afternoon", 31, 37),
        ("Deluxe", "Afternoon", 33, 38),
        ("Suite", "Morning", 40, 42),
        ("Suite", "Morning", 42, 46),
        ("Suite", "Morning", 44, 44),
        ("Suite", "Afternoon", 41, 45),
        ("Suite", "Afternoon", 43, 50),
        ("Suite", "Afternoon", 45, 52),
    ]
    return pd.DataFrame(records, columns=[
        "room_type", "period", "area_m2", "cleaning_min",
    ])
