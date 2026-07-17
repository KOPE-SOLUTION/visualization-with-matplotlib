import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
normal_temperature = rng.normal(loc=26.0, scale=1.1, size=1800)
hot_cycle = rng.normal(loc=31.5, scale=0.8, size=200)
temperature = np.concatenate([normal_temperature, hot_cycle])

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(
    temperature,
    bins=30,
    color="royalblue",
    edgecolor="white",
)
ax.set(
    title="Machine-room temperature distribution",
    xlabel="Temperature (°C)",
    ylabel="Number of readings",
)
ax.grid(axis="y", alpha=0.25)
plt.show()
