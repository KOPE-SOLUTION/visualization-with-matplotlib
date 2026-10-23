# EP10 — Customizing Ticks for Cold-Chain Logistics Monitoring

บทนี้อธิบายการปรับ **ขีดและข้อความบนแกน** ให้กราฟอ่านง่ายขึ้น เช่น เปลี่ยนจาก `4` เป็น `04:00` หรือวางขีดหลักทุก 4 ชั่วโมง โดยไม่เปลี่ยนข้อมูลที่ใช้วาดกราฟ

บทนี้ใช้ **ระบบติดตามคลังสินค้าและห้องเย็นใน Cold Chain** เป็นกรณีศึกษา โดยสร้างข้อมูลอุณหภูมิ โหลด Compressor และความชื้นตลอด 24 ชั่วโมง แล้วปรับ Tick ให้เหมาะกับกราฟเดี่ยวและ Dashboard หลายช่อง

ตัวอย่าง โครงเรื่อง และคำอธิบายทั้งหมดเรียบเรียงขึ้นใหม่สำหรับหลักสูตรนี้ ไม่ได้ใช้ข้อมูลจากคลังสินค้าจริง ค่าและเหตุการณ์ที่จำลองขึ้นมีไว้สำหรับเรียน Matplotlib เท่านั้น ไม่ควรนำไปเป็นเกณฑ์ควบคุมระบบทำความเย็นหรือความปลอดภัยของสินค้า

## การใช้งานตัวอย่าง

- รัน Import และข้อมูลในเซลล์ที่ 1–2 ก่อน จากนั้นเลือกตัวอย่างที่ต้องการทดลอง
- โค้ดสั้นในแต่ละหัวข้อแสดงคำสั่งเฉพาะส่วน ส่วนกล่อง “โค้ดเต็ม” มีคำสั่งสร้างและแสดงกราฟครบทั้งเซลล์ เลือกรันโค้ดเต็มเมื่อต้องการดูผลลัพธ์
- แต่ละตัวอย่างระบุผลที่ควรเห็นและค่าที่ปรับทดลองได้
- สูตรจำลองข้อมูล โครงสร้าง Object และตารางเครื่องมือเพิ่มเติมอยู่ในส่วนที่พับเก็บไว้

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
- ปรับหน้าตาขีดด้วย `tick_params()` และแยก Grid หลัก/ย่อยด้วย `ax.grid()`
- หลีกเลี่ยงการตั้ง Tick Label แยกจากตำแหน่งของมัน

## ภาพจำก่อนเริ่ม

แยกสิ่งที่เห็นบนแกนก่อน: **Tick** คือขีดสั้น ๆ ที่ขอบกราฟ ส่วน **Tick Label** คือตัวเลขหรือข้อความข้างขีด ไม่ใช่ชื่อแกน เช่น `Hour of day`

| คำถามที่ต้องตอบ | เครื่องมือ | ตัวอย่าง |
|---|---|---|
| ขีดอยู่ตรงไหน? | Locator | `0, 4, 8, 12, ...` |
| เขียนอะไรข้างขีด? | Formatter | `00:00, 04:00, 08:00, ...` |
| ขีดยาวหรือหนาเท่าไร? | `tick_params()` | ขีดหลักยาว 7 points |

**Major Tick** คือขีดหลัก ส่วน **Minor Tick** คือขีดย่อยที่ช่วยกะระยะ โดยทั่วไปตัวอย่างนี้ใส่ตัวเลขเฉพาะขีดหลัก

<details>
<summary>อ่านเสริม: Axes, Axis และ Object ที่เกี่ยวข้อง</summary>

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

</details>

---

## 1. เตรียมข้อมูล Cold Chain

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  # เพิ่มจากบทก่อน: เครื่องมือจัดการ Tick
~~~

บทนี้เรียก `matplotlib.ticker` ด้วยชื่อย่อ `mticker` เพื่อให้เห็นชัดว่า `MultipleLocator`, `MaxNLocator` และ Formatter ต่าง ๆ เป็นเครื่องมือในกลุ่ม Ticker

ติดตั้งไลบรารีได้ด้วย:

