# EP9 — Text and Annotation for Solar Power Plant Operations

กราฟที่ดีไม่ได้เพียงแสดงเส้นหรือจุด แต่ช่วยให้คนอ่านเห็นว่าเหตุการณ์ใดสำคัญ เกิดขึ้นเมื่อใด และควรพิจารณาข้อมูลส่วนใดก่อน บางกราฟใช้เพียงชื่อและหน่วยก็เพียงพอ ขณะที่กราฟสำหรับงานปฏิบัติการอาจต้องมีข้อความสั้น ลูกศร ช่วงเวลาเหตุการณ์ หรือหมายเหตุระดับ Figure เพิ่มเติม

บทนี้ใช้ **ระบบติดตามโรงไฟฟ้าพลังงานแสงอาทิตย์** เป็นกรณีศึกษา เพื่อเรียนรู้การวางข้อความด้วย `text()` การเลือก Coordinate System และการชี้เหตุการณ์ด้วย `annotate()` ตั้งแต่ตัวอย่างพื้นฐานไปจนถึง Operations Dashboard ที่มีหลาย Axes

ตัวอย่าง ข้อมูล สูตรจำลอง และคำอธิบายทั้งหมดเรียบเรียงขึ้นใหม่สำหรับชุดวิดีโอนี้ ข้อมูลเป็นข้อมูลสังเคราะห์ ไม่ได้มาจากโรงไฟฟ้าจริง ค่า Reference และเหตุการณ์ในบทมีไว้สอน Matplotlib เท่านั้น ไม่ควรนำไปใช้เป็นเกณฑ์ควบคุมระบบไฟฟ้าหรือประเมินประสิทธิภาพอุปกรณ์จริง

## วิธีเรียนจากบทนี้

- รันเซลล์ตามลำดับจากบนลงล่าง
- แยกให้ออกก่อนว่าข้อความต้องผูกกับข้อมูล ผูกกับ Axes หรือผูกกับ Figure
- เริ่มจาก `ax.text()` แล้วจึงเพิ่ม `ax.annotate()` เมื่อต้องมีลูกศร
- ทดลอง Zoom หรือเปลี่ยน `xlim` เพื่อดูผลของ Coordinate System
- ใช้ Annotation เท่าที่จำเป็นและตรวจกราฟหลัง Export ทุกครั้ง
- สคริปต์ฉบับเต็มอยู่ในโฟลเดอร์ [source-code](./source-code/)

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบบทนี้ จะสามารถ:

- ตั้งชื่อ Figure, Axes และแกนข้อมูลให้สื่อความหมายพร้อมหน่วย
- วางข้อความด้วย `ax.text()`
- ปรับ Font, สี, Alignment, Rotation และกล่องข้อความ
- อธิบายความแตกต่างระหว่าง `ax.transData`, `ax.transAxes` และ `fig.transFigure`
- เลือก Coordinate System ให้ตรงกับหน้าที่ของข้อความ
- ใช้ `ax.annotate()` แยกตำแหน่งข้อมูลออกจากตำแหน่งข้อความ
- วางข้อความเยื้องจากจุดข้อมูลด้วย `textcoords="offset points"`
- ปรับลูกศรด้วย `arrowprops`
- ใช้ `bbox` เพิ่มพื้นหลังให้ข้อความอ่านง่าย
- ใช้ Blended Transform สำหรับข้อความที่ผูกกับค่าบนแกนเพียงด้านเดียว
- คำนวณตำแหน่ง Annotation จากข้อมูลแทนการเดาตำแหน่งด้วยตนเอง
- สร้าง Dashboard โรงไฟฟ้าที่มีข้อความและ Annotation โดยไม่ทำให้กราฟแน่นเกินไป

## คำศัพท์สำคัญก่อนเริ่ม

| คำศัพท์ | ความหมาย |
|---------|----------|
| Text | ข้อความที่วางบน Axes หรือ Figure |
| Annotation | ข้อความที่อธิบายตำแหน่งหรือเหตุการณ์ ซึ่งอาจมีลูกศรเชื่อมไปยังข้อมูล |
| Coordinate system | กติกาที่กำหนดว่าคู่ตัวเลข `(x, y)` อ้างอิงพื้นที่ใด |
| Transform | Object ที่แปลงพิกัดจากระบบหนึ่งไปยังตำแหน่งแสดงผล |
| Data coordinates | พิกัดตามค่าจริงของแกน X และ Y |
| Axes coordinates | พิกัดสัดส่วนภายใน Axes ตั้งแต่ 0 ถึง 1 |
| Figure coordinates | พิกัดสัดส่วนของ Figure ทั้งภาพตั้งแต่ 0 ถึง 1 |
| Offset points | ระยะเยื้องจากตำแหน่งอ้างอิง มีหน่วยเป็น Point |
| `xy` | จุดข้อมูลที่ Annotation ต้องการชี้ |
| `xytext` | ตำแหน่งที่วางข้อความ Annotation |
| `bbox` | กล่องพื้นหลังหรือกรอบรอบข้อความ |
| `arrowprops` | Dictionary สำหรับกำหนดหน้าตาและเส้นทางของลูกศร |

---

## 1. เตรียมไลบรารีและข้อมูล Solar Farm

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
~~~

ติดตั้งไลบรารีได้ด้วย:

~~~bash
python -m pip install numpy matplotlib
~~~

บทนี้ไม่ต้องดาวน์โหลด Dataset ภายนอก ทุกค่าถูกสร้างขึ้นด้วย NumPy และกำหนด Seed เพื่อให้ได้ผลซ้ำเดิม

### เซลล์ที่ 2 — สร้างข้อมูลหนึ่งวัน

~~~python
rng = np.random.default_rng(9)

hours = np.arange(
    5.5,
    18.5 + 1 / 60,
    1 / 6,
)

