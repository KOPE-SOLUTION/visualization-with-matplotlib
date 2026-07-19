import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


sensor_x = np.array([1.0, 2.8, 4.5, 6.2, 8.2, 9.0])
sensor_y = np.array([1.2, 4.0, 2.0, 4.5, 1.3, 3.6])
soil_moisture = np.array([41, 55, 48, 63, 36, 58])
coverage_m2 = np.array([20, 40, 30, 50, 20, 40])

size_scale = 7
point_sizes = coverage_m2 * size_scale

fig, ax = plt.subplots(figsize=(10, 5.8))

points = ax.scatter(
    sensor_x,
    sensor_y,
    s=point_sizes,
    c=soil_moisture,
    cmap="YlGnBu",
    vmin=30,
    vmax=70,
    edgecolor="black",
    linewidth=0.8,
    alpha=0.85,
)

for index, (x_value, y_value) in enumerate(zip(sensor_x, sensor_y), start=1):
    ax.annotate(
        f"S{index}",
        (x_value, y_value),
        xytext=(0, 9),
        textcoords="offset points",
        ha="center",
    )

size_handles = [
    Line2D(
        [],
        [],
        marker="o",
        linestyle="none",
        markersize=np.sqrt(area * size_scale),
        markerfacecolor="lightgray",
        markeredgecolor="black",
        alpha=0.85,
        label=f"{area} m²",
    )
    for area in [20, 35, 50]
]

ax.legend(
    handles=size_handles,
    title="Coverage area",
    loc="upper left",
    framealpha=0.95,
)

colorbar = fig.colorbar(points, ax=ax, pad=0.02)
colorbar.set_label("Soil moisture (%)")

ax.set(
    title="Smart Farm Sensor Coverage",
    xlabel="Field X position (m)",
    ylabel="Field Y position (m)",
    xlim=(0, 10),
    ylim=(0, 5.5),
)
ax.set_aspect("equal")
ax.grid(alpha=0.2)

fig.tight_layout()
plt.show()
