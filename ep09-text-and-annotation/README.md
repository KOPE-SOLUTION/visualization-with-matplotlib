# EP9 — Text and Annotation for Solar Power Plant Operations

กราฟที่ดีควรบอกได้ว่าเกิดอะไรขึ้น จุดใดสำคัญ และข้อความนั้นอ้างถึงข้อมูลส่วนไหน บทนี้จึงโฟกัสที่ `ax.text()` และ `ax.annotate()` โดยใช้กราฟกำลังผลิตของโรงไฟฟ้าพลังงานแสงอาทิตย์เป็นกรณีศึกษา

ข้อมูลทั้งหมดเป็นข้อมูลสังเคราะห์สำหรับเรียน Matplotlib ไม่ใช่ข้อมูลจากโรงไฟฟ้าจริง และไม่ควรนำค่าตัวอย่างไปใช้เป็นเกณฑ์ควบคุมระบบไฟฟ้า

## เส้นทางการเรียน

1. สร้างข้อมูล Solar แบบสั้น ๆ
2. ใส่ชื่อกราฟ ชื่อแกน และหน่วย
3. วางข้อความด้วย `ax.text()`
4. เข้าใจ Data, Axes และ Figure Coordinates
5. ชี้จุดด้วย `ax.annotate()`
6. ใส่ Annotation ให้หลายเหตุการณ์ด้วย Loop
7. Export และตรวจความเรียบร้อย

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบบทนี้ จะสามารถ:

- วางข้อความธรรมดาด้วย `ax.text()`
- เลือกระบบพิกัดให้เหมาะกับหน้าที่ของข้อความ
- ใช้ `ax.annotate()` แยกจุดที่ต้องการชี้ออกจากตำแหน่งข้อความ
- เพิ่มลูกศรและกล่องข้อความอย่างพอดี
- สร้าง Annotation หลายรายการจาก List และ Loop
- Export กราฟโดยข้อความไม่ถูกตัด

## ภาพจำก่อนเริ่ม

| สิ่งที่ต้องการ | เครื่องมือหลัก |
|---|---|
| ชื่อกราฟและชื่อแกน | `ax.set()` |
| ข้อความธรรมดาบนกราฟ | `ax.text()` |
| ข้อความพร้อมชี้จุดข้อมูล | `ax.annotate()` |
| หมายเหตุที่ยึดกับมุมของกราฟ | `transform=ax.transAxes` |
| หมายเหตุที่ยึดกับ Figure ทั้งภาพ | `fig.text()` |

---

## 1. เตรียมข้อมูล Solar แบบเข้าใจง่าย

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
~~~

ติดตั้งไลบรารีได้ด้วย:

~~~bash
python -m pip install numpy matplotlib
~~~

### เซลล์ที่ 2 — สร้างข้อมูลหนึ่งวัน

~~~python
rng = np.random.default_rng(9)

hours = np.arange(6, 18.01, 0.25)

solar_shape = np.sin(
    np.pi * (hours - 6) / 12
) ** 1.4

clear_sky_power = 5200 * solar_shape

ac_power = np.clip(
    clear_sky_power
    + rng.normal(0, 65, hours.size)
    * solar_shape,
    0,
    None,
)

ac_power[
    np.abs(hours - 9.0) <= 0.25
] *= 0.78

ac_power[
    np.abs(hours - 12.25) <= 0.25
] *= 0.68

ac_power[
    np.abs(hours - 14.25) <= 0.25
] *= 0.58
~~~

ส่วนนี้มีหน้าที่เพียงสร้างเส้นกำลังผลิตที่ขึ้นในตอนเช้า สูงช่วงกลางวัน และลดลงช่วงเย็น พร้อมจุดลดลงสามช่วงสำหรับฝึก Annotation

