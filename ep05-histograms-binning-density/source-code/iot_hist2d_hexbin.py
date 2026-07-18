import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
sample_count = 6000
motor_current = rng.normal(loc=12.0, scale=2.2, size=sample_count)
motor_temperature = (
    24.0
    + 0.75 * motor_current
    + rng.normal(0, 1.5, sample_count)
)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

counts_2d, x_edges, y_edges, image = axes[0].hist2d(
    motor_current,
    motor_temperature,
    bins=35,
    cmap="YlOrRd",
    cmin=1,
)
fig.colorbar(image, ax=axes[0], label="Readings per bin")
axes[0].set(
    title="Two-dimensional histogram",
    xlabel="Motor current (A)",
    ylabel="Motor temperature (°C)",
)

hexagons = axes[1].hexbin(
    motor_current,
    motor_temperature,
    gridsize=35,
    cmap="viridis",
    mincnt=1,
)
fig.colorbar(hexagons, ax=axes[1], label="Readings per hexagon")
axes[1].set(
    title="Hexagonal binning",
    xlabel="Motor current (A)",
    ylabel="Motor temperature (°C)",
)

fig.tight_layout()
plt.show()