sunrise = 5.75
sunset = 18.25

daylight_phase = np.clip(
    (hours - sunrise) / (sunset - sunrise),
    0,
    1,
)

solar_shape = np.sin(
    np.pi * daylight_phase
) ** 1.45

clear_sky_power = 5200 * solar_shape
~~~

แกนเวลาเริ่มที่ 05:30 และสิ้นสุดที่ 18:30 โดยเพิ่มครั้งละ `1 / 6` ชั่วโมง หรือ 10 นาที

- `daylight_phase` แปลงช่วงพระอาทิตย์ขึ้นถึงตกให้อยู่ระหว่าง 0–1
- `solar_shape` สร้างเส้นโค้งจำลองที่เพิ่มขึ้นในตอนเช้า สูงช่วงกลางวัน และลดลงช่วงเย็น
- `clear_sky_power` เป็นกำลังผลิตอ้างอิงในวันที่สมมติว่าท้องฟ้าโปร่ง
- กำลังสูงสุด 5,200 kW เป็นค่าที่ตั้งขึ้นเพื่อการสอน ไม่ใช่ Rating ของโรงไฟฟ้าจริง

### เซลล์ที่ 3 — เพิ่มเมฆและช่วงตรวจสอบ Inverter

~~~python
morning_cloud = 0.28 * np.exp(
    -((hours - 9.1) / 0.35) ** 2
)

afternoon_cloud = 0.42 * np.exp(
    -((hours - 14.3) / 0.45) ** 2
)

cloud_factor = np.clip(
    1 - morning_cloud - afternoon_cloud,
    0.35,
    1,
)

maintenance_mask = (
    (hours >= 12.0)
    & (hours <= 12.4)
)

operating_factor = np.ones(hours.size)
operating_factor[maintenance_mask] = 0.68

ac_power = np.clip(
    clear_sky_power
    * cloud_factor
    * operating_factor
    + rng.normal(0, 55, hours.size)
    * solar_shape,
    0,
    None,
)
~~~

ข้อมูลถูกออกแบบให้มีเหตุการณ์ที่มองเห็นได้สามช่วง:

- เมฆช่วงเช้าประมาณ 09:06
- ช่วงตรวจสอบ Inverter ระหว่าง 12:00–12:24
- เมฆช่วงบ่ายประมาณ 14:18

เหตุการณ์เหล่านี้มีไว้ให้ฝึกวาง Annotation โดยรู้สาเหตุที่ใช้สร้างข้อมูลอยู่แล้ว ในงานจริงต้องตรวจ Event Log, Weather Data และสถานะอุปกรณ์ก่อนสรุปสาเหตุจากรูปทรงของกราฟ

### เซลล์ที่ 4 — สร้างข้อมูลอุณหภูมิ

~~~python
ambient_temperature = (
    24
    + 10 * solar_shape
    + rng.normal(0, 0.35, hours.size)
)

inverter_temperature = (
    ambient_temperature
    + 7
    + 8 * ac_power / 5200
    + rng.normal(0, 0.45, hours.size)
)
~~~

อุณหภูมิ Inverter ถูกสมมติให้สัมพันธ์กับอุณหภูมิแวดล้อมและสัดส่วนกำลังผลิต สูตรนี้เป็นเพียงตัวสร้างข้อมูล ไม่ใช่ Thermal Model ของ Inverter

ตรวจ Shape และช่วงค่าได้ด้วย:

~~~python
print("Samples:", hours.size)
print("Power shape:", ac_power.shape)
print("Peak power:", ac_power.max())
print(
    "Peak inverter temperature:",
    inverter_temperature.max(),
)
~~~

---

## 2. เริ่มจากชื่อกราฟและชื่อแกน

ก่อนเพิ่มข้อความภายในกราฟ ควรทำองค์ประกอบพื้นฐานให้ครบก่อน ได้แก่ชื่อกราฟ ชื่อแกน และหน่วย

### เซลล์ที่ 5 — กราฟกำลังผลิตพื้นฐาน

~~~python
fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    ac_power,
    color="tab:orange",
    linewidth=2.2,
)

ax.set(
    title="Solar Farm AC Power — One Operating Day",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(5.5, 18.5),
)

ax.grid(alpha=0.25)
plt.show()
~~~

`ax.set()` ช่วยกำหนด Property หลายรายการในครั้งเดียว คำสั่งด้านบนให้ข้อมูลพื้นฐานสามอย่างแก่คนอ่านกราฟ:

- กราฟแสดงอะไร
- แกน X คือเวลาแบบใด
- แกน Y วัดค่าอะไรและใช้หน่วยใด

ชื่อและหน่วยไม่ใช่ Annotation ของเหตุการณ์ แต่เป็นส่วนประกอบพื้นฐานที่ควรมีอยู่ก่อนแล้ว หากชื่อแกนยังไม่ชัด การเพิ่มลูกศรจำนวนมากก็ไม่ช่วยให้กราฟสื่อสารได้ดีขึ้น

---

## 3. วางข้อความด้วย `ax.text()`

รูปแบบหลักของ Method คือ:

~~~python
ax.text(x, y, "ข้อความ")
~~~

โดยค่า `x` และ `y` ใช้ Data Coordinates เป็นค่าเริ่มต้น หมายความว่าตัวเลขต้องอยู่ใน Scale เดียวกับข้อมูลบนแกน

### เซลล์ที่ 6 — เขียนข้อความใกล้ช่วงเมฆบังแผง

~~~python
cloud_index = np.abs(
    hours - 14.3
).argmin()

ax.text(
    hours[cloud_index],
    ac_power[cloud_index] + 380,
    "Afternoon cloud passage",
    fontsize=10,
    color="tab:blue",
    fontweight="bold",
    ha="center",
)
~~~

