import numpy as np
import matplotlib.pyplot as plt


rng = np.random.default_rng(42)

hours = np.arange(0, 24, 2)
floor_names = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]

time_pattern = 8 + 7 * np.exp(-((hours - 9) / 3.2) ** 2)
floor_offset = np.array([5, 2, 0, -1])[:, np.newaxis]
noise = rng.normal(0, 1.4, size=(4, hours.size))

pm25 = np.clip(time_pattern + floor_offset + noise, 0, None)

fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    pm25,
    cmap="viridis",
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
    vmin=0,
    vmax=30,
)

colorbar = fig.colorbar(image, ax=ax, pad=0.02)
colorbar.set_label("PM2.5 concentration (µg/m³)")

ax.set(
    title="Indoor PM2.5 by Floor and Time",
    xlabel="Hour",
    ylabel="Building floor",
    xticks=np.arange(0, 25, 4),
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
