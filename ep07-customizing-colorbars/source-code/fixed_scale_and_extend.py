import numpy as np
import matplotlib.pyplot as plt


rng = np.random.default_rng(42)

hours = np.arange(0, 24, 2)
floor_names = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]

time_pattern = 8 + 7 * np.exp(-((hours - 9) / 3.2) ** 2)
floor_offset = np.array([5, 2, 0, -1])[:, np.newaxis]
pm25 = np.clip(
    time_pattern
    + floor_offset
    + rng.normal(0, 1.4, size=(4, hours.size)),
    0,
    None,
)

# Simulate a short pollution event above the displayed scale.
pm25[0, 5] = 72
pm25[1, 5] = 58

pm25_cmap = plt.get_cmap("viridis").with_extremes(
    over="crimson",
)

fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    pm25,
    cmap=pm25_cmap,
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
    vmin=0,
    vmax=50,
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    extend="max",
    pad=0.02,
    ticks=np.arange(0, 51, 10),
)
colorbar.set_label("PM2.5 concentration (µg/m³)")

ax.set(
    title="PM2.5 with a Fixed Color Scale",
    xlabel="Hour",
    ylabel="Building floor",
    xticks=np.arange(0, 25, 4),
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
