import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

rng = np.random.default_rng(42)
normal_temperature = rng.normal(loc=26.0, scale=1.1, size=1800)
hot_cycle = rng.normal(loc=31.5, scale=0.8, size=200)
temperature = np.concatenate([normal_temperature, hot_cycle])

temperature_grid = np.linspace(
    temperature.min() - 1,
    temperature.max() + 1,
    400,
)
temperature_kde = gaussian_kde(temperature)
density_curve = temperature_kde(temperature_grid)

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(
    temperature,
    bins=30,
    density=True,
    color="steelblue",
    alpha=0.35,
    label="Histogram",
)
ax.plot(
    temperature_grid,
    density_curve,
    color="darkorange",
    linewidth=2.5,
    label="KDE",
)
ax.set(
    title="Temperature histogram with KDE",
    xlabel="Temperature (°C)",
    ylabel="Probability density",
)
ax.legend()
plt.show()
