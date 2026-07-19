import numpy as np
import matplotlib.pyplot as plt


hours = np.arange(0, 24)
zone_names = ["Tomato", "Melon", "Lettuce", "Seedling"]
colors = ["tomato", "goldenrod", "seagreen", "royalblue"]

fig, ax = plt.subplots(figsize=(10, 5.5))

for index, (zone_name, color) in enumerate(zip(zone_names, colors)):
    temperature = (
        24
        + index * 0.8
        + (2.5 + index * 0.3)
        * np.sin((hours - 6 - index * 0.25) * np.pi / 12)
    )
    ax.plot(
        hours,
        temperature,
        color=color,
        linewidth=2.2,
        label=zone_name,
    )

ax.set(
    title="Greenhouse Zones",
    xlabel="Hour",
    ylabel="Temperature (°C)",
    xlim=(0, 23),
)
ax.grid(alpha=0.25)

ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.02, 1),
    borderaxespad=0,
    title="Crop zone",
    frameon=False,
)

fig.tight_layout()
plt.show()
