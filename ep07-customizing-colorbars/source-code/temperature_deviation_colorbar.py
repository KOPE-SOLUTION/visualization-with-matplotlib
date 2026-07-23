import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm


rng = np.random.default_rng(7)

hours = np.arange(0, 24, 2)
floor_names = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]
target_temperature = 24.0

temperature = (
    target_temperature
    + 2.3 * np.sin((hours - 7) * np.pi / 12)
    + np.array([1.0, 0.4, -0.3, -0.8])[:, np.newaxis]
    + rng.normal(0, 0.35, size=(4, hours.size))
)
deviation = temperature - target_temperature

normalization = TwoSlopeNorm(
    vmin=-4,
    vcenter=0,
    vmax=4,
)

fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    deviation,
    cmap="RdBu_r",
    norm=normalization,
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    ticks=[-4, -2, 0, 2, 4],
    extend="both",
    pad=0.02,
)
colorbar.set_label("Deviation from 24 °C (°C)")

ax.set(
    title="Temperature Deviation from the Target",
    xlabel="Hour",
    ylabel="Building floor",
    xticks=np.arange(0, 25, 4),
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