~~~bash
python -m pip install numpy matplotlib
~~~

### เซลล์ที่ 2 — สร้างข้อมูลหนึ่งวัน

`hours` เก็บเวลาในหน่วยชั่วโมง และ `cold_room_temperature` เก็บอุณหภูมิห้องเย็น ส่วนข้อมูลอุณหภูมิภายนอก โหลด Compressor และความชื้นใช้ในตัวอย่าง Dashboard

<details>
<summary>เปิดโค้ดเตรียมข้อมูล — รันครั้งเดียวก่อนเริ่มตัวอย่าง</summary>

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
    + 0.18 * np.sin(2 * np.pi * hours / 6)
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
    + 5 * np.sin(2 * np.pi * hours / 4)
    + rng.normal(0, 2.0, hours.size),
    20,
    100,
)

relative_humidity = np.clip(
    72
    + 2.5 * np.sin(2 * np.pi * (hours + 1) / 8)
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

สูตรในเซลล์นี้ตรงกับ [`cold_chain_data.py`](./source-code/cold_chain_data.py) จึงได้ข้อมูลชุดเดียวกับสคริปต์ตัวอย่างเมื่อใช้ Seed เดียวกัน

</details>

---

## 2. เริ่มจาก Tick อัตโนมัติ

### เซลล์ที่ 3 — วาดกราฟโดยไม่ตั้ง Tick เอง

ตัวอย่างนี้ใช้ตำแหน่งขีดและข้อความบนแกนที่ Matplotlib เลือกให้อัตโนมัติ

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

ผลที่ควรเห็น: เส้นอุณหภูมิพร้อมตัวเลขบนแกน แม้ไม่ได้กำหนด Tick เอง จำนวน Tick อาจต่างกันตามขนาดกราฟและเวอร์ชัน

<details>
<summary>รายละเอียด: ตรวจชื่อเครื่องมือที่ Matplotlib เลือกให้</summary>

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

</details>

---

## 3. วิธีสั้นสำหรับกราฟที่กำหนดตำแหน่งตายตัว

หากกราฟนี้ใช้ช่วงเวลา 0–24 ชั่วโมงแน่นอน สามารถระบุตำแหน่ง Tick โดยตรงได้

### เซลล์ที่ 5 — กำหนด Major และ Minor Ticks ด้วย `set_xticks()`

`set_xticks()` รับตำแหน่งเป็นรายการ ตัวเลขในรายการมีหน่วยเดียวกับแกน X คือชั่วโมง

คำสั่งกำหนดตำแหน่ง:

~~~python
# ขีดหลัก: 0, 4, 8, 12, 16, 20, 24
ax.set_xticks(np.arange(0, 25, 4))

# ขีดย่อย: ทุก 1 ชั่วโมง; minor=True เลือกชุดขีดย่อย
ax.set_xticks(np.arange(0, 25, 1), minor=True)
~~~

<details>
<summary>โค้ดเต็มเซลล์ที่ 5 — รันหลังเซลล์ที่ 1–2</summary>

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

# กำหนดตำแหน่งขีดหลักและขีดย่อยแยกกัน
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

</details>

ผลที่ควรเห็น: ขีดหลักที่ `0, 4, 8, ... 24` พร้อมตัวเลข และขีดย่อยระหว่างนั้น เช่น `1, 2, 3` โดยไม่แสดงขีดย่อยซ้ำตรงตำแหน่งขีดหลัก

ลองเปลี่ยนค่า: เปลี่ยน `np.arange(0, 25, 4)` เป็น `np.arange(0, 25, 6)` แล้วรันโค้ดเต็มใหม่ ขีดหลักจะห่างเป็นทุก 6 ชั่วโมง แต่เส้นอุณหภูมิไม่เปลี่ยน

`set_xticks()` เหมาะกับภาพรายงานที่ช่วงแกนไม่เปลี่ยน แต่ตำแหน่งเหล่านี้เป็นค่าคงที่ หากภายหลังเปลี่ยน `xlim` หรือใช้กราฟแบบ Interactive อาจต้องแก้รายการ Tick ด้วยตนเอง

---

## 4. Major และ Minor Ticks ด้วย Locator

Locator เหมาะเมื่ออยากกำหนด “กติกา” มากกว่าระบุตำแหน่งทุกค่า

### เซลล์ที่ 6 — ใช้ `MultipleLocator`

`MultipleLocator` คำนวณตำแหน่ง Tick จากระยะห่างที่กำหนด ส่วน `tick_params()` ปรับรูปลักษณ์ของขีดที่ตำแหน่งเหล่านั้น

กำหนดตำแหน่ง:

~~~python
ax.xaxis.set_major_locator(mticker.MultipleLocator(4))  # ทุก 4 ชั่วโมง
ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))  # ทุก 1 ชั่วโมง
~~~

