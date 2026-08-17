import matplotlib.pyplot as plt

from factory_data import create_shift_data


data = create_shift_data()
shift_hour = data["shift_hour"]

layout = [
    ["output", "output", "quality"],
    ["temperature", "vibration", "quality"],
]

fig, axes = plt.subplot_mosaic(
    layout,
    figsize=(13, 7),
    width_ratios=[1.2, 1.2, 1],
    layout="constrained",
)

axes["output"].plot(
    shift_hour,
    data["line_a"],
    label="Line A",
)
axes["output"].plot(
    shift_hour,
    data["line_b"],
    label="Line B",
)
axes["output"].plot(
    shift_hour,
    data["line_c"],
    label="Line C",
)
axes["output"].set(
    title="Output Rate",
    xlabel="Shift hour",
    ylabel="Units/min",
)
axes["output"].legend(ncols=3)

axes["temperature"].plot(
    shift_hour,
    data["motor_temperature"],
    color="tab:orange",
)
axes["temperature"].set(
    title="Motor Temperature",
    xlabel="Shift hour",
    ylabel="°C",
)

axes["vibration"].plot(
    shift_hour,
    data["vibration"],
    color="tab:green",
)
axes["vibration"].set(
    title="Vibration",
    xlabel="Shift hour",
    ylabel="mm/s",
)

axes["quality"].plot(
    data["defect_rate"],
    shift_hour,
    color="tab:red",
)
axes["quality"].set(
    title="Quality Trend",
    xlabel="Defect rate (%)",
    ylabel="Shift hour",
)

for ax in axes.values():
    ax.grid(alpha=0.22)

fig.suptitle(
    "Packaging Line Monitoring Mosaic"
)

plt.show()
