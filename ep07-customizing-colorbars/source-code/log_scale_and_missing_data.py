import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import FuncFormatter


particle_count = np.array(
    [
        [18, 25, 60, 450, 1200, 95, 35, 20],
        [12, 19, 45, 300, np.nan, 70, 28, 16],
        [8, 15, 32, 180, 6500, 55, 22, 11],
    ],
    dtype=float,
)

masked_count = np.ma.masked_invalid(particle_count)
particle_cmap = plt.get_cmap("magma").with_extremes(
    bad="lightgray",
    over="cyan",
)

fig, ax = plt.subplots(figsize=(9, 4.8))

image = ax.imshow(
    masked_count,
    cmap=particle_cmap,
    norm=LogNorm(vmin=10, vmax=5000),
    aspect="auto",
    origin="lower",
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    extend="max",
    ticks=[10, 100, 1000, 5000],
    pad=0.02,
)
colorbar.ax.yaxis.set_major_formatter(
    FuncFormatter(lambda value, position: f"{value:,.0f}")
)
colorbar.set_label("Particle count (particles/L)")

ax.set(
    title="Particle Count with Logarithmic Color Scaling",
    xlabel="Measurement window",
    ylabel="Sensor node",
    yticks=[0, 1, 2],
    yticklabels=["AQ-01", "AQ-02", "AQ-03"],
)

fig.tight_layout()
plt.show()
