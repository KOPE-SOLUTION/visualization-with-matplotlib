# EP10 — Customizing Ticks for Cold-Chain Logistics Monitoring

Tick เป็นรายละเอียดเล็กบนแกน แต่มีผลโดยตรงต่อการอ่านเวลา ช่วงค่า และจังหวะการเปลี่ยนแปลงของข้อมูล หาก Tick ถี่เกินไป Label จะชนกัน หากห่างเกินไป ผู้อ่านอาจระบุตำแหน่งเหตุการณ์ได้ยาก

บทนี้ใช้ **ระบบติดตามคลังสินค้าและห้องเย็นใน Cold Chain** เป็นกรณีศึกษา โดยสร้างข้อมูลอุณหภูมิ โหลด Compressor และความชื้นตลอด 24 ชั่วโมง แล้วปรับ Tick ให้เหมาะกับกราฟเดี่ยวและ Dashboard หลายช่อง

ตัวอย่าง โครงเรื่อง และคำอธิบายทั้งหมดเรียบเรียงขึ้นใหม่สำหรับหลักสูตรนี้ ไม่ได้ใช้ข้อมูลจากคลังสินค้าจริง ค่าและเหตุการณ์ที่จำลองขึ้นมีไว้สำหรับเรียน Matplotlib เท่านั้น ไม่ควรนำไปเป็นเกณฑ์ควบคุมระบบทำความเย็นหรือความปลอดภัยของสินค้า

## เส้นทางการเรียน

1. เริ่มจาก Tick อัตโนมัติของ Matplotlib
2. แยกหน้าที่ของ Locator และ Formatter
3. สร้าง Major และ Minor Ticks
4. เปลี่ยนตัวเลขชั่วโมงเป็นข้อความเวลา
5. ลดจำนวน Tick ใน Dashboard
6. เปรียบเทียบการซ่อน Label กับการลบตำแหน่ง Tick
7. เลือกเครื่องมือให้เหมาะกับกราฟคงที่และกราฟที่ปรับช่วงได้

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบบทนี้ จะสามารถ:

- อธิบายความสัมพันธ์ระหว่าง Axes, Axis และ Tick
- แยก Major Tick ออกจาก Minor Tick
- อธิบายว่า Locator เลือกตำแหน่ง ส่วน Formatter สร้างข้อความ
- ใช้ `set_xticks()` กับกราฟที่กำหนดตำแหน่งตายตัว
- ใช้ `MultipleLocator` และ `MaxNLocator` กับกราฟที่ต้องปรับตามช่วงแกน
- ใช้ `FuncFormatter` สร้างรูปแบบ Label ตามกติกาของงาน
- ใช้ `NullFormatter` และ `NullLocator` ได้โดยไม่สับสน
- ปรับความยาว สี และ Grid ของ Tick ด้วย `tick_params()`
- หลีกเลี่ยงการตั้ง Tick Label แยกจากตำแหน่งของมัน

## ภาพจำก่อนเริ่ม

ให้คิดว่าแกนเป็นถนน:

- **Locator** เลือกว่าจะตั้งป้ายตรงกิโลเมตรใด
- **Formatter** เลือกว่าจะเขียนข้อความอะไรบนป้ายนั้น
- **Major Tick** เป็นป้ายหลักที่ควรอ่านได้ทันที
- **Minor Tick** เป็นขีดช่วยกะระยะระหว่างป้ายหลัก

โครงสร้าง Object ที่เกี่ยวข้องคือ:

~~~text
Figure
└── Axes
    ├── xaxis (XAxis)
    │   ├── Major Locator
    │   ├── Major Formatter
    │   ├── Minor Locator
    │   └── Minor Formatter
    └── yaxis (YAxis)
~~~

`ax` คือพื้นที่กราฟ ส่วน `ax.xaxis` และ `ax.yaxis` คือ Axis Object ที่จัดการ Tick, Tick Label, Grid และชื่อแกนของแต่ละด้าน

---

## 1. เตรียมข้อมูล Cold Chain

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
~~~

บทนี้เรียก `matplotlib.ticker` ด้วยชื่อย่อ `mticker` เพื่อให้เห็นชัดว่า `MultipleLocator`, `MaxNLocator` และ Formatter ต่าง ๆ เป็นเครื่องมือในกลุ่ม Ticker

ติดตั้งไลบรารีได้ด้วย:

~~~bash
python -m pip install numpy matplotlib
~~~

### เซลล์ที่ 2 — สร้างข้อมูลหนึ่งวัน