ภาพแรกอาจเหมือนเซลล์ที่ 5 ซึ่งถูกต้องแล้ว เพราะใช้ตำแหน่งเดียวกัน ต่างกันที่คราวนี้ Locator คำนวณตำแหน่งจากกติกาให้

ปรับหน้าตาขีด:

~~~python
# length คือความยาวขีดสั้น ๆ ที่ขอบกราฟ ไม่ใช่ระยะห่างระหว่าง Tick
ax.tick_params(axis="x", which="major", length=7, width=1.2)
ax.tick_params(axis="x", which="minor", length=3.5, width=0.8)
~~~

`length=7` หมายถึงขีดยาว **7 points** (`1 point = 1/72 นิ้ว`) วัดจากเส้นขอบแกนถึงปลายขีดสำหรับทิศทาง `out` บนแกน X ด้านล่างจึงเห็นขีดยื่นลง ไม่ได้ยาวไปตามเส้นข้อมูลหรือเส้น Grid ส่วน `width` คือความหนาขีด หน่วย points เช่นกัน ดูรายละเอียดใน [`tick_params()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html)

ตัวอย่างไม่ได้ใส่ `direction` เพราะใช้ค่าเริ่มต้น `out` ของ Matplotlib หากเลือก Style อื่น ทิศทางอาจต่างออกไป

<details>
<summary>โค้ดเต็มเซลล์ที่ 6 — รวมการแต่ง Grid; รันหลังเซลล์ที่ 1–2</summary>

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

# กำหนดระยะห่างของ Tick
ax.xaxis.set_major_locator(
    mticker.MultipleLocator(4)
)
ax.xaxis.set_minor_locator(
    mticker.MultipleLocator(1)
)

# ปรับหน้าตาขีดโดยไม่เปลี่ยนตำแหน่ง
ax.tick_params(
    axis="x",
    which="major",
    length=7,  # points ไม่ใช่ชั่วโมง
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

</details>

ผลที่ควรเห็น: ขีดหลักห่างกันทุก 4 ชั่วโมงและยาวกว่าขีดย่อย ส่วน Grid ย่อยจางกว่า Grid หลัก

ลองเปลี่ยนค่าทีละอย่าง:

1. เปลี่ยน `MultipleLocator(4)` เป็น `MultipleLocator(6)` — ตำแหน่งขีดหลักเปลี่ยน
2. กลับมาใช้ `4` แล้วเปลี่ยนเฉพาะ `length=7` เป็น `length=14` — ขีดยาวขึ้น แต่ตำแหน่งตามแกนและค่าตัวเลขไม่เปลี่ยน

Locator กำหนดตำแหน่งขีด ส่วน `tick_params()` กำหนดรูปลักษณ์ของขีด

---

## 5. Locator กับ Formatter ทำงานคนละหน้าที่

เมื่อใช้ `MultipleLocator(4)` เราได้ตำแหน่ง `0, 4, 8, 12, ...` แต่ Label ยังเป็นตัวเลขธรรมดา หากต้องการแสดงเป็น `00:00`, `04:00`, `08:00` ต้องเปลี่ยน Formatter

### เซลล์ที่ 7 — สร้าง Formatter สำหรับเวลา

ฟังก์ชันนี้รับค่าตัวเลขแล้วคืนข้อความสำหรับแสดงข้าง Tick โดยไม่ได้วาดกราฟหรือเปลี่ยนค่าข้อมูล

~~~python
def format_hour(value, position):
    # เช่น value=4 -> "04:00"; 02d เติม 0 ให้จำนวนเต็มครบสองหลัก
    return f"{int(round(value)):02d}:00"
~~~

Matplotlib ส่งข้อมูลให้ Function สองค่า:

- `value` คือค่าของ Tick บนแกน เช่น `4.0`
- `position` คือลำดับของ Tick ที่กำลัง Format

ตัวอย่างนี้ไม่ได้ใช้ `position` แต่ยังต้องรับ Parameter ไว้ตามรูปแบบที่ `FuncFormatter` เรียก

ตัวอย่างผลลัพธ์: `format_hour(4, 0)` ได้ `"04:00"` และ `format_hour(12, 0)` ได้ `"12:00"`

ฟังก์ชันแบบสั้นนี้ใช้กับ Major Tick ที่เป็นชั่วโมงเต็มในบทนี้ ไม่ได้แปลงเศษชั่วโมงเป็นนาที และแสดงปลายวันเป็น `24:00` หากจะใช้กับ Tick เช่น `4.5` ต้องปรับฟังก์ชันเพิ่มเติม

### เซลล์ที่ 8 — นำ Function ไปใช้กับ Major Tick

เพิ่ม Formatter ให้แกน X โดยยังใช้ Locator เดิม:

~~~python
# ส่งตัวฟังก์ชันให้ Matplotlib เรียกทีละ Tick ไม่เขียน format_hour()
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_hour))
~~~

<details>
<summary>โค้ดเต็มเซลล์ที่ 8 — รันหลังเซลล์ที่ 1–2 และฟังก์ชันในเซลล์ที่ 7</summary>

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
    mticker.FuncFormatter(format_hour)  # เปลี่ยนข้อความโดยไม่ย้ายขีด
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

</details>

ผลที่ควรเห็น: ตำแหน่งขีดและเส้นอุณหภูมิเหมือนเดิม แต่ตัวเลข `0, 4, 8, ...` กลายเป็น `00:00, 04:00, 08:00, ...`

ลำดับการทำงานคือ:

~~~text
ช่วงแกน X
→ Locator เลือกตำแหน่ง 0, 4, 8, 12, ...
→ Formatter รับค่าทีละตำแหน่ง
→ แสดงเป็น 00:00, 04:00, 08:00, 12:00, ...
~~~

Formatter เปลี่ยนเฉพาะข้อความที่แสดง ค่าใน Array `hours` ยังคงเป็นตัวเลขเดิม

ลองเปลี่ยนค่า: แก้เฉพาะบรรทัด `return` เป็น `return f"{int(round(value))} h"` แล้วรันทั้งเซลล์ที่ 7 และ 8 ใหม่ จะเห็น `0 h, 4 h, 8 h, ...` ที่ตำแหน่งเดิม

---

## 6. ลดจำนวน Tick ใน Dashboard

เมื่อ Axes มีขนาดเล็ก Tick แบบอัตโนมัติอาจแน่นเกินไป `MaxNLocator` ช่วยจำกัดจำนวนช่วงและยังเลือกค่าที่อ่านง่ายให้

### เซลล์ที่ 9 — ใช้ `MaxNLocator` กับกราฟ 2×2

ตัวอย่างนี้ใช้ `MaxNLocator` ลดความแน่นของตัวเลขบนแกนในกริดขนาด 2×2

คำสั่งกำหนด Locator ของแกน Y ภายในลูป:

~~~python
# ขอให้แบ่งแกน Y เป็นไม่เกิน 4 ช่วง โดยให้ Matplotlib เลือกค่าที่อ่านง่าย
ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4))
~~~

`nbins` นับ **ช่วงระหว่างขีด** ไม่ใช่จำนวนขีด เช่น `0 — 5 — 10 — 15 — 20` มี 4 ช่วง แต่มี 5 ขีด จำนวนขีดที่แสดงจริงขึ้นอยู่กับช่วงแกนและค่าที่ Locator เลือก ดูหลักการใน [`MaxNLocator`](https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.MaxNLocator)

<details>
<summary>โค้ดเต็มเซลล์ที่ 9 — รันหลังเซลล์ที่ 1–2</summary>

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

# แกน X ใช้ร่วมกันเพราะ sharex=True จึงตั้งผ่านกราฟเดียวก็พอ
axes[-1, 0].xaxis.set_major_locator(
    mticker.MaxNLocator(nbins=4, integer=True)
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
    # จำกัดจำนวนช่วงบนแกน Y ของแต่ละกราฟ
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

</details>

ผลที่ควรเห็น: แต่ละแกน Y มีตัวเลขห่างพออ่าน ไม่จำเป็นต้องใช้ค่า Tick ชุดเดียวกัน เพราะหน่วยและช่วงข้อมูลต่างกัน ส่วนแกน X ยังใช้ช่วง 0–24 ชั่วโมงร่วมกัน

ลองเปลี่ยนค่า: เปลี่ยนเฉพาะ `nbins=4` ของแกน Y เป็น `2` แล้วเป็น `8` และรันโค้ดเต็มใหม่แต่ละครั้ง เปรียบเทียบความแน่นของตัวเลข ไม่ใช่รูปร่างเส้นข้อมูล

`integer=True` ขอให้ Locator เลือกค่าจำนวนเต็มเมื่อช่วงข้อมูลเอื้ออำนวย เหมาะกับแกนชั่วโมงในตัวอย่างนี้ แต่ไม่ควรใช้กับข้อมูลที่ต้องแสดงทศนิยมละเอียด

<details>
<summary>รายละเอียดเสริม: เหตุใดจำนวน Tick จึงไม่ตายตัว</summary>

Locator อาจผ่อนเงื่อนไข `nbins` หรือ `integer` เพื่อให้มี Tick ขั้นต่ำตาม `min_n_ticks` จึงควรมอง `nbins` เป็นกติกาควบคุมความแน่น ไม่ใช่การสั่งจำนวนขีดตายตัว

</details>

---

## 7. ซ่อน Label หรือซ่อน Tick ทั้งชุด

สองคำสั่งนี้มีผลต่างกัน:

- `NullFormatter()` คืนข้อความว่าง แต่ Locator ยังมีตำแหน่ง Tick
- `NullLocator()` ไม่สร้างตำแหน่ง Tick จึงไม่มี Tick, Label และ Grid ที่ผูกกับตำแหน่งนั้น

### เซลล์ที่ 10 — เปรียบเทียบแบบข้างกัน

ตัวอย่างนี้เปรียบเทียบผลของทั้งสองคำสั่งบน **แกน X เหมือนกันทั้งสองกราฟ** โดยใช้ข้อมูลและช่วงแกนเดียวกัน

คำสั่งที่ใช้เปรียบเทียบ:

~~~python
# ซ้าย: ไม่แสดงข้อความ แต่ยังมีตำแหน่งขีด
axes[0].xaxis.set_major_formatter(mticker.NullFormatter())

# ขวา: ไม่มีตำแหน่งขีดหลัก จึงไม่มีข้อความและ Grid ที่อ้างถึงขีดหลักนั้น
axes[1].xaxis.set_major_locator(mticker.NullLocator())
~~~

<details>
<summary>โค้ดเต็มเซลล์ที่ 10 — รันหลังเซลล์ที่ 1–2</summary>

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
        ylabel="Temperature (°C)",
        xlim=(0, 24),
    )
    ax.xaxis.set_major_locator(mticker.MultipleLocator(4))
    # ปิด Minor Ticks เพื่อให้ดูผลของ Major Ticks อย่างเดียว
    ax.xaxis.set_minor_locator(mticker.NullLocator())
    ax.grid(alpha=0.25)

# ซ่อนเฉพาะข้อความแกน X
axes[0].xaxis.set_major_formatter(
    mticker.NullFormatter()
)
axes[0].set_title(
    "NullFormatter: positions remain"
)

# เอาตำแหน่ง Major Tick บนแกน X ออก
axes[1].xaxis.set_major_locator(
    mticker.NullLocator()
)
axes[1].set_title(
    "NullLocator: positions disappear"
)

plt.show()
~~~

</details>

ผลที่ควรเห็น — มองที่แกน X และเส้นตารางแนวตั้ง:

| สิ่งที่สังเกต | ซ้าย: `NullFormatter` | ขวา: `NullLocator` |
|---|---|---|
| ตัวเลขใต้แกน X | ไม่มี | ไม่มี |
| ขีดหลักบนแกน X | ยังอยู่ | ไม่มี |
| Grid แนวตั้งของขีดหลัก | ยังอยู่ | ไม่มี |

เส้นข้อมูล เส้นขอบกราฟ ชื่อแกน และแกน Y ยังอยู่ทั้งสองช่อง คำสั่งเหล่านี้ไม่ได้ลบกราฟหรือแกนทั้งเส้น

ลองเปลี่ยนค่า: คอมเมนต์คำสั่ง `set_major_formatter(...)` ของช่องซ้ายทั้งชุดแล้วรันใหม่ ตัวเลขจะกลับมา โดยขีดและ Grid อยู่ที่เดิม

หากต้องการเพียงไม่แสดง Label ของบางช่องในกริด ใช้ `tick_params(labelbottom=False)` ได้ โดยไม่ต้องเปลี่ยน Formatter ที่อาจใช้ร่วมกันผ่าน `sharex=True` ตัวอย่างเปรียบเทียบนี้จึงไม่เปิด `sharex`

---

## 8. Tick ของข้อมูลแบบหมวดหมู่

Dock (อ่านว่า “ด็อก”) ในตัวอย่างนี้คือช่องจอดรถสำหรับขนถ่ายสินค้า แต่ละแท่งแสดงเวลาขนถ่ายเฉลี่ยของช่อง A–D แกน X แสดงชื่อช่อง ส่วนแกน Y แสดงเวลาในหน่วยนาที

### เซลล์ที่ 11 — จับคู่ตำแหน่งกับชื่อ Dock

`set_xticks(..., labels=...)` จับคู่ **ตำแหน่ง** กับ **ข้อความ** ในคำสั่งเดียว:

~~~text
ตำแหน่ง:   0         1         2         3
ข้อความ: Dock A    Dock B    Dock C    Dock D
~~~

คำสั่งจับคู่ตำแหน่งกับชื่อ:

~~~python
ax.set_xticks(
    positions,          # 0, 1, 2, 3: ตำแหน่งเดียวกับที่ใช้วาดแท่ง
    labels=dock_names,   # ข้อความที่ต้องการให้แสดงใต้แต่ละตำแหน่ง
)
~~~

<details>
<summary>โค้ดเต็มเซลล์ที่ 11 — รันหลัง Import ในเซลล์ที่ 1; ไม่ต้องใช้ข้อมูลห้องเย็น</summary>

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

# ตำแหน่งแท่งยังเป็นตัวเลข แต่ข้อความใต้แท่งเป็นชื่อ Dock
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
        nbins=5,  # จำกัดจำนวนช่วงบนแกน Y
        integer=True,
    )
)
ax.grid(
    axis="y",
    alpha=0.20,
)

plt.show()
~~~

</details>

ผลที่ควรเห็น: ใต้แท่งเป็น `Dock A`, `Dock B`, `Dock C`, `Dock D` ไม่ใช่ตำแหน่ง `0, 1, 2, 3` ส่วนความสูงยังเป็น `31, 26, 38, 29` นาทีเหมือนเดิม

ลองเปลี่ยนค่า: แก้ชื่อ `"Dock A"` เป็น `"Gate A"` แล้วรันใหม่ จะเปลี่ยนเฉพาะชื่อใต้แท่ง ไม่เปลี่ยนตำแหน่งหรือความสูงแท่ง

หากจำนวน Label ไม่เท่ากับจำนวนตำแหน่ง Matplotlib จะรายงานข้อผิดพลาด จึงควรส่ง `positions` และ `labels` พร้อมกัน แทนการเรียก `set_xticklabels()` เพียงอย่างเดียว

---

## 9. เลือก Locator และ Formatter อย่างไร

ตารางต่อไปนี้สรุปเครื่องมือสำหรับกำหนดตำแหน่ง Tick และรูปแบบข้อความตามลักษณะของแกน

<details>
<summary>เปิดตารางเครื่องมือเพิ่มเติมและตัวอย่าง Log Scale</summary>

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

สำหรับแกนที่เป็นอิสระจากกัน ไม่ควรนำ Locator Object เดียวไปใช้ร่วมกัน ให้สร้าง Instance ใหม่สำหรับแต่ละ Axis ส่วนกราฟที่ใช้ `sharex=True` จะแชร์ Locator/Formatter ของแกน X อยู่แล้ว จึงตั้งผ่านกราฟหนึ่งในกลุ่มได้เหมือนเซลล์ที่ 9

<details>
  <summary>ตัวอย่างเพิ่มเติม: Tick บน Log Scale</summary>

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

<details>
<summary>รายละเอียดและตัวอย่างข้อผิดพลาด</summary>

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

</details>

---

## 12. Export และตรวจผลงาน

ใช้ `fig` ของกราฟที่ต้องการบันทึก และวาง `fig.savefig(...)` **ก่อน `plt.show()` ในโค้ดเต็มตัวอย่างนั้น**

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
3. เปรียบเทียบ `set_xticks()` กับ `MultipleLocator` หลังขยายช่วงเป็น `xlim=(0, 32)` แล้วสังเกตตำแหน่ง 28 และ 32
4. เขียน `FuncFormatter` ให้แสดงเวลาแบบ `8 AM`, `12 PM`, `4 PM`
5. ทดลอง `MaxNLocator(nbins=3)`, `nbins=5` และ `nbins=8`
6. ใช้ `NullFormatter` ซ่อน Label แกน X แล้วตรวจว่า Grid ยังอยู่หรือไม่
7. ใช้ `NullLocator` กับแกนเดียวกันและอธิบายความต่าง
8. สร้าง Bar Chart ชื่อคลังสินค้าโดยกำหนดตำแหน่งและ Label พร้อมกัน

อ่านโจทย์ฉบับเต็มได้ที่ [แบบฝึกหัด EP10](./exercises/exercise01.md)

## สคริปต์ฉบับเต็ม

รันสคริปต์ได้จากโฟลเดอร์หลักของ Repository เช่น:

~~~bash
python ep10-customizing-ticks/source-code/major_minor_ticks.py
~~~

- [cold_chain_data.py](./source-code/cold_chain_data.py) — สร้างข้อมูลสังเคราะห์
- [major_minor_ticks.py](./source-code/major_minor_ticks.py) — Major และ Minor Ticks
- [custom_time_formatter.py](./source-code/custom_time_formatter.py) — Formatter สำหรับเวลา
- [small_multiples_ticks.py](./source-code/small_multiples_ticks.py) — ลด Tick ใน Dashboard
- [hide_ticks_labels.py](./source-code/hide_ticks_labels.py) — เปรียบเทียบ NullFormatter และ NullLocator
- [cold_chain_tick_dashboard.py](./source-code/cold_chain_tick_dashboard.py) — ตัวอย่างรวมสำหรับต่อยอด

## สรุป

Locator เลือกตำแหน่ง Tick, Formatter กำหนดข้อความข้าง Tick และ `tick_params()` ปรับรูปลักษณ์ของขีด การปรับทั้งสามส่วนนี้ไม่เปลี่ยนค่าข้อมูลที่ใช้วาดกราฟ

## เอกสาร Matplotlib ที่เกี่ยวข้อง

- [Axis ticks](https://matplotlib.org/stable/users/explain/axes/axes_ticks.html)
- [`matplotlib.ticker`](https://matplotlib.org/stable/api/ticker_api.html)
- [`Axes.tick_params`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html)
- [Tick formatters gallery](https://matplotlib.org/stable/gallery/ticks/tick-formatters.html)

## ตอนก่อนหน้า

**EP9 — [Text and Annotation for Solar Power Plant Operations](../ep09-text-and-annotation/README.md)**

## ตอนถัดไป

**EP11 — [Customizing Matplotlib: Configurations and Stylesheets](../ep11-configurations-and-stylesheets/README.md)**

