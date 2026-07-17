import numpy as np
import matplotlib.pyplot as plt


def make_temperature_field(x, y):
    room_temperature = 26.0
    machine_heat = 6.0 * np.exp(
        -(((x - 7.5) ** 2) / 2.0 + ((y - 2.0) ** 2) / 1.5)
    )
    air_conditioner = 4.0 * np.exp(
        -(((x - 1.0) ** 2) / 3.0 + ((y - 6.5) ** 2) / 2.0)
    )
    airflow = 0.4 * np.sin(np.pi * x / 5) * np.cos(np.pi * y / 4)
    return room_temperature + machine_heat - air_conditioner + airflow


x = np.linspace(0, 10, 200)
y = np.linspace(0, 8, 160)
X, Y = np.meshgrid(x, y)
temperature = make_temperature_field(X, Y)

sensor_positions = np.array([
    [1.0, 1.0],
    [3.0, 2.0],
    [5.0, 1.0],
    [8.0, 1.0],
    [2.0, 4.0],
    [5.0, 4.0],
    [8.0, 4.0],
    [1.0, 7.0],
    [4.0, 7.0],
    [7.0, 7.0],
    [9.0, 7.0],
])

rng = np.random.default_rng(42)
sensor_values = make_temperature_field(
    sensor_positions[:, 0],
    sensor_positions[:, 1],
)
sensor_values += rng.normal(0, 0.15, len(sensor_positions))

fig, ax = plt.subplots(figsize=(9, 6))
image = ax.imshow(
    temperature,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin="lower",
    cmap="coolwarm",
    vmin=22,
    vmax=34,
    aspect="equal",
)

lines = ax.contour(
    X,
    Y,
    temperature,
    levels=[24, 26, 28, 30, 32],
    colors="black",
    linewidths=0.8,
)
ax.clabel(lines, inline=True, fontsize=8, fmt="%.0f °C")

ax.scatter(
    sensor_positions[:, 0],
    sensor_positions[:, 1],
    color="white",
    edgecolor="black",
    s=65,
)

for index, ((sensor_x, sensor_y), value) in enumerate(
    zip(sensor_positions, sensor_values),
    start=1,
):
    ax.annotate(
        f"T{index}: {value:.1f}",
        (sensor_x, sensor_y),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=7,
    )

fig.colorbar(image, ax=ax, label="Temperature (°C)")
ax.set(
    title="IoT temperature monitoring",
    xlabel="Room width (m)",
    ylabel="Room height (m)",
    xlim=(0, 10),
    ylim=(0, 8),
)
plt.show()
