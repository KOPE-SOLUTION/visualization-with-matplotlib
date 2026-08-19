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

ax.set(
    title="Solar Farm AC Power — One Operating Day",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(5.5, 18.5),
)
ax.grid(alpha=0.25)

cloud_index = nearest_index(hours, 14.3)
text_style = {
    "fontsize": 10,
    "color": "tab:blue",
    "fontweight": "bold",
    "ha": "center",
}

ax.text(
    hours[cloud_index],
    ac_power[cloud_index] + 380,
    "Afternoon cloud passage",
    **text_style,
)

plt.show()
