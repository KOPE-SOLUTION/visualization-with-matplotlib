import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


hours = np.arange(0, 24)
temperature_a = 25 + 4 * np.sin((hours - 7) * np.pi / 12)
temperature_b = 24 + 3 * np.sin((hours - 6) * np.pi / 12)

fig, ax = plt.subplots(figsize=(10, 5.5))

line_a, = ax.plot(
    hours,
    temperature_a,
    color="forestgreen",
    linewidth=2.5,
    label="Greenhouse A",
)
line_b, = ax.plot(
    hours,
    temperature_b,
    color="royalblue",
    linewidth=2.5,
    label="Greenhouse B",
)

ax.axhspan(18, 30, color="mediumseagreen", alpha=0.12)
ax.axhspan(30, 35, color="gold", alpha=0.15)
ax.axhline(30, color="darkorange", linestyle="--", linewidth=1.8)

sensor_legend = ax.legend(
    handles=[line_a, line_b],
    title="Temperature sensor",
    loc="upper left",
)
ax.add_artist(sensor_legend)

status_handles = [
    Patch(
        facecolor="mediumseagreen",
        alpha=0.35,
        label="Target: 18–30 °C",
    ),
    Line2D(
        [],
        [],
        color="darkorange",
        linestyle="--",
        linewidth=1.8,
        label="Warning threshold",
    ),
]
ax.legend(
    handles=status_handles,
    title="Operating status",
    loc="upper right",
)

ax.set(
    title="Greenhouse Temperature and Operating Status",
    xlabel="Hour",
    ylabel="Temperature (°C)",
    xlim=(0, 23),
    ylim=(16, 35),
)
ax.grid(alpha=0.25)

fig.tight_layout()
plt.show()
