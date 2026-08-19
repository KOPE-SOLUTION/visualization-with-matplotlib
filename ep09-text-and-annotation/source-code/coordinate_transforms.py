import matplotlib.pyplot as plt

from solar_data import create_solar_day, nearest_index


data = create_solar_day()
hours = data["hours"]
ac_power = data["ac_power"]

fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    ac_power,
    color="tab:orange",
    linewidth=2.2,
)

maintenance_index = nearest_index(hours, 12.2)

ax.text(
    hours[maintenance_index],
    ac_power[maintenance_index],
    "  Data position",
    transform=ax.transData,
    color="tab:red",
    va="bottom",
)

ax.text(
    0.02,
    0.95,
    "Axes position: 2% from left, 95% from bottom",
    transform=ax.transAxes,
    va="top",
    bbox={
        "boxstyle": "round,pad=0.3",
        "facecolor": "white",
        "edgecolor": "0.6",
        "alpha": 0.9,
    },
)

fig.text(
    0.99,
    0.01,
    "Figure position — synthetic training data",
    ha="right",
    va="bottom",
    fontsize=9,
    color="0.35",
)

ax.set(
    title="Three Coordinate Systems for Text",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(5.5, 18.5),
)
ax.grid(alpha=0.25)

plt.show()