~~~python
rng = np.random.default_rng(10)

hours = np.arange(0, 24.01, 0.25)

ambient_temperature = (
    29
    + 5 * np.sin(
        2 * np.pi * (hours - 8) / 24
    )
    + rng.normal(0, 0.35, hours.size)
)

cold_room_temperature = (
    -20
    + rng.normal(0, 0.12, hours.size)
)

door_open = (
    (hours >= 10.0)
    & (hours <= 10.75)
)

cold_room_temperature[door_open] += np.linspace(
    0.5,
    2.2,
    door_open.sum(),
)

recovery = (
    (hours > 10.75)
    & (hours <= 12.0)
)

cold_room_temperature[recovery] += np.linspace(
    1.8,
    0,
    recovery.sum(),
)

compressor_load = np.clip(
    48
    + 9 * (cold_room_temperature + 20)
    + rng.normal(0, 2.0, hours.size),
    20,
    100,
)

relative_humidity = np.clip(
    72
    + 5 * door_open.astype(float)
    + rng.normal(0, 0.8, hours.size),
    55,
    90,
)
~~~

ข้อมูลถูกเก็บทุก 15 นาที เพราะ `0.25` ชั่วโมงเท่ากับ 15 นาที จึงมีจุดข้อมูล 97 จุดตั้งแต่เวลา 00:00 ถึง 24:00 รวมปลายช่วง

- `cold_room_temperature` คืออุณหภูมิห้องเย็นจำลอง
- `ambient_temperature` คืออุณหภูมิภายนอกจำลอง
- `door_open` เป็น Boolean Mask ของช่วงเปิดประตู
- `compressor_load` คือโหลด Compressor จำลองในช่วง 20–100%
- `relative_humidity` คือความชื้นสัมพัทธ์จำลอง

สูตรมีหน้าที่สร้างข้อมูลสำหรับฝึก Tick เท่านั้น ไม่ใช่แบบจำลองทางวิศวกรรมของระบบทำความเย็น

---

## 2. เริ่มจาก Tick อัตโนมัติ

### เซลล์ที่ 3 — วาดกราฟโดยไม่ตั้ง Tick เอง

~~~python
fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    cold_room_temperature,
    color="tab:blue",
    linewidth=2,
)

ax.set(
    title="Cold-Room Temperature — Default Ticks",
    xlabel="Hour of day",
    ylabel="Temperature (°C)",
    xlim=(0, 24),
)

ax.grid(alpha=0.22)
plt.show()
~~~

ในโค้ดนี้ไม่มี `set_xticks()` และไม่มี Locator ที่เรากำหนดเอง Matplotlib จึงเลือกตำแหน่งและข้อความให้โดยอัตโนมัติ ค่า Default เหมาะสำหรับเริ่มสำรวจข้อมูล และไม่จำเป็นต้องปรับ Tick ทุกกราฟ

### เซลล์ที่ 4 — ตรวจ Object ที่ทำงานอยู่เบื้องหลัง

~~~python
print(
    type(
        ax.xaxis.get_major_locator()
    ).__name__
)

print(
    type(
        ax.xaxis.get_major_formatter()
    ).__name__
)

print(
    type(
        ax.xaxis.get_minor_locator()
    ).__name__
)

print(
    type(
        ax.xaxis.get_minor_formatter()
    ).__name__
)
~~~

บนแกน Linear ทั่วไป มักพบ `AutoLocator` และ `ScalarFormatter` สำหรับ Major Ticks ส่วน Minor Ticks อาจยังใช้ `NullLocator` และ `NullFormatter` จึงไม่ปรากฏให้เห็น

Class ที่เป็น Default สามารถเปลี่ยนตาม Scale และชนิดข้อมูล เช่น แกน Log หรือแกนวันที่จะใช้เครื่องมือที่เหมาะกับข้อมูลประเภทนั้น

---

## 3. วิธีสั้นสำหรับกราฟที่กำหนดตำแหน่งตายตัว

หากกราฟนี้ใช้ช่วงเวลา 0–24 ชั่วโมงแน่นอน สามารถระบุตำแหน่ง Tick โดยตรงได้

### เซลล์ที่ 5 — กำหนด Major และ Minor Ticks ด้วย `set_xticks()`

~~~python
fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    cold_room_temperature,
    color="tab:blue",
    linewidth=2,
)

ax.set_xticks(
    np.arange(0, 25, 4)
)
ax.set_xticks(
    np.arange(0, 25, 1),
    minor=True,
)