ตำแหน่ง X มาจากเวลาที่ใกล้ 14.3 ชั่วโมงที่สุด ส่วนตำแหน่ง Y ใช้ค่ากำลังผลิต ณ จุดนั้นบวก 380 kW เพื่อให้ข้อความอยู่เหนือเส้น

Parameter ที่ใช้บ่อยมีดังนี้:

| Parameter | หน้าที่ |
|-----------|--------|
| `fontsize` | ขนาดตัวอักษร |
| `color` | สีข้อความ |
| `fontweight` | น้ำหนักตัวอักษร เช่น `"normal"` หรือ `"bold"` |
| `fontstyle` | รูปแบบ เช่น `"normal"` หรือ `"italic"` |
| `ha` | Horizontal Alignment: `"left"`, `"center"`, `"right"` |
| `va` | Vertical Alignment: `"top"`, `"center"`, `"bottom"`, `"baseline"` |
| `rotation` | มุมหมุนข้อความเป็นองศา |
| `alpha` | ความทึบตั้งแต่ 0–1 |
| `bbox` | กล่องพื้นหลังรอบข้อความ |
| `transform` | Coordinate System ที่ใช้ตีความ `(x, y)` |

### ใช้ Dictionary ลดการเขียน Style ซ้ำ

~~~python
text_style = {
    "fontsize": 10,
    "color": "tab:blue",
    "fontweight": "bold",
    "ha": "center",
}

ax.text(
    hours[cloud_index],
    ac_power[cloud_index] + 380,
    "Afternoon cloud passage",
    **text_style,
)
~~~

`**text_style` กระจายคู่ Key–Value ใน Dictionary ให้เป็น Keyword Arguments รูปแบบนี้ช่วยให้ข้อความหลายรายการใช้ Style สอดคล้องกัน

### `ha` และ `va` อ้างอิงจุดใด

คู่พิกัด `(x, y)` เป็นจุดยึดของข้อความ ไม่ได้หมายถึงมุมซ้ายล่างเสมอไป

- `ha="left"` ให้ขอบซ้ายของข้อความอยู่ที่ค่า X
- `ha="center"` ให้กึ่งกลางข้อความอยู่ที่ค่า X
- `ha="right"` ให้ขอบขวาของข้อความอยู่ที่ค่า X
- `va="top"` ให้ขอบบนของข้อความอยู่ที่ค่า Y
- `va="bottom"` ให้ขอบล่างของข้อความอยู่ที่ค่า Y

เมื่อข้อความดูเยื้องจากตำแหน่งที่คาด ให้ตรวจ Alignment ก่อนแก้ตัวเลขพิกัด

---

## 4. Coordinate System คือกุญแจของตำแหน่งข้อความ

คำสั่งเดียวกันอาจใช้ตัวเลข `(0.5, 0.5)` แต่ได้ตำแหน่งต่างกัน เพราะ Coordinate System เป็นผู้กำหนดความหมายของตัวเลข

~~~text
ค่าที่เขียนในโค้ด
        ↓
Coordinate System
        ↓
Transform คำนวณตำแหน่ง
        ↓
ตำแหน่งบนหน้าจอหรือไฟล์ภาพ
~~~

สามระบบที่ใช้บ่อยมีดังนี้:

| ระบบพิกัด | Transform | ความหมายของ `(x, y)` | เหมาะกับ |
|-----------|-----------|------------------------|----------|
| Data | `ax.transData` | ค่าจริงตามแกน X และ Y | ชื่อเหตุการณ์หรือค่าที่ผูกกับข้อมูล |
| Axes | `ax.transAxes` | สัดส่วนภายใน Axes จาก 0–1 | รหัส Panel, สถานะ, หมายเหตุประจำกราฟ |
| Figure | `fig.transFigure` | สัดส่วนของ Figure จาก 0–1 | แหล่งข้อมูล หมายเหตุรวม Branding |

### พิกัด Axes และ Figure อ่านอย่างไร

สำหรับ Axes Coordinates:

~~~text
(0, 1) ┌────────────────────┐ (1, 1)
       │                    │
       │     (0.5, 0.5)     │
       │                    │
(0, 0) └────────────────────┘ (1, 0)
~~~

- `(0, 0)` คือมุมซ้ายล่าง
- `(1, 1)` คือมุมขวาบน
- `(0.5, 0.5)` คือกึ่งกลาง
- `(0.02, 0.95)` คือ 2% จากซ้าย และ 95% จากล่าง

ตัวเลขเหล่านี้ไม่ใช่ชั่วโมงหรือ kW เมื่อใช้ `ax.transAxes`

### เซลล์ที่ 7 — ทดลองสาม Coordinate Systems

~~~python
fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    ac_power,
    color="tab:orange",
    linewidth=2.2,
)

maintenance_index = np.abs(
    hours - 12.2
).argmin()

ax.text(
    hours[maintenance_index],
    ac_power[maintenance_index],
    "  Data position",
    transform=ax.transData,
    color="tab:red",
    va="bottom",
)

ax.text(
    0.02,
    0.95,
    "Plant ID: SOLAR-09",
    transform=ax.transAxes,
    va="top",
)

fig.text(
    0.99,
    0.01,
    "Synthetic training data",
    ha="right",
    va="bottom",
    fontsize=9,
    color="0.35",
)

ax.set(
    title="Three Coordinate Systems for Text",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(5.5, 18.5),
)
ax.grid(alpha=0.25)

plt.show()
~~~

ข้อความทั้งสามมีหน้าที่ต่างกัน:

- `Data position` ต้องตามเหตุการณ์บนเส้น จึงใช้ Data Coordinates
- `Plant ID` ควรอยู่มุมเดิมของ Axes จึงใช้ Axes Coordinates
- `Synthetic training data` เป็นหมายเหตุของภาพทั้งหมด จึงใช้ `fig.text()`

