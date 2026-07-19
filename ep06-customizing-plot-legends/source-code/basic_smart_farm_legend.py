import numpy as np
import matplotlib.pyplot as plt


hours = np.arange(0, 24)

greenhouse_a = 25 + 4 * np.sin((hours - 7) * np.pi / 12)
greenhouse_b = 24 + 3 * np.sin((hours - 6) * np.pi / 12)
outdoor = 27 + 6 * np.sin((hours - 8) * np.pi / 12)

fig, ax = plt.subplots(figsize=(10, 5.5))

ax.plot(
    hours,
    greenhouse_a,
    color="forestgreen",
    linewidth=2.5,
    label="Greenhouse A",
)
ax.plot(
    hours,
    greenhouse_b,
    color="royalblue",
    linewidth=2.5,
    linestyle="--",
    label="Greenhouse B",
)
ax.plot(
    hours,
    outdoor,
    color="darkorange",
    linewidth=2,
    linestyle=":",
    label="Outdoor sensor",
)

ax.set(
    title="Smart Farm Temperature Monitoring",
    xlabel="Hour",
    ylabel="Temperature (°C)",
    xlim=(0, 23),
)
ax.grid(alpha=0.25)

ax.legend(
    loc="upper left",
    ncols=1,
    title="Sensor location",
    frameon=True,
    fancybox=True,
    framealpha=0.9,
    borderpad=0.8,
)

fig.tight_layout()
plt.show()
