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

fig, ax = plt.subplots(figsize=(8, 6))
lines = ax.contour(
    X,
    Y,
    temperature,
    levels=np.arange(22, 34, 1),
    colors="black",
    linewidths=0.8,
)
ax.clabel(lines, inline=True, fontsize=8, fmt="%.0f °C")

ax.scatter(
    sensor_positions[:, 0],
    sensor_positions[:, 1],
    color="white",
    edgecolor="black",
    s=55,
    label="Temperature sensors",
)

ax.set(
    title="Temperature contour in a machine room",
    xlabel="Room width (m)",
    ylabel="Room height (m)",
    xlim=(0, 10),
    ylim=(0, 8),
    aspect="equal",
)
ax.legend()
plt.show()