ax.set(
    title="Cold-Room Temperature — Fixed Tick Positions",
    xlabel="Hour of day",
    ylabel="Temperature (°C)",
    xlim=(0, 24),
)

ax.grid(
    axis="x",
    which="major",
    alpha=0.30,
)
ax.grid(
    axis="x",
    which="minor",
    alpha=0.08,
)

plt.show()
~~~

- Major Tick อยู่ทุก 4 ชั่วโมงและมี Label
- Minor Tick อยู่ทุก 1 ชั่วโมง โดยปกติไม่มี Label
- `minor=True` บอกว่ารายการตำแหน่งชุดที่สองเป็น Minor Ticks

`set_xticks()` เหมาะกับภาพรายงานที่ช่วงแกนไม่เปลี่ยน แต่ตำแหน่งเหล่านี้เป็นค่าคงที่ หากภายหลังเปลี่ยน `xlim` หรือใช้กราฟแบบ Interactive อาจต้องแก้รายการ Tick ด้วยตนเอง

---

## 4. Major และ Minor Ticks ด้วย Locator

Locator เหมาะเมื่ออยากกำหนด “กติกา” มากกว่าระบุตำแหน่งทุกค่า

### เซลล์ที่ 6 — ใช้ `MultipleLocator`

~~~python
fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    cold_room_temperature,
    color="tab:blue",
    linewidth=2,
)

ax.xaxis.set_major_locator(
    mticker.MultipleLocator(4)
)
ax.xaxis.set_minor_locator(
    mticker.MultipleLocator(1)
)

ax.tick_params(
    axis="x",
    which="major",
    length=7,
    width=1.2,
)
ax.tick_params(
    axis="x",
    which="minor",
    length=3.5,
    width=0.8,
)

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

ax.set(
    title="Cold-Room Temperature — Major and Minor Ticks",
    xlabel="Hour of day",
    ylabel="Temperature (°C)",
    xlim=(0, 24),
)

plt.show()
~~~

ความหมายของ Locator สองรายการคือ:

- `MultipleLocator(4)` วาง Major Tick ที่ค่าซึ่งเป็นผลคูณของ 4
- `MultipleLocator(1)` วาง Minor Tick ทุกหนึ่งหน่วยของแกน X

`tick_params()` เปลี่ยนหน้าตา ไม่ได้เปลี่ยนตำแหน่ง Tick ส่วน `which` เลือกว่าจะปรับ Major หรือ Minor

Minor Grid ควรจางกว่า Major Grid มิฉะนั้นพื้นหลังจะเด่นกว่าเส้นข้อมูล

---

## 5. Locator กับ Formatter ทำงานคนละหน้าที่

เมื่อใช้ `MultipleLocator(4)` เราได้ตำแหน่ง `0, 4, 8, 12, ...` แต่ Label ยังเป็นตัวเลขธรรมดา หากต้องการแสดงเป็น `00:00`, `04:00`, `08:00` ต้องเปลี่ยน Formatter

### เซลล์ที่ 7 — สร้าง Formatter สำหรับเวลา

~~~python
def format_hour(value, position):
    return f"{int(round(value)):02d}:00"
~~~

Matplotlib ส่งข้อมูลให้ Function สองค่า:

- `value` คือค่าของ Tick บนแกน เช่น `4.0`
- `position` คือลำดับของ Tick ที่กำลัง Format

ตัวอย่างนี้ไม่ได้ใช้ `position` แต่ยังต้องรับ Parameter ไว้ตามรูปแบบที่ `FuncFormatter` เรียก

### เซลล์ที่ 8 — นำ Function ไปใช้กับ Major Tick

~~~python
fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    cold_room_temperature,
    color="tab:blue",
    linewidth=2,
)

ax.xaxis.set_major_locator(
    mticker.MultipleLocator(4)
)
ax.xaxis.set_minor_locator(
    mticker.MultipleLocator(1)
)
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(format_hour)
)

ax.set(
    title="Cold-Room Temperature with Clock Labels",
    xlabel="Local time",
    ylabel="Temperature (°C)",
    xlim=(0, 24),
)

ax.grid(alpha=0.22)
plt.show()
~~~

ลำดับการทำงานคือ:

~~~text
ช่วงแกน X
→ Locator เลือกตำแหน่ง 0, 4, 8, 12, ...
→ Formatter รับค่าทีละตำแหน่ง
→ แสดงเป็น 00:00, 04:00, 08:00, 12:00, ...
~~~

