import matplotlib.pyplot as plt

from factory_data import create_shift_data


data = create_shift_data()
shift_hour = data["shift_hour"]

fig, axes = plt.subplots(
    2,
    2,
    figsize=(11, 7),
    sharex=True,
    layout="constrained",
)

series = [
    (
        data["line_a"],
        "Line A Output Rate",
        "Output rate (units/min)",
        "tab:blue",
    ),
    (
        data["motor_temperature"],
        "Motor Temperature",
        "Temperature (°C)",
        "tab:orange",
    ),
    (
        data["vibration"],
        "Motor Vibration",
        "Vibration (mm/s)",
        "tab:green",
    ),
    (
        data["defect_rate"],
        "Defect Rate",
        "Defect rate (%)",
        "tab:red",
    ),
]

for ax, (values, title, ylabel, color) in zip(
    axes.flat,
    series,
):
    ax.plot(
        shift_hour,
        values,
        color=color,
        linewidth=2,
    )
    ax.set(
        title=title,
        ylabel=ylabel,
    )
    ax.grid(alpha=0.25)

for ax in axes[-1, :]:
    ax.set_xlabel("Shift hour")

fig.suptitle(
    "Packaging Line A — Shift Monitoring"
)

plt.show()
