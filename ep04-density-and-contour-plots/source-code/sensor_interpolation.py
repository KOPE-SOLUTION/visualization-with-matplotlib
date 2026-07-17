import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


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


def format_room_axes(ax, title):
    ax.set(
        title=title,
        xlabel="Room width (m)",
        ylabel="Room height (m)",
        xlim=(0, 10),
        ylim=(0, 8),
        aspect="equal",
    )


x = np.linspace(0, 10, 200)
y = np.linspace(0, 8, 160)
X, Y = np.meshgrid(x, y)
true_temperature = make_temperature_field(X, Y)

sensor_positions = np.array([
    [1, 1], [3, 2], [5, 1], [8, 1],
    [2, 4], [5, 4], [8, 4],
    [1, 7], [4, 7], [7, 7], [9, 7],
])
sensor_x = sensor_positions[:, 0]
sensor_y = sensor_positions[:, 1]

rng = np.random.default_rng(42)
true_sensor_values = make_temperature_field(sensor_x, sensor_y)
measurement_noise = rng.normal(0, 0.15, len(sensor_positions))
sensor_values = true_sensor_values + measurement_noise

interpolated_temperature = griddata(
    points=sensor_positions,
    values=sensor_values,
    xi=(X, Y),
    method="linear",
)
interpolated_temperature = np.ma.masked_invalid(interpolated_temperature)

fig, ax = plt.subplots(figsize=(8, 6))
filled = ax.contourf(
    X,
    Y,
    interpolated_temperature,
    levels=np.arange(22, 34.5, 0.5),
    cmap="coolwarm",
    extend="both",
)
ax.scatter(
    sensor_x,
    sensor_y,
    c=sensor_values,
    cmap="coolwarm",
    vmin=22,
    vmax=34,
    edgecolor="black",
    s=80,
    label="Measured locations",
)
fig.colorbar(filled, ax=ax, label="Estimated temperature (°C)")
format_room_axes(ax, "Temperature estimated from IoT sensors")
ax.legend()
plt.show()

valid_area = ~interpolated_temperature.mask
mean_absolute_error = np.mean(
    np.abs(
        interpolated_temperature.data[valid_area]
        - true_temperature[valid_area]
    )
)
print(f"Interpolation MAE: {mean_absolute_error:.2f} °C")