Formatter เปลี่ยนเฉพาะข้อความที่แสดง ค่าใน Array `hours` ยังคงเป็นตัวเลขเดิม

---

## 6. ลดจำนวน Tick ใน Dashboard

เมื่อ Axes มีขนาดเล็ก Tick แบบอัตโนมัติอาจแน่นเกินไป `MaxNLocator` ช่วยจำกัดจำนวนช่วงและยังเลือกค่าที่อ่านง่ายให้

### เซลล์ที่ 9 — ใช้ `MaxNLocator` กับกราฟ 2×2

~~~python
series = [
    (
        cold_room_temperature,
        "Cold-room temperature",
        "°C",
        "tab:blue",
    ),
    (
        ambient_temperature,
        "Ambient temperature",
        "°C",
        "tab:orange",
    ),
    (
        compressor_load,
        "Compressor load",
        "%",
        "tab:red",
    ),
    (
        relative_humidity,
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
        hours,
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
~~~

`MaxNLocator(nbins=4)` กำหนดจำนวน **ช่วงระหว่าง Tick** ไม่เกิน 4 ช่วง ดังนั้นภายใน Limit อาจเห็นได้ถึง 5 Tick และไม่รับประกันว่าจะต้องได้จำนวนเท่ากันทุกครั้ง

`integer=True` ขอให้ Locator เลือกค่าจำนวนเต็มเมื่อช่วงข้อมูลเอื้ออำนวย เหมาะกับแกนชั่วโมงในตัวอย่างนี้ แต่ไม่ควรใช้กับข้อมูลที่ต้องแสดงทศนิยมละเอียด

---

## 7. ซ่อน Label หรือซ่อน Tick ทั้งชุด

สองคำสั่งนี้มีผลต่างกัน:

- `NullFormatter()` คืนข้อความว่าง แต่ Locator ยังมีตำแหน่ง Tick
- `NullLocator()` ไม่สร้างตำแหน่ง Tick จึงไม่มี Tick, Label และ Grid ที่ผูกกับตำแหน่งนั้น

### เซลล์ที่ 10 — เปรียบเทียบแบบข้างกัน

~~~python
fig, axes = plt.subplots(
    1,
    2,
    figsize=(11, 4.5),
    layout="constrained",
)

for ax in axes:
    ax.plot(
        hours,
        cold_room_temperature,
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
~~~

หากเพียงต้องการไม่แสดง Label ภายในกริด Subplot การใช้ `tick_params(labelbottom=False)` มักสื่อเจตนาได้ตรงกว่า ส่วน `NullFormatter` เหมาะเมื่อกำลังสาธิตหรือควบคุม Formatter โดยตรง

---

## 8. Tick ของข้อมูลแบบหมวดหมู่

กราฟแท่งที่มีชื่อ Dock เป็นหมวดหมู่ควรกำหนดตำแหน่งและ Label พร้อมกัน อย่าเรียก `set_xticklabels()` เพียงอย่างเดียว เพราะ Locator อาจเปลี่ยนตำแหน่งภายหลัง

### เซลล์ที่ 11 — จับคู่ตำแหน่งกับชื่อ Dock

~~~python
dock_names = [
    "Dock A",
    "Dock B",
    "Dock C",
    "Dock D",
]

average_unloading_time = [
    31,
    26,
    38,
    29,
]

positions = np.arange(
    len(dock_names)
)

fig, ax = plt.subplots(
    figsize=(8, 4.5),
    layout="constrained",
)

ax.bar(
    positions,
    average_unloading_time,
    color="tab:cyan",
)

ax.set_xticks(
    positions,
    labels=dock_names,
)

ax.set(
    title="Average Unloading Time by Dock",
    xlabel="Receiving dock",
    ylabel="Minutes",
)

ax.yaxis.set_major_locator(
    mticker.MaxNLocator(
        nbins=5,
        integer=True,
    )
)
ax.grid(
    axis="y",
    alpha=0.20,
)

plt.show()
~~~

การส่ง `positions` และ `labels` ในคำสั่งเดียวช่วยให้จำนวนและลำดับตรงกัน หากจำนวน Label ไม่เท่ากับจำนวนตำแหน่ง Matplotlib จะรายงานข้อผิดพลาดแทนการจับคู่แบบคลุมเครือ

---

## 9. เลือก Locator และ Formatter อย่างไร

### Locator ที่ใช้บ่อย

| ความต้องการ | เครื่องมือ |
|---|---|
| ให้ Matplotlib เลือกอัตโนมัติ | `AutoLocator` |
| Tick ทุกระยะคงที่ | `MultipleLocator` |
| จำกัดความแน่นของ Tick | `MaxNLocator` |
| แบ่งช่อง Major Tick บนแกน Linear | `AutoMinorLocator` |
| ตำแหน่งกำหนดตายตัว | `FixedLocator` หรือ `set_xticks()` |
| ไม่ต้องการตำแหน่ง Tick | `NullLocator` |
| แกน Logarithmic | `LogLocator` |

### Formatter ที่ใช้บ่อย

| ความต้องการ | เครื่องมือ |
|---|---|
| ตัวเลขทั่วไปบนแกน Linear | `ScalarFormatter` |
| กติกาข้อความที่เขียนเอง | `FuncFormatter` |
| รูปแบบด้วย `{x}` | `StrMethodFormatter` |
| แสดงเปอร์เซ็นต์ | `PercentFormatter` |
| หน่วยวิศวกรรม เช่น kW หรือ MHz | `EngFormatter` |
| Label กำหนดเองตามตำแหน่งตายตัว | `FixedFormatter` คู่กับ `FixedLocator` |
| ซ่อนข้อความ | `NullFormatter` |
| แกน Logarithmic | Formatter ในกลุ่ม `LogFormatter` |

ไม่ควรนำ Locator Object เดียวไปใช้ร่วมกับ Axis หลายตัว ให้สร้าง Instance ใหม่สำหรับแต่ละ Axis เพราะ Locator เก็บการอ้างอิงถึง Axis ที่มันทำงานด้วย

<details>
  <summary>อ่านต่อเมื่อพร้อม: Tick บน Log Scale</summary>

หากข้อมูลครอบคลุมหลายลำดับขนาด เช่น จำนวนจุลินทรีย์จาก 1 ถึง 100,000 สามารถใช้แกน Log ได้:

~~~python
sample_hours = np.arange(6)
microbial_count = np.array([
    1,
    4,
    20,
    300,
    5000,
    100000,
])

fig, ax = plt.subplots(
    figsize=(8, 4.5),
    layout="constrained",
)

ax.plot(
    sample_hours,
    microbial_count,
    marker="o",
)
ax.set_yscale("log")
ax.set(
    title="Training Example — Logarithmic Count Scale",
    xlabel="Sample sequence",
    ylabel="Count (log scale)",
)
ax.grid(
    which="both",
    alpha=0.20,
)

plt.show()
~~~

เมื่อใช้ `set_yscale("log")` Matplotlib จะเลือก Locator และ Formatter สำหรับ Log Scale ให้อัตโนมัติ จึงควรทดลองค่า Default ก่อนปรับเอง ตัวเลขชุดนี้เป็นข้อมูลฝึก ไม่ใช่ผลตรวจสินค้าและไม่ใช่เกณฑ์ความปลอดภัย

</details>

---

## 10. ลำดับการตัดสินใจเมื่อ Tick อ่านยาก

1. ตรวจว่าช่วงแกนและหน่วยถูกต้องหรือไม่
2. ทดลองลดจำนวน Tick ด้วย `MaxNLocator`
3. หากต้องการระยะตายตัว ใช้ `MultipleLocator`
4. เพิ่ม Minor Tick เฉพาะเมื่อช่วยกะระยะ
5. ใช้ Formatter เมื่อข้อความเดิมไม่สื่อความหมาย เช่น ชั่วโมงต้องอ่านเป็นเวลา
6. ปรับ `tick_params()` หลังตำแหน่งและ Label ถูกต้องแล้ว
7. เปลี่ยนขนาด Figure และ Export เพื่อตรวจการชนกันอีกครั้ง

อย่าเริ่มจากการหมุน Label ทุกครั้ง การหมุนช่วยเพิ่มพื้นที่ได้ แต่ถ้าปัญหาเกิดจาก Tick มากเกินไป ควรแก้จำนวน Tick ก่อน

---

## 11. ข้อผิดพลาดที่พบบ่อย

### สับสนว่า Formatter เปลี่ยนข้อมูล

Formatter เปลี่ยนเฉพาะข้อความบนแกน ค่าใน Array ไม่ถูกแก้ไข

### ตั้ง Label โดยไม่ล็อกตำแหน่ง

หลีกเลี่ยง:

~~~python
ax.set_xticklabels([
    "A",
    "B",
    "C",
])
~~~

ควรจับคู่ตำแหน่งและ Label:

~~~python
ax.set_xticks(
    [0, 1, 2],
    labels=["A", "B", "C"],
)
~~~

### ใส่ Label ให้ Minor Tick ทุกตำแหน่ง

Minor Tick มีหน้าที่ช่วยกะระยะ หากใส่ข้อความทุกจุด กราฟอาจกลับมาแน่นเหมือนเดิม

### ทำ Minor Grid เข้มเท่า Major Grid

ลำดับชั้นของกราฟควรชัด Major Grid ใช้นำสายตา ส่วน Minor Grid ควรเบากว่า

### เข้าใจ `nbins` ว่าเป็นจำนวน Tick

ใน `MaxNLocator` ค่า `nbins` คือจำนวนช่วงสูงสุด ไม่ใช่จำนวน Tick ที่ต้องได้แบบตายตัว

### ใช้ `AutoMinorLocator` กับ Log Scale

`AutoMinorLocator` ออกแบบสำหรับแกน Linear ที่ Major Ticks มีระยะสม่ำเสมอ แกน Log ควรใช้ Locator ที่เหมาะกับ Log Scale

---

## 12. Export และตรวจผลงาน

~~~python
fig.savefig(
    "cold-chain-ticks.png",
    dpi=160,
    bbox_inches="tight",
)
~~~

ก่อนนำภาพไปใช้ ให้ตรวจว่า:

- Major Labels ไม่ชนกัน
- Minor Ticks ไม่เด่นเกินไป
- เวลาและหน่วยอ่านได้โดยไม่ต้องเดา
- Grid ไม่กลบเส้นข้อมูล
- รูปแบบตัวเลขไม่ทำให้ค่าจริงดูผิดความหมาย
- Label ยังอ่านได้เมื่อย่อภาพเป็นขนาดปลายทาง

---

## แบบฝึกหัด

1. เปลี่ยน Major Tick จากทุก 4 ชั่วโมงเป็นทุก 3 ชั่วโมง
2. เปลี่ยน Minor Tick จากทุก 1 ชั่วโมงเป็นทุก 30 นาที
3. เปรียบเทียบ `set_xticks()` กับ `MultipleLocator` หลังเปลี่ยน `xlim=(8, 16)`
4. เขียน `FuncFormatter` ให้แสดงเวลาแบบ `8 AM`, `12 PM`, `4 PM`
5. ทดลอง `MaxNLocator(nbins=3)`, `nbins=5` และ `nbins=8`
6. ใช้ `NullFormatter` ซ่อน Label แกน X แล้วตรวจว่า Grid ยังอยู่หรือไม่
7. ใช้ `NullLocator` กับแกนเดียวกันและอธิบายความต่าง
8. สร้าง Bar Chart ชื่อคลังสินค้าโดยกำหนดตำแหน่งและ Label พร้อมกัน

อ่านโจทย์ฉบับเต็มได้ที่ [แบบฝึกหัด EP10](./exercises/exercise01.md)

## สคริปต์ฉบับเต็ม

- [cold_chain_data.py](./source-code/cold_chain_data.py) — สร้างข้อมูลสังเคราะห์
- [major_minor_ticks.py](./source-code/major_minor_ticks.py) — Major และ Minor Ticks
- [custom_time_formatter.py](./source-code/custom_time_formatter.py) — Formatter สำหรับเวลา
- [small_multiples_ticks.py](./source-code/small_multiples_ticks.py) — ลด Tick ใน Dashboard
- [hide_ticks_labels.py](./source-code/hide_ticks_labels.py) — เปรียบเทียบ NullFormatter และ NullLocator
- [cold_chain_tick_dashboard.py](./source-code/cold_chain_tick_dashboard.py) — ตัวอย่างรวมสำหรับต่อยอด

## เอกสาร Matplotlib ที่เกี่ยวข้อง

- [Axis ticks](https://matplotlib.org/stable/users/explain/axes/axes_ticks.html)
- [`matplotlib.ticker`](https://matplotlib.org/stable/api/ticker_api.html)
- [`Axes.tick_params`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html)
- [Tick formatters gallery](https://matplotlib.org/stable/gallery/ticks/tick-formatters.html)

## ตอนก่อนหน้า

**EP9 — [Text and Annotation for Solar Power Plant Operations](../ep09-text-and-annotation/README.md)**

## ตอนถัดไป

**EP11 — Customizing Matplotlib: Configurations and Stylesheets**

