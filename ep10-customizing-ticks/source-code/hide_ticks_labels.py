import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from cold_chain_data import create_cold_chain_day


# ใช้ข้อมูลและช่วงแกนเดียวกัน เพื่อให้เปรียบเทียบที่แกน X ได้ตรง ๆ
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
        ylabel="Temperature (°C)",
        xlim=(0, 24),
    )
    ax.xaxis.set_major_locator(mticker.MultipleLocator(4))
    # ไม่ใช้ Minor Ticks ในการเปรียบเทียบนี้
    ax.xaxis.set_minor_locator(mticker.NullLocator())
    ax.grid(alpha=0.25)

# ซ่อนเฉพาะตัวเลขแกน X; ขีดและเส้นตารางแนวตั้งยังอยู่
axes[0].xaxis.set_major_formatter(
    mticker.NullFormatter()
)
axes[0].set_title(
    "NullFormatter: positions remain"
)

# ใช้แกน X เหมือนช่องซ้าย แต่เอาตำแหน่ง Major Tick ออก
axes[1].xaxis.set_major_locator(
    mticker.NullLocator()
)
axes[1].set_title(
    "NullLocator: positions disappear"
)

plt.show()

