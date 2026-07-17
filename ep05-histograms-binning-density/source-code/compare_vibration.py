import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
normal_vibration = rng.normal(loc=1.8, scale=0.35, size=1200)
warning_vibration = rng.normal(loc=3.4, scale=0.55, size=700)

histogram_style = {
    "bins": 35,
    "density": True,
    "histtype": "stepfilled",
    "alpha": 0.45,
}

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(
    normal_vibration,
    label="Normal operation",
    color="royalblue",
    **histogram_style,
)
ax.hist(
    warning_vibration,
    label="Warning operation",
    color="tomato",
    **histogram_style,
)
ax.set(
    title="Motor vibration by operating state",
    xlabel="Vibration RMS (mm/s)",
    ylabel="Probability density",
)
ax.legend()
plt.show()
