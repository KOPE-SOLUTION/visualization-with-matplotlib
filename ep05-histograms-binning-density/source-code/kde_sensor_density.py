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

kde_narrow = gaussian_kde(
    temperature,
    bw_method=0.12,
)
kde_default = gaussian_kde(temperature)
kde_wide = gaussian_kde(
    temperature,
    bw_method=0.50,
)

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

axes[0].hist(
    temperature,
    bins=30,
    density=True,
    color="steelblue",
    alpha=0.35,
    label="Histogram",
)
axes[0].plot(
    temperature_grid,
    kde_default(temperature_grid),
    color="darkorange",
    linewidth=2.5,
    label="Default KDE",
)
axes[0].set(
    title="Temperature histogram with KDE",
    xlabel="Temperature (°C)",
    ylabel="Probability density (1/°C)",
)
axes[0].legend()

axes[1].hist(
    temperature,
    bins=30,
    density=True,
    color="lightgray",
    alpha=0.45,
    label="Histogram",
)
axes[1].plot(
    temperature_grid,
    kde_narrow(temperature_grid),
    linewidth=2,
    label="Narrow bandwidth (0.12)",
)
axes[1].plot(
    temperature_grid,
    kde_default(temperature_grid),
    linewidth=2.5,
    label="Default bandwidth",
)
axes[1].plot(
    temperature_grid,
    kde_wide(temperature_grid),
    linewidth=2,
    label="Wide bandwidth (0.50)",
)
axes[1].set(
    title="Effect of KDE bandwidth",
    xlabel="Temperature (°C)",
)
axes[1].legend()

fig.tight_layout()
plt.show()
