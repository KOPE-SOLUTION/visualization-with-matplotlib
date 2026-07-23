import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap


rng = np.random.default_rng(42)

hours = np.arange(0, 24, 2)
floor_names = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]

time_pattern = 8 + 18 * np.exp(-((hours - 9) / 3.2) ** 2)
floor_offset = np.array([12, 6, 2, 0])[:, np.newaxis]
pm25 = np.clip(
    time_pattern
    + floor_offset
    + rng.normal(0, 2.0, size=(4, hours.size)),
    0,
    74.9,
)

# Example bands for this lesson, not official health thresholds.
boundaries = [0, 15, 25, 37.5, 50, 75]
status_labels = ["Very low", "Low", "Moderate", "High", "Very high"]
status_colors = [
    "#2c7bb6",
    "#abd9e9",
    "#ffffbf",
    "#fdae61",
    "#d7191c",
]

status_cmap = ListedColormap(status_colors)
status_norm = BoundaryNorm(
    boundaries,
    ncolors=status_cmap.N,
    clip=True,
)
tick_positions = [
    (lower + upper) / 2
    for lower, upper in zip(boundaries[:-1], boundaries[1:])
]

fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    pm25,
    cmap=status_cmap,
    norm=status_norm,
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    boundaries=boundaries,
    ticks=tick_positions,
    spacing="proportional",
    pad=0.02,
)
colorbar.ax.set_yticklabels(status_labels)
colorbar.set_label("Building-specific PM2.5 status")

ax.set(
    title="Discrete Indoor Air Quality Status",
    xlabel="Hour",
    ylabel="Building floor",
    xticks=np.arange(0, 25, 4),
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