`fig.text()` ใช้ Figure Coordinates เป็นค่าเริ่มต้นอยู่แล้ว จึงไม่จำเป็นต้องเขียน `transform=fig.transFigure` ทุกครั้ง แต่สามารถระบุให้เห็นชัดได้เมื่อต้องการสอนหรืออ่านโค้ดร่วมกับ Transform อื่น

---

## 5. เมื่อ Zoom แล้วข้อความใดควรขยับ

ข้อความใน Data Coordinates ผูกกับค่าบนแกน เมื่อเปลี่ยน `xlim` หรือ `ylim` ตำแหน่งบนหน้าจอจึงเปลี่ยนตามข้อมูล ส่วนข้อความใน Axes Coordinates จะยังอยู่ที่สัดส่วนเดิมของกรอบกราฟ

### เซลล์ที่ 8 — เปรียบเทียบมุมมองเต็มวันกับช่วงกลางวัน

~~~python
fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 4.5),
    layout="constrained",
)

event_index = np.abs(
    hours - 12.2
).argmin()

for ax in axes:
    ax.plot(
        hours,
        ac_power,
        color="tab:orange",
    )
    ax.text(
        hours[event_index],
        ac_power[event_index],
        "Data",
        color="tab:red",
        transform=ax.transData,
    )
    ax.text(
        0.02,
        0.95,
        "Axes",
        transform=ax.transAxes,
        va="top",
        fontweight="bold",
    )
    ax.grid(alpha=0.25)

axes[0].set(
    title="Full day",
    xlim=(5.5, 18.5),
)

axes[1].set(
    title="Zoom: 11:00–15:00",
    xlim=(11, 15),
)

plt.show()
~~~

คำว่า `Data` ยังชี้ค่าประมาณ 12:12 เหมือนเดิม แต่ตำแหน่งบนหน้าจอเปลี่ยนเพราะช่วงแกน X เปลี่ยน ส่วนคำว่า `Axes` อยู่มุมซ้ายบนของแต่ละ Axes เหมือนเดิม

หลักเลือกอย่างสั้น:

- ถ้าข้อความต้องตามจุดข้อมูล ให้ใช้ Data Coordinates
- ถ้าข้อความต้องอยู่มุมเดิมของกราฟ ให้ใช้ Axes Coordinates
- ถ้าข้อความอธิบายทั้งภาพ ให้ใช้ Figure Coordinates

---

## 6. ชี้จุดสำคัญด้วย `ax.annotate()`

`ax.text()` วางข้อความได้ แต่ไม่ได้แยกจุดที่ต้องการอธิบายออกจากตำแหน่งข้อความอย่างชัดเจน `ax.annotate()` เหมาะกว่าเมื่อข้อความต้องชี้กลับไปยังข้อมูล

### เซลล์ที่ 9 — ชี้กำลังผลิตสูงสุด

~~~python
peak_index = int(ac_power.argmax())

peak_xy = (
    hours[peak_index],
    ac_power[peak_index],
)

fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    ac_power,
    color="tab:orange",
    linewidth=2.2,
)

ax.annotate(
    f"Peak {ac_power[peak_index]:.0f} kW",
    xy=peak_xy,
    xytext=(13.2, 5550),
    arrowprops={
        "arrowstyle": "->",
        "color": "black",
    },
)

ax.set(
    title="Peak Solar-Farm Output",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(5.5, 18.5),
)
ax.grid(alpha=0.25)

plt.show()
~~~

องค์ประกอบหลักคือ:

- `xy` คือจุดที่ต้องการชี้
- `xytext` คือตำแหน่งข้อความ
- `arrowprops` เปิดใช้และปรับลูกศร

เมื่อไม่ได้กำหนด `xycoords` ค่า `xy` จะใช้ Data Coordinates และเมื่อไม่ได้กำหนด `textcoords` ค่า `xytext` จะใช้ระบบเดียวกับ `xycoords`

ข้อดีของการหา `peak_index` ด้วย `argmax()` คือ Annotation จะตามค่าสูงสุดของข้อมูล หากเปลี่ยน Seed หรือข้อมูลใหม่ ไม่ต้องแก้ตำแหน่ง `xy` ด้วยตนเอง

---

## 7. แยกตำแหน่งข้อมูลกับระยะเยื้องของข้อความ

การกำหนด `xytext` เป็นค่าข้อมูลโดยตรงอาจต้องแก้ใหม่เมื่อช่วงแกนเปลี่ยน วิธีที่ใช้ได้สะดวกในหลายกรณีคือให้ `xy` อยู่ใน Data Coordinates แต่ให้ข้อความเยื้องจากจุดนั้นเป็นจำนวน Point

### เซลล์ที่ 10 — ใช้ `offset points`

~~~python
ax.annotate(
    f"Peak {ac_power[peak_index]:.0f} kW",
    xy=peak_xy,
    xytext=(25, 35),
    textcoords="offset points",
    ha="left",
    arrowprops={
        "arrowstyle": "->",
        "color": "black",
    },
)
~~~

ความหมายคือ:

- จุดที่ชี้ยังเป็นชั่วโมงและกำลังผลิตจริง
- ข้อความอยู่ขวา 25 Point และสูงขึ้น 35 Point จากจุดนั้น
- Point เป็นหน่วยงานพิมพ์ โดย 72 Point เท่ากับ 1 นิ้ว

วิธีนี้ช่วยให้ระยะระหว่างจุดกับข้อความค่อนข้างคงที่เมื่อเปลี่ยน Scale ของข้อมูล แต่ยังต้องตรวจว่าข้อความไม่ชนขอบ Figure หลัง Export

---

## 8. Annotation หลายเหตุการณ์ด้วย List และ Loop

