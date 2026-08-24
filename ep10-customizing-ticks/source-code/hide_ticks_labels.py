import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from cold_chain_data import create_cold_chain_day


data = create_cold_chain_day()

fig, axes = plt.subplots(
    1,
    2,
    figsize=(11, 4.5),
    layout="constrained",
)

for ax in axes:
    ax.plot(
        data["hours"],
        data["cold_room_temperature"],
        color="tab:blue",
    )
    ax.set(
        xlabel="Hour of day",
        xlim=(0, 24),
    )
    ax.grid(alpha=0.25)

axes[0].xaxis.set_major_formatter(
    mticker.NullFormatter()
)
axes[0].set_title(
    "NullFormatter: positions remain"
)

axes[1].yaxis.set_major_locator(
    mticker.NullLocator()
)
axes[1].set_title(
    "NullLocator: positions disappear"
)

plt.show()

