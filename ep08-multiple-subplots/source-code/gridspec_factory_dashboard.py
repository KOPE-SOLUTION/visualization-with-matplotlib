import matplotlib.pyplot as plt

from factory_data import create_shift_data


data = create_shift_data()
shift_hour = data["shift_hour"]

fig = plt.figure(
    figsize=(13, 7.5),
    layout="constrained",
)

grid = fig.add_gridspec(
    2,
    3,
    width_ratios=[1.3, 1.3, 1],
    height_ratios=[1.2, 1],
)

output_ax = fig.add_subplot(grid[0, :2])
summary_ax = fig.add_subplot(grid[0, 2])
temperature_ax = fig.add_subplot(grid[1, 0])
vibration_ax = fig.add_subplot(grid[1, 1])
quality_ax = fig.add_subplot(grid[1, 2])

output_ax.plot(
    shift_hour,
    data["line_a"],
    label="Line A",
)
output_ax.plot(
    shift_hour,
    data["line_b"],
    label="Line B",
)
output_ax.plot(
    shift_hour,
    data["line_c"],
    label="Line C",
)
output_ax.set(
    title="Output Rate During the Shift",
    xlabel="Shift hour",
    ylabel="Units/min",
)
output_ax.legend(ncols=3)

summary_ax.barh(
    ["Line A", "Line B", "Line C"],
    [
        data["line_a"].mean(),
        data["line_b"].mean(),
        data["line_c"].mean(),
    ],
    color=[
        "tab:blue",
        "tab:orange",
        "tab:green",
    ],
)
summary_ax.set(
    title="Average Output",
    xlabel="Units/min",
)

temperature_ax.plot(
    shift_hour,
    data["motor_temperature"],
    color="tab:orange",
)
temperature_ax.set(
    title="Motor Temperature",
    xlabel="Shift hour",
    ylabel="°C",
)

vibration_ax.plot(
    shift_hour,
    data["vibration"],
    color="tab:green",
)
vibration_ax.set(
    title="Vibration",
    xlabel="Shift hour",
    ylabel="mm/s",
)

quality_ax.plot(
    shift_hour,
    data["defect_rate"],
    color="tab:red",
)
quality_ax.set(
    title="Defect Rate",
    xlabel="Shift hour",
    ylabel="%",
)

for ax in fig.axes:
    ax.grid(alpha=0.22)

fig.suptitle(
    "Packaging Factory — Shift Overview"
)

plt.show()
