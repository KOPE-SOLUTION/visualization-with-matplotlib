import matplotlib.pyplot as plt

from solar_data import create_solar_day, nearest_index


data = create_solar_day()
hours = data["hours"]
ac_power = data["ac_power"]

fig, ax = plt.subplots(
    figsize=(11, 5.5),
    layout="constrained",
)

ax.plot(
    hours,
    data["clear_sky_power"],
    color="0.65",
    linestyle="--",
    label="Clear-sky reference",
)
ax.plot(
    hours,
    ac_power,
    color="tab:orange",
    linewidth=2.3,
    label="Measured AC power",
)

events = [
    {
        "hour": 9.1,
        "label": "Morning cloud",
        "offset": (-55, -55),
        "color": "tab:blue",
    },
    {
        "hour": 12.2,
        "label": "Inverter inspection",
        "offset": (0, -75),
        "color": "tab:red",
    },
    {
        "hour": 14.3,
        "label": "Afternoon cloud",
        "offset": (55, -60),
        "color": "tab:blue",
    },
]

for event in events:
    index = nearest_index(hours, event["hour"])
    xy = (hours[index], ac_power[index])

    ax.scatter(
        *xy,
        color=event["color"],
        zorder=3,
    )
    ax.annotate(
        event["label"],
        xy=xy,
        xytext=event["offset"],
        textcoords="offset points",
        ha="center",
        fontsize=9,
        bbox={
            "boxstyle": "round,pad=0.3",
            "facecolor": "white",
            "edgecolor": event["color"],
            "alpha": 0.95,
        },
        arrowprops={
            "arrowstyle": "->",
            "color": event["color"],
            "connectionstyle": "arc3,rad=0.15",
        },
    )

ax.set(
    title="Annotated Solar-Farm Operating Events",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(5.5, 18.5),
)
ax.legend()
ax.grid(alpha=0.25)

plt.show()
