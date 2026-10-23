import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from cold_chain_data import create_cold_chain_day


def format_hour(value, position):
    """Format whole-hour ticks; position is required but unused here."""
    # จุดเน้น 1: รับค่าตำแหน่ง เช่น 4 แล้วคืนข้อความ "04:00"
    return f"{int(round(value)):02d}:00"


# ส่วนเดิม: เตรียมข้อมูลและวาดกราฟ
data = create_cold_chain_day()

fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    data["hours"],
    data["cold_room_temperature"],
    color="tab:blue",
    linewidth=2,
)

# ทบทวน: Locator ยังวางตำแหน่งทุก 4 ชั่วโมงเหมือนตัวอย่างก่อน
ax.xaxis.set_major_locator(
    mticker.MultipleLocator(4)
)
ax.xaxis.set_minor_locator(
    mticker.MultipleLocator(1)
)
# จุดเน้น 2: ส่งฟังก์ชันให้ Formatter; ไม่ใส่ () หลัง format_hour
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(format_hour)
)

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

ax.set(
    title="Cold-Room Temperature with Clock Labels",
    xlabel="Local time",
    ylabel="Temperature (°C)",
    xlim=(0, 24),
)
ax.grid(alpha=0.22)

plt.show()