- `clear_sky_power` คือเส้นอ้างอิงเมื่อสมมติว่าท้องฟ้าโปร่ง
- `ac_power` คือกำลังผลิตจำลองหลังเพิ่มความผันผวน
- สามคำสั่งท้ายสร้างช่วงกำลังลดลงสำหรับฝึกชี้เหตุการณ์

สูตรนี้ไม่ใช่แบบจำลองทางวิศวกรรมของโรงไฟฟ้าจริง จุดประสงค์คือทำให้มีข้อมูลที่อ่านง่ายและเหมาะกับการฝึกวางข้อความ

---

## 2. เริ่มจากชื่อกราฟ ชื่อแกน และหน่วย

### เซลล์ที่ 3 — กราฟพื้นฐาน

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
    title="Solar Farm AC Power",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(6, 18),
)

ax.grid(alpha=0.25)
plt.show()
~~~

ก่อนใส่ Annotation ควรทำให้ผู้อ่านกราฟทราบก่อนว่ากราฟแสดงอะไร แกน X คืออะไร และแกน Y ใช้หน่วยใด

---

## 3. วางข้อความด้วย `ax.text()`

รูปแบบพื้นฐานคือ `ax.text(x, y, "ข้อความ")`

ถ้าไม่กำหนด `transform` ค่า `x` และ `y` จะอ้างอิงค่าจริงบนแกนข้อมูล

### เซลล์ที่ 4 — เขียนข้อความใกล้เหตุการณ์

~~~python
cloud_index = np.abs(
    hours - 14.25
).argmin()

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

ax.text(
    hours[cloud_index],
    ac_power[cloud_index] + 420,
    "Afternoon cloud",
    color="tab:blue",
    fontweight="bold",
    ha="center",
)

ax.set(
    title="Text Placed Near a Solar Event",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(6, 18),
)

ax.grid(alpha=0.25)
plt.show()
~~~

ค่าที่ส่งให้ `ax.text()` มีความหมายดังนี้:

- X คือเวลาของเหตุการณ์
- Y คือกำลังผลิตตรงเหตุการณ์ บวก 420 kW เพื่อยกข้อความขึ้นเหนือเส้น
- `ha="center"` จัดให้ข้อความอยู่กึ่งกลางตำแหน่ง X

`ax.text()` เหมาะกับข้อความที่ไม่จำเป็นต้องมีลูกศร หากต้องการชี้จุดให้ชัดเจน ควรใช้ `ax.annotate()` ซึ่งจะเรียนในหัวข้อถัดไป

---

## 4. เลือกระบบพิกัดให้ถูก

Matplotlib มีระบบพิกัดที่ใช้บ่อยสามแบบ:

| พิกัด | ช่วงตัวเลข | เหมาะกับ |
|---|---|---|
| `ax.transData` | ค่าจริงของแกน | ชื่อเหตุการณ์หรือค่าที่ผูกกับข้อมูล |
| `ax.transAxes` | 0–1 ภายใน Axes | ป้ายที่ต้องอยู่มุมเดิมของกราฟ |
| `fig.transFigure` | 0–1 ทั้ง Figure | หมายเหตุรวมของภาพ |

ภาพจำง่าย ๆ คือ:

- Data Coordinates ผูกกับเส้นข้อมูล
- Axes Coordinates ผูกกับกรอบกราฟ
- Figure Coordinates ผูกกับภาพทั้งใบ

### เซลล์ที่ 5 — เปรียบเทียบสามระบบพิกัด

~~~python
fig, ax = plt.subplots(
    figsize=(10, 5),
    layout="constrained",
)

ax.plot(
    hours,
    ac_power,
    color="tab:orange",
)

event_index = np.abs(
    hours - 9.0
).argmin()

ax.text(
    hours[event_index],
    ac_power[event_index] + 350,
    "Data coordinates\n(x and y follow the data)",
    color="tab:blue",
)

ax.text(
    0.02,
    0.95,
    "Axes coordinates\n(0.02, 0.95)",
    transform=ax.transAxes,
    va="top",
    fontweight="bold",
)

