import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from cold_chain_data import create_cold_chain_day


# ส่วนเดิมจาก EP8: ข้อมูลหลายชุดและ Layout 2x2 ไม่ต้องอธิบายซ้ำทุกบรรทัด
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

# จุดเน้น 1: sharex=True ทำให้แกน X ใช้ Locator ร่วมกัน ตั้งผ่านช่องเดียวพอ
axes[-1, 0].xaxis.set_major_locator(
    mticker.MaxNLocator(nbins=4, integer=True)
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
    # จุดเน้น 2: จำกัดจำนวนช่วงบนแกน Y; สร้าง Locator ใหม่ให้แต่ละแกน
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

