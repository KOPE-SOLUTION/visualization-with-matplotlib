import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from cold_chain_data import create_cold_chain_day


# ส่วนเดิม: เตรียมข้อมูลและวาดกราฟ ไม่ใช่จุดเน้นของตัวอย่างนี้
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

# จุดเน้น 1: Locator กำหนดตำแหน่งขีดบนแกน X (หน่วยของข้อมูลคือชั่วโมง)
ax.xaxis.set_major_locator(
    mticker.MultipleLocator(4)
)
ax.xaxis.set_minor_locator(
    mticker.MultipleLocator(1)
)

# จุดเน้น 2: ปรับขนาดขีด ไม่ได้เปลี่ยนระยะห่างระหว่าง Tick
ax.tick_params(
    axis="x",
    which="major",
    length=7,  # ความยาวขีด 7 points ไม่ใช่ 7 ชั่วโมง
    width=1.2,
)
ax.tick_params(
    axis="x",
    which="minor",
    length=3.5,
    width=0.8,
)

# ส่วนเสริม: ใช้เส้นตารางจาง ๆ ช่วยแยกจังหวะหลักกับจังหวะย่อย
ax.grid(
    axis="x",
    which="major",
    alpha=0.30,
)
ax.grid(
    axis="x",
    which="minor",
    alpha=0.10,
)
ax.grid(
    axis="y",
    which="major",
    alpha=0.20,
)

ax.set(
    title="Cold-Room Temperature — Major and Minor Ticks",
    xlabel="Hour of day",
    ylabel="Temperature (°C)",
    xlim=(0, 24),
)

plt.show()