fig.text(
    0.98,
    0.03,
    "Figure coordinates (0.98, 0.03)",
    ha="right",
    va="bottom",
    color="tab:red",
    fontweight="bold",
    bbox=dict(
        facecolor="white",
        edgecolor="tab:red",
        alpha=0.9,
    ),
)

ax.set(
    title="Three Coordinate Systems",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(6, 18),
)

ax.grid(alpha=0.25)
plt.show()
~~~

จุดสังเกตจากผลลัพธ์:

- `ax.text()` รายการแรกไม่ได้กำหนด `transform` จึงใช้ `ax.transData` ซึ่งเป็นค่าเริ่มต้น ตำแหน่งจึงอ้างอิงค่าบนแกน x และ y
- `ax.text()` รายการที่สองต้องเขียน `transform=ax.transAxes` เพราะต้องการเปลี่ยนจากค่าข้อมูลมาเป็นสัดส่วน 0–1 ภายในกรอบกราฟ
- `fig.text()` ใช้พิกัด Figure เป็นค่าเริ่มต้นอยู่แล้ว ตำแหน่ง `(0.98, 0.03)` จึงหมายถึง 98% จากซ้ายและ 3% จากล่างของภาพทั้งใบ

หลักจำง่าย ๆ คือ **เขียน `transform` เมื่อเราต้องการเปลี่ยนระบบพิกัดจากค่าเริ่มต้น** ส่วนค่าที่เป็น Default ไม่จำเป็นต้องเขียนซ้ำ แต่ควรรู้ว่า Matplotlib กำลังใช้อะไรอยู่เบื้องหลัง

---

## 5. ชี้จุดด้วย `ax.annotate()`

`ax.annotate()` แยกตำแหน่งออกเป็นสองส่วน:

- `xy` คือจุดข้อมูลที่ต้องการชี้
- `xytext` คือจุดที่ต้องการวางข้อความ

### เซลล์ที่ 6 — ชี้กำลังผลิตสูงสุด

~~~python
peak_index = ac_power.argmax()

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
    xy=(
        hours[peak_index],
        ac_power[peak_index],
    ),
    xytext=(25, 35),
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

ax.set(
    title="Peak Power Annotation",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(6, 18),
)

ax.grid(alpha=0.25)
plt.show()
~~~

`textcoords="offset points"` ทำให้ `(25, 35)` หมายถึงเลื่อนข้อความจากจุด `xy` ไปทางขวา 25 Point และขึ้นด้านบน 35 Point ไม่ใช่เพิ่มเวลา 25 ชั่วโมงหรือเพิ่มกำลัง 35 kW

ตัวอย่างนี้ไม่ได้กำหนด `xycoords` เพราะ `ax.annotate()` ใช้ Data Coordinates เป็นค่าเริ่มต้นสำหรับ `xy` อยู่แล้ว แต่ต้องกำหนด `textcoords="offset points"` เนื่องจากต้องการวางข้อความด้วยระบบพิกัดที่ต่างจากค่าเริ่มต้น

ส่วนที่ใช้ปรับหน้าตามีสองกลุ่ม:

- `bbox` ควบคุมกล่องรอบข้อความ
- `arrowprops` ควบคุมลูกศร

เริ่มจาก `arrowstyle="->"` ก่อนก็เพียงพอ ไม่จำเป็นต้องใช้ลูกศรหลายรูปแบบในกราฟเดียว

---

## 6. Annotation หลายเหตุการณ์ด้วย List และ Loop

จุดแข็งของการเก็บเหตุการณ์ใน List คือเพิ่มหรือลดเหตุการณ์ได้โดยไม่ต้องคัดลอกโค้ด `annotate()` หลายชุด

### เซลล์ที่ 7 — ชี้เหตุการณ์สำคัญสามช่วง