เมื่อมีหลายเหตุการณ์ ไม่ควร Copy-paste คำสั่ง `annotate()` ทั้งชุด ให้เก็บสิ่งที่ต่างกันไว้ใน List ของ Dictionary แล้ววนลูป

### เซลล์ที่ 11 — เมฆและช่วงตรวจสอบ Inverter

~~~python
fig, ax = plt.subplots(
    figsize=(11, 5.5),
    layout="constrained",
)

ax.plot(
    hours,
    clear_sky_power,
    color="0.65",
    linestyle="--",
    label="Clear-sky reference",
)

ax.plot(
    hours,
    ac_power,
    color="tab:orange",
    linewidth=2.3,
    label="Measured AC power",
)

events = [
    {
        "hour": 9.1,
        "label": "Morning cloud",
        "offset": (-55, -55),
        "color": "tab:blue",
    },
    {
        "hour": 12.2,
        "label": "Inverter inspection",
        "offset": (0, -75),
        "color": "tab:red",
    },
    {
        "hour": 14.3,
        "label": "Afternoon cloud",
        "offset": (55, -60),
        "color": "tab:blue",
    },
]

for event in events:
    index = np.abs(
        hours - event["hour"]
    ).argmin()

    xy = (
        hours[index],
        ac_power[index],
    )

    ax.scatter(
        *xy,
        color=event["color"],
        zorder=3,
    )

    ax.annotate(
        event["label"],
        xy=xy,
        xytext=event["offset"],
        textcoords="offset points",
        ha="center",
        fontsize=9,
        bbox={
            "boxstyle": "round,pad=0.3",
            "facecolor": "white",
            "edgecolor": event["color"],
            "alpha": 0.95,
        },
        arrowprops={
            "arrowstyle": "->",
            "color": event["color"],
            "connectionstyle": "arc3,rad=0.15",
        },
    )

ax.set(
    title="Annotated Solar-Farm Operating Events",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(5.5, 18.5),
)
ax.legend()
ax.grid(alpha=0.25)

plt.show()
~~~

รูปแบบข้อมูลภายใน `events` ช่วยแยกสองส่วนออกจากกัน:

- ข้อมูลของเหตุการณ์ เช่น เวลา ชื่อ สี และ Offset
- กติกาการวาด ซึ่งอยู่ใน Loop เพียงชุดเดียว

ถ้าต้องเพิ่มเหตุการณ์ใหม่ ให้เพิ่ม Dictionary อีกหนึ่งรายการ ไม่ต้องคัดลอกโค้ด Plot ทั้งก้อน

---

## 9. ทำให้ข้อความอ่านง่ายด้วย `bbox`

เส้นกราฟและ Grid อาจพาดผ่านตัวอักษร `bbox` ช่วยสร้างพื้นหลังให้ข้อความโดยรับค่าเป็น Dictionary

~~~python
bbox={
    "boxstyle": "round,pad=0.3",
    "facecolor": "white",
    "edgecolor": "tab:blue",
    "linewidth": 1,
    "alpha": 0.9,
}
~~~

Parameter สำคัญมีดังนี้:

| Key | หน้าที่ |
|-----|--------|
| `boxstyle` | รูปร่างกล่องและ Padding |
| `facecolor` | สีพื้นกล่อง |
| `edgecolor` | สีขอบ |
| `linewidth` | ความหนาขอบ |
| `alpha` | ความทึบของกล่อง |

Style ที่ใช้บ่อย ได้แก่ `"square"`, `"round"` และ `"round4"` การเลือกควรสอดคล้องทั้ง Figure ไม่จำเป็นต้องใช้หลายรูปทรงเพื่อแสดงความสามารถทั้งหมดในกราฟเดียว

---

## 10. ปรับลูกศรด้วย `arrowprops`

`arrowprops` เป็น Dictionary ที่ควบคุมลูกศรระหว่าง `xytext` กับ `xy`

~~~python
arrowprops={
    "arrowstyle": "->",
    "color": "tab:red",
    "linewidth": 1.3,
    "connectionstyle": "arc3,rad=0.15",
}
~~~

| Key | หน้าที่ |
|-----|--------|
| `arrowstyle` | รูปแบบหัวและลำตัวลูกศร |
| `color` | สีลูกศร |
| `linewidth` | ความหนาเส้น |
| `connectionstyle` | รูปแบบเส้นเชื่อมระหว่างข้อความกับจุด |
| `shrinkA` | เว้นระยะจากกล่องข้อความ |
| `shrinkB` | เว้นระยะจากจุดที่ชี้ |
| `mutation_scale` | Scale ของหัวลูกศรและองค์ประกอบที่เกี่ยวข้อง |

ตัวอย่างเส้นเชื่อม:

~~~python
"arc3,rad=0.15"   # เส้นโค้งเล็กน้อย
"angle3"          # เส้นหักมุม
"bar,fraction=0.2"  # รูปแบบคล้ายวงเล็บหรือ Bar
~~~

สำหรับ Dashboard จริง ควรเลือก Style หลักหนึ่งแบบและใช้ซ้ำ ความหมายของสีและเส้นสำคัญกว่าความหลากหลายของรูปลูกศร

---

## 11. Blended Transform: ผูก X กับ Axes แต่ผูก Y กับข้อมูล

บางข้อความต้องอยู่ชิดขอบขวาของ Axes เสมอ แต่ระดับแนวตั้งต้องตามค่าจริงบนแกน Y ตัวอย่างเช่น Label ของเส้นอ้างอิงกำลังผลิต

### เซลล์ที่ 12 — ชื่อเส้นอ้างอิงที่ระดับ 4,500 kW

~~~python
reference_power = 4500

fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    ac_power,
    color="tab:orange",
)

ax.axhline(
    reference_power,
    color="tab:red",
    linestyle="--",
)

