"""Synthetic check-in records for one day at an auto service center."""

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

HOURS = list(range(8, 16))
SERVICE_ORDER = ["Inspection", "Oil change", "Tire service"]
SERVICE_COLORS = {
    "Inspection": "tab:blue",
    "Oil change": "tab:orange",
    "Tire service": "tab:green",
}
WAIT_TARGET = 20
WAIT_BINS = [0, 10, 20, 30, 40, 50]


def load_jobs():
    """Return a fresh table; each row is one completed service job, not one hour."""
    records = [
        ("J01", 8, "Inspection", 5, 20),
        ("J02", 8, "Oil change", 8, 35),
        ("J03", 9, "Tire service", 10, 55),
        ("J04", 9, "Inspection", 12, 25),
        ("J05", 9, "Oil change", 15, 40),
        ("J06", 10, "Inspection", 20, 30),
        ("J07", 10, "Oil change", 25, 45),
        ("J08", 10, "Tire service", 30, 60),
        ("J09", 10, "Inspection", 18, 25),
        ("J10", 11, "Oil change", 22, 40),
        ("J11", 11, "Tire service", 28, 65),
        ("J12", 11, "Inspection", 24, 30),
        ("J13", 12, "Tire service", 32, 60),
        ("J14", 12, "Inspection", 38, 33),
        ("J15", 12, "Oil change", 45, 48),
        ("J16", 12, "Tire service", 35, 68),
        ("J17", 13, "Inspection", 25, 25),
        ("J18", 13, "Oil change", 30, 45),
        ("J19", 13, "Tire service", 28, 65),
        ("J20", 14, "Oil change", 18, 35),
        ("J21", 14, "Inspection", 15, 20),
        ("J22", 15, "Tire service", 12, 55),
        ("J23", 15, "Oil change", 10, 40),
        ("J24", 15, "Tire service", 8, 60),
    ]
    jobs = pd.DataFrame(records, columns=[
        "job_id", "hour", "service_type", "wait_min", "service_min",
    ])
    validate_jobs(jobs)
    return jobs


def validate_jobs(jobs):
    """Reject malformed input rather than silently dropping records in plots."""
    required = ["job_id", "hour", "service_type", "wait_min", "service_min"]
    if not all(column in jobs.columns for column in required):
        raise ValueError(f"Required columns: {required}")
    if jobs.empty or jobs[required].isna().any().any():
        raise ValueError("Jobs must be non-empty and have no missing required values.")
    if not jobs["job_id"].is_unique:
        raise ValueError("job_id must be unique.")
    numeric = ["hour", "wait_min", "service_min"]
    if not all(is_numeric_dtype(jobs[column]) for column in numeric):
        raise ValueError("hour, wait_min and service_min must be numeric.")
    if not np.isfinite(jobs[numeric].to_numpy()).all():
        raise ValueError("Numeric values must be finite.")
    if not jobs["hour"].isin(HOURS).all():
        raise ValueError("hour must be one of the supported hourly buckets in HOURS.")
    if not jobs["service_type"].isin(SERVICE_ORDER).all():
        raise ValueError("Unknown service_type; update SERVICE_ORDER and SERVICE_COLORS.")
    if (jobs["wait_min"] < 0).any() or (jobs["service_min"] <= 0).any():
        raise ValueError("Waiting time must be non-negative; service time must be positive.")


def summarize_jobs(jobs):
    validate_jobs(jobs)
    hourly_jobs = jobs.groupby("hour").size().reindex(HOURS, fill_value=0)
    mean_service = jobs.groupby("service_type")["service_min"].mean().reindex(SERVICE_ORDER)
    return hourly_jobs, mean_service