~~~python
events = [
    {
        "hour": 9.0,
        "label": "Morning cloud",
        "offset": (-50, -55),
        "color": "tab:blue",
    },
    {
        "hour": 12.25,
        "label": "Inverter inspection",
        "offset": (0, -70),
        "color": "tab:red",
    },
    {
        "hour": 14.25,
        "label": "Afternoon cloud",
        "offset": (55, -55),
        "color": "tab:blue",
    },
]

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
    label="Synthetic AC power",
)

for event in events:
    index = np.abs(
        hours - event["hour"]
    ).argmin()

    point = (
        hours[index],
        ac_power[index],
    )

    ax.scatter(
        *point,
        color=event["color"],
        zorder=3,
    )

    ax.annotate(
        event["label"],
        xy=point,
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
        },
    )

ax.set(
    title="Annotated Solar-Farm Events",
    xlabel="Local time (hour)",
    ylabel="AC power (kW)",
    xlim=(6, 18),
)

ax.legend()
ax.grid(alpha=0.25)
plt.show()
~~~

ลำดับการทำงานของ Loop คือ:

1. อ่านข้อมูลเหตุการณ์หนึ่งรายการ
2. หาตำแหน่งเวลาใน Array ที่ใกล้ที่สุด
3. สร้างจุด `(x, y)`
4. วาดจุดด้วย `scatter()`
5. วางข้อความและลูกศรด้วย `annotate()`

ในงานจริง ไม่ควรสรุปสาเหตุจากรูปร่างของกราฟเพียงอย่างเดียว ชื่อเหตุการณ์ควรมาจากแหล่งข้อมูล เช่น Event Log, Weather Station หรือ Work Order

---

## 7. เลือก `text()` หรือ `annotate()`

| สถานการณ์ | เครื่องมือที่เหมาะ |
|---|---|
| ใส่ข้อความทั่วไปโดยไม่ต้องชี้จุด | `ax.text()` |
| ชี้จุดสูงสุด จุดผิดปกติ หรือเหตุการณ์ | `ax.annotate()` |
| วางหมายเหตุไว้ที่มุมเดิมของ Axes | `ax.text(..., transform=ax.transAxes)` |
| วางหมายเหตุรวมของ Figure | `fig.text()` |

หลักง่าย ๆ คือ ถ้าผู้อ่านต้องรู้ว่าข้อความชี้จุดใด ให้ใช้ `annotate()`

### แนวทางสำหรับกราฟงานปฏิบัติการ

- ใส่ Annotation เฉพาะเหตุการณ์ที่ช่วยตอบคำถาม
- ใช้สีเดียวกันกับเหตุการณ์ประเภทเดียวกัน
- แสดงเวลาและหน่วยเมื่อข้อความมีตัวเลข
- หลีกเลี่ยงข้อความยาวทับเส้นข้อมูล
- ตรวจว่าลูกศรชี้จุดถูกต้องหลังเปลี่ยนขนาด Figure
- ระบุให้ชัดว่าเป็นข้อมูลจริงหรือข้อมูลสังเคราะห์

<details>
  <summary>อ่านต่อเมื่อพร้อม: ตัวอย่างขั้นสูง</summary>

หัวข้อต่อไปนี้มีประโยชน์ แต่ไม่จำเป็นสำหรับการเข้าใจพื้นฐานของ EP9:

- Blended Transform สำหรับผูก X กับ Axes และ Y กับ Data
- Function สำหรับสร้าง Annotation รูปแบบเดิมซ้ำหลายครั้ง
- Dashboard ที่มีหลาย Subplot

ดูตัวอย่างได้ในสคริปต์:

- [coordinate_transforms.py](./source-code/coordinate_transforms.py)
- [annotate_solar_events.py](./source-code/annotate_solar_events.py)
- [solar_annotation_dashboard.py](./source-code/solar_annotation_dashboard.py)

</details>

---

## 8. Export และตรวจผลงาน

### เซลล์ที่ 8 — บันทึกเป็น PNG

~~~python
fig.savefig(
    "solar-annotation.png",
    dpi=160,
    bbox_inches="tight",
)
~~~