ax.text(
    0.98,
    reference_power,
    "Dispatch reference",
    transform=ax.get_yaxis_transform(),
    ha="right",
    va="bottom",
    color="tab:red",
)

ax.set(
    title="Label Fixed to the Right Edge",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(5.5, 18.5),
)
ax.grid(alpha=0.25)

plt.show()
~~~

`ax.get_yaxis_transform()` ใช้:

- X เป็น Axes Coordinates ดังนั้น `0.98` คือ 98% ของความกว้าง Axes
- Y เป็น Data Coordinates ดังนั้น `4500` คือระดับ 4,500 kW จริง

ข้อความจึงอยู่ใกล้ขอบขวาแม้เปลี่ยนช่วงแกน X แต่ยังตามระดับเส้นอ้างอิงบนแกน Y

ในระบบจริง ค่า Dispatch Limit, Alarm หรือ Threshold ต้องมาจากข้อกำหนดที่ได้รับอนุมัติ ไม่ควรเลือกตัวเลขจากรูปร่างของกราฟ

---

## 12. สร้าง Function สำหรับ Annotation ที่ใช้ซ้ำ

เมื่อหลายกราฟใช้กติกาเหมือนกัน สามารถรวมการหาจุดและการวาดไว้ใน Function

### เซลล์ที่ 13 — Function `annotate_nearest()`

~~~python
def annotate_nearest(
    ax,
    x_values,
    y_values,
    event_x,
    label,
    offset=(20, 30),
    color="black",
):
    index = np.abs(
        x_values - event_x
    ).argmin()

    xy = (
        x_values[index],
        y_values[index],
    )

    return ax.annotate(
        label,
        xy=xy,
        xytext=offset,
        textcoords="offset points",
        color=color,
        bbox={
            "boxstyle": "round,pad=0.25",
            "facecolor": "white",
            "edgecolor": color,
            "alpha": 0.9,
        },
        arrowprops={
            "arrowstyle": "->",
            "color": color,
        },
    )
~~~

เรียกใช้งานได้ด้วย:

~~~python
annotation = annotate_nearest(
    ax,
    hours,
    ac_power,
    event_x=14.3,
    label="Afternoon cloud",
    offset=(45, -50),
    color="tab:blue",
)
~~~

`ax.annotate()` คืน Annotation Object กลับมา จึงเก็บไว้ในตัวแปรเพื่อปรับภายหลังได้ เช่น:

~~~python
annotation.set_fontsize(11)
annotation.set_visible(False)
~~~

---

## 13. ใช้ร่วมกับ Multiple Subplots จาก EP8

ข้อความและ Annotation ต้องวางบน Axes ที่ถูกต้อง เมื่อมีหลาย Subplots ให้เลือก Axes ก่อนเสมอ

### เซลล์ที่ 14 — Solar Operations Dashboard

~~~python
fig, axes = plt.subplots(
    2,
    1,
    figsize=(11, 7),
    sharex=True,
    layout="constrained",
)

power_ax, temperature_ax = axes

power_ax.plot(
    hours,
    clear_sky_power,
    color="0.65",
    linestyle="--",
    label="Clear-sky reference",
)

power_ax.plot(
    hours,
    ac_power,
    color="tab:orange",
    linewidth=2.2,
    label="AC power",
)

for ax in axes:
    ax.axvspan(
        12.0,
        12.4,
        color="tab:red",
        alpha=0.1,
    )
    ax.grid(alpha=0.25)

maintenance_index = np.abs(
    hours - 12.2
).argmin()

power_ax.annotate(
    "Inspection window",
    xy=(
        hours[maintenance_index],
        ac_power[maintenance_index],
    ),
    xytext=(35, -55),
    textcoords="offset points",
    bbox={
        "boxstyle": "round,pad=0.3",
        "facecolor": "white",
        "edgecolor": "tab:red",
    },
    arrowprops={
        "arrowstyle": "->",
        "color": "tab:red",
    },
)

power_ax.set(
    title="Power Production",
    ylabel="AC power (kW)",
)
power_ax.legend(ncols=2)

temperature_ax.plot(
    hours,
    ambient_temperature,
    color="tab:blue",
    label="Ambient",
)

temperature_ax.plot(
    hours,
    inverter_temperature,
    color="tab:red",
    linewidth=2,
    label="Inverter",
)

peak_temperature_index = int(
    inverter_temperature.argmax()
)

temperature_ax.annotate(
    (
        "Peak inverter temperature\n"
        f"{inverter_temperature[peak_temperature_index]:.1f} °C"
    ),
    xy=(
        hours[peak_temperature_index],
        inverter_temperature[peak_temperature_index],
    ),
    xytext=(0.02, 0.92),
    textcoords="axes fraction",
    ha="left",
    va="top",
    bbox={
        "boxstyle": "round,pad=0.3",
        "facecolor": "white",
        "edgecolor": "tab:red",
        "alpha": 0.9,
    },
    arrowprops={
        "arrowstyle": "->",
        "color": "tab:red",
    },
)

temperature_ax.set(
    title="Thermal Condition",
    xlabel="Local time (hour)",
    ylabel="Temperature (°C)",
    xlim=(5.5, 18.5),
)
temperature_ax.legend(ncols=2)

fig.suptitle(
    "Solar Farm Operations — Text and Annotation Dashboard"
)

fig.text(
    0.99,
    0.01,
    "Synthetic data for Matplotlib training",
    ha="right",
    fontsize=9,
    color="0.35",
)

plt.show()
~~~

องค์ประกอบแต่ละระดับมีหน้าที่ต่างกัน:

- `power_ax.set(title=...)` ตั้งชื่อเฉพาะกราฟกำลังผลิต
- `temperature_ax.set(title=...)` ตั้งชื่อเฉพาะกราฟอุณหภูมิ
- `fig.suptitle()` ตั้งชื่อรวมของ Dashboard
- `fig.text()` ใส่หมายเหตุที่ใช้กับ Figure ทั้งภาพ
- `power_ax.annotate()` ชี้เหตุการณ์บนกราฟกำลังผลิตเท่านั้น
- `temperature_ax.annotate()` ชี้ค่าสูงสุดบนกราฟอุณหภูมิเท่านั้น

---

## 14. เลือก `text()` หรือ `annotate()` อย่างไร

| ความต้องการ | เครื่องมือที่เหมาะ |
|-------------|-------------------|
| วางข้อความทั่วไปใน Axes | `ax.text()` |
| วางรหัส Panel ที่มุมกราฟ | `ax.text(..., transform=ax.transAxes)` |
| วางหมายเหตุรวมของ Figure | `fig.text()` |
| ชี้จุดข้อมูลด้วยข้อความ | `ax.annotate()` |
| เชื่อมข้อความกับจุดด้วยลูกศร | `ax.annotate(..., arrowprops=...)` |
| แสดงช่วงเวลาเหตุการณ์ | `ax.axvspan()` ร่วมกับ `text()` หรือ `annotate()` |
| ตั้งชื่อเส้นอ้างอิงที่ผูกกับ Y | `ax.text()` ร่วมกับ `ax.get_yaxis_transform()` |

หลักสำคัญคือเลือกเครื่องมือตามความสัมพันธ์ของข้อความกับข้อมูล ไม่ใช่เลือกจากความสวยเพียงอย่างเดียว

---

## 15. คำนวณตำแหน่งจากข้อมูลแทนการเดา

การเขียนพิกัดแบบตายตัวเหมาะกับข้อมูลคงที่ แต่เสี่ยงชี้ผิดเมื่อเปลี่ยน Dataset

### ค่าสูงสุด

~~~python
peak_index = int(ac_power.argmax())
peak_hour = hours[peak_index]
peak_power = ac_power[peak_index]
~~~

### จุดที่ใกล้เวลาที่กำหนด

~~~python
event_hour = 14.3
event_index = np.abs(
    hours - event_hour
).argmin()
~~~

### ช่วงที่ตรงตามเงื่อนไข

~~~python
hot_mask = inverter_temperature >= 47
hot_hours = hours[hot_mask]
~~~

ถ้าข้อมูลมาจากระบบจริง ควรใช้ Timestamp, Event ID และสถานะอุปกรณ์เป็นตัวอ้างอิงแทนการสมมติว่าจุดต่ำสุดทุกจุดเกิดจากสาเหตุเดียวกัน

---

## 16. แนวทางออกแบบ Annotation สำหรับงานอุตสาหกรรม

### ให้ข้อความตอบคำถาม

ข้อความที่มีประโยชน์ควรบอกอย่างน้อยหนึ่งเรื่อง:

- เกิดอะไรขึ้น
- เกิดเมื่อใด
- ค่า ณ จุดนั้นเท่าใด
- สถานะมาจากแหล่งข้อมูลใด

คำว่า `Event` เพียงอย่างเดียวอาจกว้างเกินไป ข้อความ `Inverter inspection — 12:12` สื่อความหมายได้มากกว่า

### แยกเหตุการณ์ออกจากข้อสรุป

เส้นกำลังผลิตที่ลดลงบอกเพียงว่าค่าลด ไม่ได้ยืนยันสาเหตุ หาก Annotation เขียนว่า `Cloud passage` ต้องมีข้อมูลอากาศหรือ Event Log สนับสนุน ในบทนี้ระบุสาเหตุได้เพราะสูตรสร้างข้อมูลถูกกำหนดไว้ล่วงหน้า

### ใช้สีอย่างมีความหมาย

- สีแดงอาจใช้กับ Alarm, Trip หรือช่วงตรวจสอบ แต่ต้องกำหนดความหมายให้ชัด
- สีฟ้าอาจใช้กับ Weather Event
- อย่าใช้สีอย่างเดียวในการแยกสถานะ ควรมีข้อความ รูปทรง หรือ Line Style ร่วมด้วย

### จำกัดจำนวน Annotation

ถ้าทุกจุดมี Label กราฟจะกลายเป็นตารางที่อ่านยาก ให้เลือกเฉพาะเหตุการณ์ที่เกี่ยวข้องกับคำถามของ Figure หรือเปิดรายละเอียดผ่าน Interactive Tool แทน

### ระบุเวลาและหน่วย

- ระบุว่าเวลาเป็น Local Time หรือ UTC
- ในระบบหลาย Site ต้องแสดง Timezone
- ตัวเลขใน Annotation ควรมีหน่วย เช่น kW, °C หรือ kWh
- ใช้จำนวนทศนิยมเท่าที่จำเป็น

### ตรวจ Contrast และขนาดตัวอักษร

- พื้นหลังของ `bbox` ช่วยให้ข้อความไม่กลืนกับเส้นกราฟ
- ตรวจทั้งจอคอมพิวเตอร์ โปรเจกเตอร์ และภาพที่ย่อบนมือถือ
- Export แล้วตรวจว่าข้อความไม่ถูกตัดหรือชนขอบ

---

## 17. ข้อผิดพลาดที่พบบ่อย

### ใช้ Axes Coordinates แต่ใส่ค่าข้อมูล

ผิด:

~~~python
ax.text(
    14.3,
    3200,
    "Cloud",
    transform=ax.transAxes,
)
~~~

`ax.transAxes` คาดค่าประมาณ 0–1 พิกัดจึงออกนอกกราฟ ควรใช้ Data Coordinates หรือเปลี่ยนตัวเลขให้เป็นสัดส่วนของ Axes

### ลืมแยก `xy` กับ `xytext`

