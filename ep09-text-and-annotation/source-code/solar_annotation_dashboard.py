import matplotlib.pyplot as plt

from solar_data import create_solar_day, nearest_index


data = create_solar_day()
hours = data["hours"]

fig, axes = plt.subplots(
    2,
    1,
    figsize=(11, 7),
    sharex=True,
    layout="constrained",
)

power_ax, temperature_ax = axes

power_ax.plot(
    hours,
    data["clear_sky_power"],
    color="0.65",
    linestyle="--",
    label="Clear-sky reference",
)
power_ax.plot(
    hours,
    data["ac_power"],
    color="tab:orange",
    linewidth=2.2,
    label="AC power",
)

for ax in axes:
    ax.axvspan(
        12.0,
        12.4,
        color="tab:red",
        alpha=0.1,
    )
    ax.grid(alpha=0.25)

maintenance_index = nearest_index(hours, 12.2)
power_ax.annotate(
    "Inspection window",
    xy=(
        hours[maintenance_index],
        data["ac_power"][maintenance_index],
    ),
    xytext=(35, -55),
    textcoords="offset points",
    ha="left",
    bbox={
        "boxstyle": "round,pad=0.3",
        "facecolor": "white",
        "edgecolor": "tab:red",
    },
    arrowprops={
        "arrowstyle": "->",
        "color": "tab:red",
    },
)

power_ax.set(
    title="Power Production",
    ylabel="AC power (kW)",
)
power_ax.legend(ncols=2)

temperature_ax.plot(
    hours,
    data["ambient_temperature"],
    color="tab:blue",
    label="Ambient",
)
temperature_ax.plot(
    hours,
    data["inverter_temperature"],
    color="tab:red",
    linewidth=2,
    label="Inverter",
)

peak_temperature_index = int(
    data["inverter_temperature"].argmax()
)
temperature_ax.annotate(
    (
        "Peak inverter temperature\n"
        f"{data['inverter_temperature'][peak_temperature_index]:.1f} °C"
    ),
    xy=(
        hours[peak_temperature_index],
        data["inverter_temperature"][peak_temperature_index],
    ),
    xytext=(0.02, 0.92),
    textcoords="axes fraction",
    ha="left",
    va="top",
    bbox={
        "boxstyle": "round,pad=0.3",
        "facecolor": "white",
        "edgecolor": "tab:red",
        "alpha": 0.9,
    },
    arrowprops={
        "arrowstyle": "->",
        "color": "tab:red",
    },
)

temperature_ax.set(
    title="Thermal Condition",
    xlabel="Local time (hour)",
    ylabel="Temperature (°C)",
    xlim=(5.5, 18.5),
)
temperature_ax.legend(ncols=2)

fig.suptitle(
    "Solar Farm Operations — Text and Annotation Dashboard"
)
fig.text(
    0.99,
    0.01,
    "Synthetic data for Matplotlib training",
    ha="right",
    fontsize=9,
    color="0.35",
)

plt.show()