- `dpi=160` ให้ความคมชัดเหมาะกับการดูบนหน้าจอ
- `bbox_inches="tight"` ช่วยลดโอกาสที่ข้อความรอบ Figure ถูกตัด

ก่อนนำไปใช้ ควรเปิดไฟล์ PNG ตรวจอีกครั้งว่า:

- ไม่มีข้อความชนกัน
- ลูกศรชี้จุดที่ต้องการจริง
- ชื่อแกนและหน่วยครบ
- ตัวอักษรอ่านได้ในขนาดปลายทาง
- สีของข้อความและลูกศรมี Contrast เพียงพอ

---

## ข้อผิดพลาดที่พบบ่อย

### ใช้ค่าข้อมูลกับ Axes Coordinates

~~~python
# ไม่ถูก: 4500 ไม่อยู่ในช่วง 0–1
ax.text(
    0.5,
    4500,
    "Alarm",
    transform=ax.transAxes,
)
~~~

ถ้าต้องการใช้ค่า 4,500 kW ให้ใช้ Data Coordinates หรือเลือก Transform ที่เหมาะกับงาน

### วางข้อความด้วยตัวเลขคงที่ทั้งที่ข้อมูลเปลี่ยนได้

ใช้ `argmax()` หรือค้นหา Index จากเวลา แทนการเดาตำแหน่งจุดสำคัญด้วยตนเอง

### ใช้ `xytext` แต่ไม่กำหนด `textcoords`

ถ้าต้องการเลื่อนข้อความจากจุดข้อมูลเป็นระยะสั้น ๆ ให้กำหนด `textcoords="offset points"` ให้ชัดเจน

### ใส่ Annotation มากเกินไป

เลือกเฉพาะเหตุการณ์ที่จำเป็น หากทุกจุดมีข้อความ กราฟจะอ่านยากกว่าการไม่มี Annotation

---

## แบบฝึกหัด

ใช้ข้อมูลเดิมแล้วสร้างกราฟใหม่ที่มี:

- เส้น `clear_sky_power` และ `ac_power`
- Annotation สำหรับเหตุการณ์สองรายการ
- ข้อความ `"Synthetic data"` ที่มุมขวาล่างของ Axes
- กล่องข้อความสีขาวและลูกศรสีเดียวกับประเภทเหตุการณ์
- ชื่อกราฟ ชื่อแกน และหน่วยครบ

จากนั้นทดลองเปลี่ยน `figsize` และตรวจว่าข้อความยังไม่ชนกัน

## สคริปต์ฉบับเต็ม

- [solar_data.py](./source-code/solar_data.py) — สร้างข้อมูลสังเคราะห์ฉบับเต็ม
- [basic_text_labels.py](./source-code/basic_text_labels.py) — ตัวอย่าง `ax.text()`
- [coordinate_transforms.py](./source-code/coordinate_transforms.py) — ตัวอย่างระบบพิกัด
- [annotate_solar_events.py](./source-code/annotate_solar_events.py) — Annotation หลายเหตุการณ์
- [solar_annotation_dashboard.py](./source-code/solar_annotation_dashboard.py) — ตัวอย่าง Dashboard สำหรับต่อยอด

## เอกสาร Matplotlib ที่เกี่ยวข้อง

- [`Axes.text`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.text.html)
- [`Axes.annotate`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.annotate.html)
- [Transformations tutorial](https://matplotlib.org/stable/users/explain/artists/transforms_tutorial.html)
- [Annotations guide](https://matplotlib.org/stable/users/explain/text/annotations.html)

## ตอนก่อนหน้า

**EP8 — [Multiple Subplots for Manufacturing Production Monitoring](../ep08-multiple-subplots/README.md)**

## ตอนถัดไป

**EP10 — [Customizing Ticks for Cold-Chain Logistics Monitoring](../ep10-customizing-ticks/README.md)**