หากข้อความทับจุดข้อมูล ให้กำหนด `xytext` และเลือก `textcoords` ให้ชัด ไม่ควรแก้ `xy` เพราะจะทำให้ลูกศรชี้ผิดจุด

### Hard-code ตำแหน่งสูงสุด

~~~python
ax.annotate(
    "Peak",
    xy=(12.0, 5000),
)
~~~

เมื่อข้อมูลเปลี่ยน จุดนี้อาจไม่ใช่ Peak ควรใช้ `argmax()` คำนวณจากข้อมูล

### ข้อความชนกันหลังเปลี่ยน Figure Size

ตำแหน่งที่ดูดีบน Figure `(12, 6)` อาจชนกันบน `(6, 4)` ต้องทดสอบขนาดปลายทางจริง และใช้ `layout="constrained"` ช่วยจัดองค์ประกอบระดับ Layout

### ใช้ Arrow Style มากเกินไป

ลูกศรหลายสี หลายหัว และหลายเส้นเชื่อมใน Figure เดียวทำให้ความหมายไม่สม่ำเสมอ ควรกำหนด Style ตามประเภทเหตุการณ์และใช้ซ้ำ

### Annotation ชี้เหตุการณ์แต่ไม่มีแหล่งที่มา

หากกราฟใช้ในการรายงาน ควรเก็บ Event Source เช่น SCADA Log, Work Order, Weather Station หรือ Operator Note ไว้กับข้อมูล ไม่ควรพิมพ์สาเหตุจากการคาดเดา

---

## 18. Export และตรวจผลงาน

~~~python
fig.savefig(
    "solar_annotation_dashboard.png",
    dpi=160,
    bbox_inches="tight",
)
~~~

ก่อนนำไปใช้ ให้ตรวจ:

- ชื่อกราฟและหน่วยครบหรือไม่
- ลูกศรชี้จุดที่ถูกต้องหรือไม่
- Text และ Annotation ไม่ทับกันหรือไม่
- ข้อความยังอ่านได้เมื่อย่อภาพหรือไม่
- หมายเหตุด้านนอก Axes ถูกตัดหรือไม่
- Event Name และเวลาอ้างอิงข้อมูลจริงหรือไม่
- สีที่ใช้มีความหมายสม่ำเสมอหรือไม่

`bbox_inches="tight"` ช่วยคำนวณกรอบ Export ให้รวม Artist ที่อยู่ใกล้ขอบ แต่ไม่ควรใช้แทนการตรวจ Layout ด้วยสายตา

---

## แบบฝึกหัด

1. เพิ่มข้อความกำลังผลิตสูงสุดด้วย `ax.text()` โดยไม่มีลูกศร
2. เปลี่ยนข้อความเดียวกันเป็น `ax.annotate()` แล้วเปรียบเทียบ
3. วาง Plant ID ด้วย `ax.transData` และ `ax.transAxes` จากนั้น Zoom กราฟ
4. ทดลอง `ha` และ `va` ทุกค่าในตำแหน่งเดียวกัน
5. สร้างกล่องข้อความด้วย `bbox` สาม Style แล้วเลือกแบบที่อ่านง่ายที่สุด
6. ทดลอง `arrowstyle` และ `connectionstyle` อย่างละสามแบบ
7. เพิ่ม Annotation ของเหตุการณ์จาก List และ Loop
8. สร้าง Function ที่รับ Axes, เวลา, ค่า, Label และ Offset
9. ใช้ Blended Transform วางชื่อเส้นอ้างอิงที่ขอบขวา
10. สร้าง Dashboard สอง Axes และเพิ่ม Figure Note ด้วย `fig.text()`

อ่านโจทย์ฉบับเต็มได้ที่ [แบบฝึกหัด EP9](./exercises/exercise01.md)

## โจทย์ท้าทายย่อย

สร้าง Solar Farm Daily Operations Report หนึ่ง Figure โดยต้องมี:

- กราฟ AC Power เทียบกับ Clear-sky Reference
- กราฟ Ambient และ Inverter Temperature
- Annotation ของ Peak Power และ Peak Temperature
- ช่วงสีสำหรับ Maintenance หรือ Inspection Window
- Event Annotation อย่างน้อยสามรายการที่สร้างจาก List
- Plant ID, วันที่ และ Timezone
- หมายเหตุว่าเป็นข้อมูลจริงหรือข้อมูลสังเคราะห์
- หน่วยบนทุกแกนและใน Annotation ที่มีตัวเลข
- Function สำหรับวาง Annotation ที่ใช้ซ้ำได้
- การ Export เป็น PNG โดยข้อความไม่ถูกตัด

เขียนสรุปท้ายงานว่าแต่ละข้อความใช้ Data, Axes, Figure หรือ Blended Coordinates เพราะเหตุใด

## สคริปต์ฉบับเต็ม

- [solar_data.py](./source-code/solar_data.py)
- [basic_text_labels.py](./source-code/basic_text_labels.py)
- [coordinate_transforms.py](./source-code/coordinate_transforms.py)
- [annotate_solar_events.py](./source-code/annotate_solar_events.py)
- [solar_annotation_dashboard.py](./source-code/solar_annotation_dashboard.py)

## เอกสาร Matplotlib ที่เกี่ยวข้อง

- [`Axes.text`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.text.html)
- [`Axes.annotate`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.annotate.html)
- [Transformations Tutorial](https://matplotlib.org/stable/users/explain/artists/transforms_tutorial.html)
- [Annotations guide](https://matplotlib.org/stable/users/explain/text/annotations.html)
- [Annotation examples](https://matplotlib.org/stable/gallery/text_labels_and_annotations/annotation_demo.html)

## ตอนก่อนหน้า

**EP8 — [Multiple Subplots for Manufacturing Production Monitoring](../ep08-multiple-subplots/README.md)**

## ตอนถัดไป

**EP10 — Customizing Ticks**
