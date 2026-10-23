"""Cold-chain dashboard with shared time ticks and independent y-axis locators."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from cold_chain_data import create_cold_chain_day


def format_hour(value, position):
    return f"{int(round(value)):02d}:00"


data = create_cold_chain_day()

fig, axes = plt.subplots(
    2,
    1,
    figsize=(11, 7),
    sharex=True,
    layout="constrained",
)

temperature_ax, load_ax = axes

temperature_ax.plot(
    data["hours"],
    data["cold_room_temperature"],
    color="tab:blue",
    linewidth=2.2,
)
temperature_ax.set(
    title="Cold-Room Temperature",
    ylabel="Temperature (°C)",
)

load_ax.plot(
    data["hours"],
    data["compressor_load"],
    color="tab:red",
    linewidth=2,
)
load_ax.set(
    title="Compressor Load",
    xlabel="Local time",
    ylabel="Load (%)",
    xlim=(0, 24),
)

# แกน X ใช้ร่วมกัน จึงตั้ง Locator/Formatter ผ่าน load_ax ตัวเดียว
load_ax.xaxis.set_major_locator(
    mticker.MultipleLocator(4)
)
load_ax.xaxis.set_minor_locator(
    mticker.MultipleLocator(1)
)
load_ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(format_hour)
)

# แกน Y แยกกัน จึงสร้าง MaxNLocator ให้แต่ละแกน
for ax in axes:
    ax.yaxis.set_major_locator(
        mticker.MaxNLocator(nbins=5)
    )
    # ความยาวขีดเป็น points; ตำแหน่งมาจาก Locator ด้านบน
    ax.tick_params(
        axis="x",
        which="major",
        length=7,
    )
    ax.tick_params(
        axis="x",
        which="minor",
        length=3,
    )
    ax.grid(
        which="major",
        alpha=0.23,
    )
    ax.grid(
        axis="x",
        which="minor",
        alpha=0.08,
    )

fig.suptitle(
    "Cold-Chain Operations — Tick Design"
)

plt.show()

