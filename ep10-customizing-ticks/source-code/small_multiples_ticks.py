import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from cold_chain_data import create_cold_chain_day


data = create_cold_chain_day()

series = [
    (
        data["cold_room_temperature"],
        "Cold-room temperature",
        "°C",
        "tab:blue",
    ),
    (
        data["ambient_temperature"],
        "Ambient temperature",
        "°C",
        "tab:orange",
    ),
    (
        data["compressor_load"],
        "Compressor load",
        "%",
        "tab:red",
    ),
    (
        data["relative_humidity"],
        "Relative humidity",
        "%RH",
        "tab:green",
    ),
]

fig, axes = plt.subplots(
    2,
    2,
    figsize=(11, 7),
    sharex=True,
    layout="constrained",
)

for ax, (values, title, unit, color) in zip(
    axes.flat,
    series,
):
    ax.plot(
        data["hours"],
        values,
        color=color,
        linewidth=2,
    )
    ax.xaxis.set_major_locator(
        mticker.MaxNLocator(
            nbins=4,
            integer=True,
        )
    )
    ax.yaxis.set_major_locator(
        mticker.MaxNLocator(nbins=4)
    )
    ax.set(
        title=title,
        ylabel=unit,
        xlim=(0, 24),
    )
    ax.grid(alpha=0.20)

for ax in axes[-1, :]:
    ax.set_xlabel("Hour of day")

fig.suptitle(
    "Cold-Chain Facility — Daily Sensor Overview"
)

plt.show()

