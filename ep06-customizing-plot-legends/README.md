# EP6 — Customizing Plot Legends for Smart Farm Data

Legend หรือคำอธิบายสัญลักษณ์ทำหน้าที่เชื่อมสิ่งที่มองเห็นบนกราฟกับความหมายของข้อมูล เช่น เส้นสีเขียวคืออุณหภูมิในโรงเรือน A เส้นประสีส้มคือค่าเตือน และวงกลมขนาดใหญ่คือ Sensor Node ที่ดูแลพื้นที่กว้างกว่า

บทนี้ใช้ **ระบบติดตามสภาพแวดล้อมใน Smart Farm** เป็นกรณีศึกษา เพื่อเรียนรู้การสร้างและปรับแต่ง Legend ด้วย Matplotlib ตั้งแต่กราฟเส้นพื้นฐานไปจนถึง Legend สำหรับขนาดจุดและหลาย Legend บน Axes เดียว

ตัวอย่างและคำอธิบายในบทนี้เรียบเรียงขึ้นใหม่สำหรับชุดวิดีโอนี้ โดยใช้ข้อมูลสังเคราะห์ ไม่ต้องดาวน์โหลดชุดข้อมูลจากภายนอก

## วิธีเรียนจากบทนี้

- คัดลอกเซลล์ตามลำดับจากบนลงล่าง
- รันเซลล์เตรียมข้อมูลก่อนเซลล์สร้างกราฟ
- แต่ละกราฟเริ่มด้วย `plt.subplots()` และจบด้วย `plt.show()` ในเซลล์เดียว
- ทดลองเปลี่ยนค่าของ `loc`, `ncols`, `framealpha` และ `bbox_to_anchor`
- สคริปต์ฉบับเต็มอยู่ในโฟลเดอร์ [source-code](./source-code/)

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบบทนี้ คุณจะสามารถ:
- อธิบายว่า Legend คืออะไร และต่างจาก Label, Annotation และ Colorbar อย่างไร
- สร้าง Legend อัตโนมัติจาก `label` และ `ax.legend()`
- กำหนดตำแหน่ง จำนวนคอลัมน์ กรอบ ความโปร่งใส และชื่อ Legend
- วาง Legend นอกพื้นที่กราฟด้วย `bbox_to_anchor`
- เลือกและจัดลำดับรายการด้วย Handles และ Labels
- สร้างสัญลักษณ์ Legend เองด้วย `Line2D` และ `Patch`
- อธิบายขนาดจุดใน Scatter Plot โดยไม่สร้างข้อมูลปลอม
- แยกการใช้ Legend สำหรับหมวดหมู่ออกจาก Colorbar สำหรับค่าต่อเนื่อง
- แสดงหลาย Legend บน Axes เดียวด้วย `ax.add_artist()`
- ออกแบบ Legend สำหรับ Smart Farm Dashboard ให้เข้าใจง่ายและไม่บดบังข้อมูล

## คำศัพท์สำคัญก่อนเริ่ม

| คำศัพท์ | ความหมาย |
|---------|----------|
| Legend | กล่องหรือพื้นที่ที่อธิบายว่าสี เส้น Marker หรือรูปแบบแต่ละชนิดหมายถึงอะไร |
| Label | ข้อความที่ผูกกับ Plot Artist หนึ่งชิ้นและสามารถนำไปแสดงใน Legend |
| Handle | Object ที่ Legend ใช้เป็นตัวอย่างสัญลักษณ์ เช่น เส้น จุด หรือแถบสี |
| Artist | วัตถุที่ Matplotlib วาดบน Figure เช่น Line2D, Text, Patch และ Legend |
| `loc` | ตำแหน่งยึดของ Legend ภายในหรือสัมพันธ์กับกรอบอ้างอิง |
| `bbox_to_anchor` | จุดหรือกรอบอ้างอิงเพิ่มเติมสำหรับจัดวาง Legend อย่างละเอียด |
| `ncols` | จำนวนคอลัมน์ของรายการใน Legend |
| Colorbar | แถบที่จับคู่สีแบบต่อเนื่องกับค่าตัวเลข เช่น ความชื้น 30–70% |
| Annotation | ข้อความที่ชี้หรืออธิบายเหตุการณ์เฉพาะจุดบนกราฟ |
| Telemetry | ข้อมูลที่อุปกรณ์ส่งกลับมา เช่น อุณหภูมิ ความชื้นดิน และสถานะแบตเตอรี่ |

### Legend ไม่ใช่ชื่อกราฟหรือชื่อแกน

- **Title** บอกว่ากราฟนี้เกี่ยวกับอะไร
- **Axis label** บอกความหมายและหน่วยของแกน X หรือ Y
- **Legend** แยกความหมายของชุดข้อมูลหรือหมวดหมู่
- **Annotation** อธิบายจุดหรือเหตุการณ์เฉพาะ
- **Colorbar** แปลสีที่แทนค่าตัวเลขต่อเนื่อง

Legend ที่ดีจึงไม่ควรใช้แทนข้อความทุกอย่างในกราฟ และไม่ควรใส่รายการที่ไม่ช่วยให้ผู้ชมแยกข้อมูล

---

## 1. เตรียมไลบรารีและข้อมูล Smart Farm

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
~~~

บทนี้ใช้เพียง NumPy และ Matplotlib:

~~~bash
python -m pip install numpy matplotlib
~~~

### เซลล์ที่ 2 — จำลองอุณหภูมิรายชั่วโมง

~~~python
hours = np.arange(0, 24)

greenhouse_a = 25 + 4 * np.sin(
    (hours - 7) * np.pi / 12
)
greenhouse_b = 24 + 3 * np.sin(
    (hours - 6) * np.pi / 12
)
outdoor = 27 + 6 * np.sin(
    (hours - 8) * np.pi / 12
)
~~~

- `hours` แทนเวลา 0–23 นาฬิกา
- `greenhouse_a` และ `greenhouse_b` แทนอุณหภูมิจากสองโรงเรือน
- `outdoor` แทน Sensor ภายนอก
- ฟังก์ชัน Sine ใช้สร้างรูปแบบกลางวัน–กลางคืนเพื่อการสาธิต ไม่ใช่แบบจำลองพยากรณ์อากาศ

### เซลล์ที่ 3 — ตรวจสอบขนาดข้อมูล

~~~python
print("Hours:", hours.shape)
print("Greenhouse A:", greenhouse_a.shape)
print("Greenhouse B:", greenhouse_b.shape)
print("Outdoor:", outdoor.shape)
~~~

ทุก Array ต้องมี 24 ค่าเพื่อให้จับคู่กับเวลาได้ครบ หากความยาวต่างกัน `plot()` จะสร้างกราฟไม่ได้

---

## 2. Legend แรกจาก Label

Matplotlib จะสร้าง Legend จาก Plot Artist ที่มี `label` เมื่อเราเรียก `ax.legend()`

### เซลล์ที่ 4 — สร้างกราฟพร้อม Legend

~~~python
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    hours,
    greenhouse_a,
    color="forestgreen",
    linewidth=2.5,
    label="Greenhouse A",
)
ax.plot(
    hours,
    greenhouse_b,
    color="royalblue",
    linewidth=2.5,
    linestyle="--",
    label="Greenhouse B",
)
ax.plot(
    hours,
    outdoor,
    color="darkorange",
    linewidth=2,
    linestyle=":",
    label="Outdoor sensor",
)

ax.set(
    title="Smart Farm Temperature Monitoring",
    xlabel="Hour",
    ylabel="Temperature (°C)",
    xlim=(0, 23),
)
ax.grid(alpha=0.25)
ax.legend()

fig.tight_layout()
plt.show()
~~~

ลำดับการทำงานคือ:

1. `ax.plot()` สร้าง Line2D และเก็บข้อความจาก `label`
2. `ax.legend()` ค้นหา Handles และ Labels บน Axes
3. Legend วาดตัวอย่างเส้นคู่กับข้อความ

> หากไม่เรียก `ax.legend()` ข้อความใน `label` จะยังไม่ปรากฏเป็น Legend

### Label ใดจะไม่ถูกนำมาแสดง

Artist ที่ไม่มี Label หรือมี Label ขึ้นต้นด้วย `_` จะถูกละเว้นในการสร้าง Legend อัตโนมัติ คุณสมบัตินี้เหมาะกับเส้นช่วยที่ไม่ต้องการอธิบายในกล่อง Legend

~~~python
ax.axhline(
    30,
    color="gray",
    linestyle="--",
    label="_temporary_helper",
)
~~~

อย่าใช้ Label ซ้ำโดยไม่ตั้งใจ เพราะ Legend ไม่ได้รวมรายการซ้ำให้โดยอัตโนมัติทุกกรณี

---

## 3. ปรับตำแหน่งและรูปแบบ Legend

### ตำแหน่งที่ใช้บ่อย

| ค่า `loc` | ตำแหน่ง |
|-----------|---------|
| `"upper left"` | มุมซ้ายบน |
| `"upper right"` | มุมขวาบน |
| `"lower left"` | มุมซ้ายล่าง |
| `"lower right"` | มุมขวาล่าง |
| `"upper center"` | กึ่งกลางด้านบน |
| `"lower center"` | กึ่งกลางด้านล่าง |
| `"center left"` | กึ่งกลางด้านซ้าย |
| `"center right"` | กึ่งกลางด้านขวา |
| `"best"` | ให้ Matplotlib ประเมินตำแหน่งที่บดบังข้อมูลน้อย |

`loc="best"` สะดวกสำหรับการสำรวจข้อมูล แต่ Dashboard ที่ต้องมี Layout คงที่ควรกำหนดตำแหน่งให้ชัดเจน

### เซลล์ที่ 5 — ปรับกรอบ ชื่อ และระยะห่าง

ให้รันเซลล์ที่ 4 ใหม่ โดยแทน `ax.legend()` เดิมด้วยคำสั่งนี้ก่อน `fig.tight_layout()`:

~~~python
ax.legend(
    loc="upper left",
    title="Sensor location",
    ncols=1,
    frameon=True,
    fancybox=True,
    shadow=False,
    framealpha=0.9,
    borderpad=0.8,
    labelspacing=0.6,
    handlelength=2.5,
)
~~~

ความหมายของ Parameter สำคัญ:

- `title` เพิ่มหัวข้อเพื่อบอกว่ารายการกำลังแบ่งตามอะไร
- `frameon` เปิดหรือปิดกรอบ
- `fancybox` ทำให้มุมกรอบโค้ง
- `framealpha` กำหนดความทึบของพื้นหลังระหว่าง 0–1
- `borderpad` คือระยะระหว่างเนื้อหากับขอบกรอบ
- `labelspacing` คือระยะห่างแนวตั้งระหว่างรายการ
- `handlelength` คือความยาวตัวอย่างเส้น

### เซลล์ที่ 6 — แสดง Legend หลายคอลัมน์

~~~python
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(hours, greenhouse_a, label="Greenhouse A")
ax.plot(hours, greenhouse_b, label="Greenhouse B")
ax.plot(hours, outdoor, label="Outdoor sensor")

ax.set(
    title="Temperature by Sensor Location",
    xlabel="Hour",
    ylabel="Temperature (°C)",
)
ax.grid(alpha=0.25)

ax.legend(
    loc="lower center",
    ncols=3,
    frameon=False,
)

fig.tight_layout()
plt.show()
~~~

หลายคอลัมน์เหมาะกับ Legend ที่มีรายการสั้นและต้องการประหยัดความสูง แต่ต้องตรวจบนหน้าจอขนาดเล็กว่าข้อความไม่ชนกัน

> Matplotlib รุ่นปัจจุบันใช้ `ncols` ส่วนตัวอย่างเก่าบางแห่งอาจพบ `ncol`

---

## 4. วาง Legend นอกพื้นที่ Axes

เมื่อเส้นข้อมูลใช้พื้นที่เกือบทั้งกราฟ การย้าย Legend ออกด้านข้างช่วยลดการบดบังข้อมูล

### ทำความเข้าใจ `bbox_to_anchor`

Axes ใช้พิกัดสัดส่วนโดยค่าเริ่มต้น:

- `(0, 0)` คือมุมซ้ายล่างของ Axes
- `(1, 1)` คือมุมขวาบนของ Axes
- `(1.02, 1)` คือเลยขอบขวาออกไปเล็กน้อยและอยู่ระดับบน

`loc` บอกว่า “ส่วนใดของกล่อง Legend” จะไปยึดกับจุดนั้น ส่วน `bbox_to_anchor` บอกว่า “จุดยึดอยู่ที่ไหน” ดังนั้นชื่ออย่าง `upper left` หรือ `lower right` ในกรณีนี้หมายถึง **มุมของกล่อง Legend** ไม่ได้หมายถึงมุมของ Axes โดยตรง

ให้จินตนาการว่า `bbox_to_anchor=(1.02, 1)` เป็นหมุดหนึ่งตัว:

- ค่า X เท่ากับ `1.02` หมายถึงหมุดอยู่เลยขอบขวาของ Axes ออกไป 2%
- ค่า Y เท่ากับ `1` หมายถึงหมุดอยู่ระดับเดียวกับขอบบนของ Axes
- `loc` เลือกว่ามุมใดของ Legend จะถูกนำไปแขวนไว้กับหมุดนี้

เมื่อใช้หมุดเดิม ตำแหน่งของกล่องจะเปลี่ยนตาม `loc`:

| `loc` | มุมของ Legend ที่เกาะหมุด | กล่องขยายออกไปทางใด |
|-------|---------------------------|----------------------|
| `"upper left"` | มุมซ้ายบน | ไปทางขวาและลงด้านล่าง |
| `"lower left"` | มุมซ้ายล่าง | ไปทางขวาและขึ้นด้านบน |
| `"upper right"` | มุมขวาบน | ไปทางซ้ายและลงด้านล่าง |
| `"lower right"` | มุมขวาล่าง | ไปทางซ้ายและขึ้นด้านบน |

เพราะฉะนั้นตัวอย่างนี้ใช้:

~~~python
loc="upper left"
bbox_to_anchor=(1.02, 1)
~~~

มุมซ้ายบนของ Legend จะเกาะกับหมุดที่อยู่ข้างขวาของกราฟ กล่องจึงวางอยู่ด้านขวาและเรียงรายการลงมาในระดับเดียวกับขอบบนของ Axes

แต่หากเปลี่ยนเฉพาะ `loc` เป็น:

~~~python
loc="lower right"
bbox_to_anchor=(1.02, 1)
~~~

มุมขวาล่างของ Legend จะไปเกาะหมุดเดิม กล่องจึงขยายไปทางซ้ายและขึ้นด้านบน ทำให้ดูเหมือน Legend ย้ายกลับเข้าหากราฟหรือสูงเกินขอบบน นี่เป็นพฤติกรรมที่ถูกต้อง เพราะหมุดไม่ได้เปลี่ยน มีเพียงมุมของกล่องที่นำไปเกาะหมุดเท่านั้น

หากต้องการวาง Legend ไว้ **มุมขวาล่างภายในกราฟ** ไม่ต้องใช้ `bbox_to_anchor`:

~~~python
ax.legend(loc="lower right")
~~~

หากต้องการวาง Legend ไว้ **ด้านขวานอกกราฟและชิดขอบล่าง** ให้ย้ายหมุดลงมาที่ `(1.02, 0)` และใช้มุมซ้ายล่างของกล่อง:

~~~python
ax.legend(
    loc="lower left",
    bbox_to_anchor=(1.02, 0),
)
~~~

ส่วน `borderaxespad=0` หมายถึงไม่เพิ่มระยะห่างรอบ Legend จากจุดยึดอีก ระยะห่างด้านขวาในตัวอย่างจึงมาจากค่า X ที่เป็น `1.02`

### เซลล์ที่ 7 — ย้าย Legend ไปด้านขวา

~~~python
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(hours, greenhouse_a, label="Greenhouse A")
ax.plot(hours, greenhouse_b, label="Greenhouse B")
ax.plot(hours, outdoor, label="Outdoor sensor")

ax.set(
    title="Smart Farm Temperature Monitoring",
    xlabel="Hour",
    ylabel="Temperature (°C)",
)
ax.grid(alpha=0.25)

ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.02, 1),
    borderaxespad=0,
    title="Sensor location",
    frameon=False,
)

fig.tight_layout()
plt.show()
~~~

`fig.tight_layout()` ช่วยจัดพื้นที่ใหม่หลังเพิ่ม Legend ด้านนอก หากบันทึกภาพแล้ว Legend ถูกตัด สามารถใช้:

~~~python
fig.savefig(
    "smart_farm_temperature.png",
    dpi=150,
    bbox_inches="tight",
)
~~~

`bbox_inches="tight"` ทำให้ขอบเขตภาพรวม Artist ด้านนอกด้วย แต่ควรเปิดไฟล์ผลลัพธ์ตรวจสอบทุกครั้ง

---

## 5. เลือกและจัดลำดับรายการใน Legend

บางครั้งกราฟมีหลาย Artist แต่เราไม่ต้องการแสดงทั้งหมด หรืออยากให้สถานะสำคัญอยู่ก่อน สามารถรับ Handles และ Labels แล้วเลือกใหม่ได้

### เซลล์ที่ 8 — ตรวจสอบ Handles และ Labels

~~~python
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(hours, greenhouse_a, label="Greenhouse A")
ax.plot(hours, greenhouse_b, label="Greenhouse B")
ax.plot(hours, outdoor, label="Outdoor sensor")

handles, labels = ax.get_legend_handles_labels()

print(labels)
plt.close(fig)
~~~

`handles` เก็บ Object ของเส้น ส่วน `labels` เก็บข้อความในลำดับเดียวกัน การปิด Figure ด้วย `plt.close(fig)` เหมาะกับเซลล์ที่ต้องการตรวจ Object โดยไม่แสดงกราฟ

### เซลล์ที่ 9 — เลือกเฉพาะ Sensor ในโรงเรือน

~~~python
fig, ax = plt.subplots(figsize=(9, 5))

line_a, = ax.plot(
    hours,
    greenhouse_a,
    label="Greenhouse A",
)
line_b, = ax.plot(
    hours,
    greenhouse_b,
    label="Greenhouse B",
)
ax.plot(
    hours,
    outdoor,
    color="lightgray",
    label="Outdoor sensor",
)

ax.set(
    title="Greenhouse Temperature Comparison",
    xlabel="Hour",
    ylabel="Temperature (°C)",
)
ax.grid(alpha=0.25)

ax.legend(
    handles=[line_a, line_b],
    labels=["Zone A", "Zone B"],
    title="Selected zones",
)

fig.tight_layout()
plt.show()
~~~

เครื่องหมายจุลภาคใน `line_a, = ax.plot(...)` มีความสำคัญ เพราะ `ax.plot()` คืนค่าเป็น List แม้ว่าจะวาดเพียงเส้นเดียว การ Unpack ทำให้ `line_a` เป็น Line2D โดยตรง

โดยทั่วไปการใส่ `label` ตั้งแต่สร้าง Artist อ่านง่ายที่สุด ส่วนการส่ง `handles` เหมาะเมื่อจำเป็นต้องเลือก จัดลำดับ หรือเปลี่ยนคำอธิบายจริง ๆ

---

## 6. สร้าง Custom Legend สำหรับสถานะระบบ

ข้อมูล Smart Farm อาจมีความหมายที่ไม่ได้มาจากเส้นข้อมูลโดยตรง เช่น พื้นที่สีเขียวคือช่วงอุณหภูมิเป้าหมาย และเส้นประสีส้มคือเกณฑ์เตือน เราสามารถสร้างตัวอย่าง Handle ด้วย `Patch` และ `Line2D`

### เซลล์ที่ 10 — Import Handle Classes

~~~python
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
~~~

### เซลล์ที่ 11 — สร้าง Legend อธิบาย Operating Status

~~~python
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    hours,
    greenhouse_a,
    color="forestgreen",
    linewidth=2.5,
)
ax.axhspan(18, 30, color="mediumseagreen", alpha=0.15)
ax.axhline(
    30,
    color="darkorange",
    linestyle="--",
    linewidth=1.8,
)

status_handles = [
    Patch(
        facecolor="mediumseagreen",
        alpha=0.35,
        label="Target: 18–30 °C",
    ),
    Line2D(
        [],
        [],
        color="darkorange",
        linestyle="--",
        linewidth=1.8,
        label="Warning threshold",
    ),
]

ax.legend(
    handles=status_handles,
    title="Operating status",
    loc="upper left",
)

ax.set(
    title="Greenhouse Temperature Status",
    xlabel="Hour",
    ylabel="Temperature (°C)",
    ylim=(16, 35),
)
ax.grid(alpha=0.25)

fig.tight_layout()
plt.show()
~~~

รายการใน Custom Legend เป็นตัวแทนเชิงภาพ ไม่ใช่ข้อมูลวัดเพิ่ม การสร้าง Handle จึงไม่เปลี่ยนค่าใน Array และไม่ควรถูกนำไปใช้คำนวณสถิติ

Threshold 30 °C ในตัวอย่างมีไว้สาธิตเท่านั้น ระบบจริงต้องกำหนดตามชนิดพืช ระยะการเจริญเติบโต สภาพโรงเรือน ความแม่นยำของ Sensor และคำแนะนำของผู้เชี่ยวชาญ

---

## 7. Legend สำหรับขนาดจุดของ Sensor Node

สมมติว่าแผนที่แปลงเกษตรใช้:

- ตำแหน่ง X, Y แทนตำแหน่งติดตั้ง
- สีแทนความชื้นดิน ซึ่งเป็นค่าต่อเนื่อง
- ขนาดวงกลมแทนพื้นที่ครอบคลุมของ Sensor

ข้อมูลสองชนิดนี้ควรใช้คำอธิบายต่างกัน:

- **Colorbar** อธิบายสีของค่าความชื้นต่อเนื่อง
- **Legend** อธิบายขนาดตัวอย่างของพื้นที่ครอบคลุม

### เซลล์ที่ 12 — เตรียมข้อมูล Sensor Node

~~~python
sensor_x = np.array([1.0, 2.8, 4.5, 6.2, 8.2, 9.0])
sensor_y = np.array([1.2, 4.0, 2.0, 4.5, 1.3, 3.6])

soil_moisture = np.array([41, 55, 48, 63, 36, 58])
coverage_m2 = np.array([20, 40, 30, 50, 20, 40])

size_scale = 7
point_sizes = coverage_m2 * size_scale
~~~

ค่า `s` ของ `scatter()` คือพื้นที่ Marker ในหน่วย point² ไม่ใช่ตารางเมตรโดยตรง เราจึงใช้ `size_scale` แปลงค่าทางธุรกิจให้เป็นขนาดที่มองเห็นได้

### เซลล์ที่ 13 — สร้าง Scatter, Size Legend และ Colorbar

~~~python
fig, ax = plt.subplots(figsize=(10, 5.8))

points = ax.scatter(
    sensor_x,
    sensor_y,
    s=point_sizes,
    c=soil_moisture,
    cmap="YlGnBu",
    vmin=30,
    vmax=70,
    edgecolor="black",
    linewidth=0.8,
    alpha=0.85,
)

size_handles = [
    Line2D(
        [],
        [],
        marker="o",
        linestyle="none",
        markersize=np.sqrt(area * size_scale),
        markerfacecolor="lightgray",
        markeredgecolor="black",
        alpha=0.85,
        label=f"{area} m²",
    )
    for area in [20, 35, 50]
]

ax.legend(
    handles=size_handles,
    title="Coverage area",
    loc="upper left",
)

colorbar = fig.colorbar(points, ax=ax, pad=0.02)
colorbar.set_label("Soil moisture (%)")

ax.set(
    title="Smart Farm Sensor Coverage",
    xlabel="Field X position (m)",
    ylabel="Field Y position (m)",
    xlim=(0, 10),
    ylim=(0, 5.5),
)
ax.set_aspect("equal")
ax.grid(alpha=0.2)

fig.tight_layout()
plt.show()
~~~

เหตุผลที่ใช้ `np.sqrt()` กับ `markersize` คือ `scatter(s=...)` กำหนด **พื้นที่** Marker แต่ `Line2D(markersize=...)` รับ **ความกว้างโดยประมาณ** หากไม่ถอดรากที่สอง สัญลักษณ์ใน Legend จะใหญ่เกินสัดส่วน

อีกทางเลือกหนึ่งคือ `PathCollection.legend_elements()` ซึ่งช่วยสร้าง Handles จาก Scatter อัตโนมัติ แต่ Custom Handle เหมาะกับบทนี้เพราะควบคุมค่าตัวอย่างและข้อความได้ตรงกับหน่วยงานจริง

### Colorbar หรือ Legend

| ลักษณะข้อมูล | เครื่องมือที่เหมาะสม | ตัวอย่าง |
|--------------|----------------------|----------|
| หมวดหมู่แยกจากกัน | Legend | Online, Offline, Warning |
| รูปแบบเส้น | Legend | Sensor จริง, ค่าเฉลี่ย, Threshold |
| ขนาดจุดตัวอย่าง | Legend | พื้นที่ 20, 35, 50 m² |
| สีแทนค่าต่อเนื่อง | Colorbar | ความชื้น 30–70% |

ไม่ควรสร้าง Legend หลายสิบรายการเพื่อแทนความชื้นทุกค่า เพราะผู้อ่านกราฟควรใช้ Scale ต่อเนื่องจาก Colorbar เพื่อเทียบสีกับค่าความชื้นได้โดยตรง

---

## 8. หลาย Legend บน Axes เดียว

การเรียก `ax.legend()` ครั้งที่สองจะใช้ Legend ใหม่แทน Legend เดิม หากต้องการเก็บกล่องแรก ต้องเก็บ Object แล้วเพิ่มกลับด้วย `ax.add_artist()`

### เซลล์ที่ 14 — Legend สำหรับ Sensor และ Operating Status

~~~python
fig, ax = plt.subplots(figsize=(10, 5.5))

line_a, = ax.plot(
    hours,
    greenhouse_a,
    color="forestgreen",
    linewidth=2.5,
    label="Greenhouse A",
)
line_b, = ax.plot(
    hours,
    greenhouse_b,
    color="royalblue",
    linewidth=2.5,
    label="Greenhouse B",
)

ax.axhspan(18, 30, color="mediumseagreen", alpha=0.12)
ax.axhline(
    30,
    color="darkorange",
    linestyle="--",
    linewidth=1.8,
)

sensor_legend = ax.legend(
    handles=[line_a, line_b],
    title="Temperature sensor",
    loc="upper left",
)
ax.add_artist(sensor_legend)

status_handles = [
    Patch(
        facecolor="mediumseagreen",
        alpha=0.35,
        label="Target: 18–30 °C",
    ),
    Line2D(
        [],
        [],
        color="darkorange",
        linestyle="--",
        linewidth=1.8,
        label="Warning threshold",
    ),
]

ax.legend(
    handles=status_handles,
    title="Operating status",
    loc="upper right",
)

ax.set(
    title="Greenhouse Temperature and Operating Status",
    xlabel="Hour",
    ylabel="Temperature (°C)",
    xlim=(0, 23),
    ylim=(16, 35),
)
ax.grid(alpha=0.25)

fig.tight_layout()
plt.show()
~~~

ลำดับสำคัญคือ:

1. สร้าง Legend กล่องแรกและเก็บไว้ใน `sensor_legend`
2. เรียก `ax.add_artist(sensor_legend)` เพื่อคงกล่องแรกบน Axes
3. สร้าง Legend กล่องที่สองด้วย `ax.legend()`

หลาย Legend เหมาะเมื่อความหมายแบ่งเป็นคนละกลุ่มอย่างชัดเจน หากรายการมีเพียงไม่กี่รายการ การรวมเป็นกล่องเดียวมักอ่านง่ายกว่า

---

## 9. Legend สำหรับสถานะ Online, Warning และ Offline

ในระบบ IoT สถานะอุปกรณ์เป็นข้อมูลแบบหมวดหมู่ สีอย่างเดียวอาจไม่เพียงพอสำหรับผู้มีภาวะการมองเห็นสี ควรใช้ Marker Shape ร่วมด้วย

### เซลล์ที่ 15 — สร้าง Status Legend ที่ไม่พึ่งสีอย่างเดียว

~~~python
status_handles = [
    Line2D(
        [], [],
        marker="o",
        linestyle="none",
        color="seagreen",
        markersize=9,
        label="Online",
    ),
    Line2D(
        [], [],
        marker="^",
        linestyle="none",
        color="darkorange",
        markersize=9,
        label="Warning",
    ),
    Line2D(
        [], [],
        marker="x",
        linestyle="none",
        color="dimgray",
        markersize=9,
        markeredgewidth=2,
        label="Offline",
    ),
]

fig, ax = plt.subplots(figsize=(8, 4.5))

ax.scatter([1, 3, 5], [2, 3, 2], marker="o", color="seagreen")
ax.scatter([2, 6], [1, 3], marker="^", color="darkorange")
ax.scatter([4], [2.5], marker="x", color="dimgray", linewidth=2)

ax.legend(
    handles=status_handles,
    title="Node status",
    loc="upper center",
    ncols=3,
)
ax.set(
    title="Soil Sensor Network Status",
    xlabel="Field X position",
    ylabel="Field Y position",
    xlim=(0, 7),
    ylim=(0, 4),
)
ax.grid(alpha=0.2)

fig.tight_layout()
plt.show()
~~~

ใน Dashboard จริง คำว่า Offline ต้องมาจากกฎที่ชัดเจน เช่น ไม่ได้รับ Telemetry เกิน 10 นาที ไม่ใช่ตัดสินจากค่าวัดต่ำหรือสูง

---

## 10. แนวทางออกแบบ Legend ให้อ่านง่าย

### ใช้ข้อความที่บอกความหมาย

- ใช้ `Greenhouse A` แทน `line1`
- ระบุหน่วยในชื่อแกนหรือ Colorbar แทนการซ้ำใน Legend ทุกรายการ
- ใช้ชื่อสถานะที่คนปฏิบัติงานเข้าใจตรงกัน
- ระบุว่า Threshold มาจาก Config, Agronomist หรือ Standard ใดในเอกสารระบบ

### จัดลำดับตามความสำคัญ

- Warning หรือ Critical ควรมองเห็นง่าย
- รายการควรเรียงเหมือนลำดับใน Dashboard หรือกระบวนการทำงาน
- อย่าใช้สีเดียวกันกับคนละความหมายข้ามหลายกราฟ

### ลดความซ้ำซ้อน

- ถ้ามีเส้นชนิดเดียวและชื่อกราฟบอกชัด อาจไม่ต้องมี Legend
- หากชื่อ Sensor อยู่ข้างปลายเส้นโดยตรง อาจไม่ต้องใช้กล่อง Legend
- ถ้ามีรายการจำนวนมาก ควรแบ่งกราฟ ใช้ตัวกรอง หรือเลือกเฉพาะข้อมูลสำคัญ

### รองรับการอ่านบนจอหลายขนาด

- ตรวจ Legend บน Mobile, Tablet และจอควบคุม
- หลีกเลี่ยง Font ขนาดเล็กเกินไป
- อย่าวาง Legend ทับค่าผิดปกติหรือจุดล่าสุด
- เมื่อวาง Legend ด้านนอก ให้ตรวจภาพที่ Export และหน้า Dashboard จริง

### อย่าพึ่งสีเพียงอย่างเดียว

ใช้สีร่วมกับ:
- เส้นทึบ เส้นประ และเส้นจุด
- วงกลม สามเหลี่ยม และกากบาท
- ข้อความกำกับที่ชัดเจน
- Pattern หรือความหนาเส้นเมื่อเหมาะสม

---

## 11. ข้อจำกัดและข้อควรระวังกับข้อมูล Smart Farm จริง

- ตรวจสอบ Timestamp และ Timezone ก่อนรวมข้อมูลหลาย Gateway
- แสดงเวลาที่อัปเดตล่าสุด เพราะ Legend ไม่ได้บอกว่าข้อมูลสดหรือเก่า
- แยก Sensor Offline ออกจากค่าความชื้น 0% ซึ่งอาจเป็นข้อมูลผิดปกติคนละชนิด
- ตรวจสอบ Calibration และหน่วยก่อนเปรียบเทียบ Sensor หลายรุ่น
- Threshold ของพืชต่างชนิดหรือระยะเติบโตต่างกันอาจใช้ร่วมกันไม่ได้
- สีสถานะต้องสอดคล้องทั้ง Dashboard, Alarm และเอกสารปฏิบัติงาน
- Legend อธิบายการเข้ารหัสทางภาพ แต่ไม่ได้พิสูจน์คุณภาพข้อมูลหรือสาเหตุของเหตุการณ์
- หากมี Device จำนวนมาก ควรแบ่งตาม Zone หรือใช้ Interactive Filter แทน Legend ที่ยาวเกินไป

---

## 12. สรุปการเลือกใช้ Parameter

| ความต้องการ | แนวทาง |
|-------------|--------|
| สร้าง Legend จากเส้นทั่วไป | ใส่ `label` แล้วเรียก `ax.legend()` |
| ย้าย Legend ใน Axes | ใช้ `loc` |
| ย้าย Legend นอก Axes | ใช้ `loc` ร่วมกับ `bbox_to_anchor` |
| ลดความสูงของ Legend | ใช้ `ncols` |
| ปรับความทึบของกรอบ | ใช้ `framealpha` |
| เลือกบางรายการ | ส่ง `handles` และ `labels` |
| อธิบายสถานะที่ไม่ได้มาจาก Plot โดยตรง | สร้าง `Line2D` หรือ `Patch` |
| อธิบายสีต่อเนื่อง | ใช้ Colorbar |
| แสดงหลาย Legend | เก็บ Legend แรกแล้วใช้ `ax.add_artist()` |

## แบบฝึกหัด

1. ย้าย Legend ของกราฟอุณหภูมิไปครบทั้งสี่มุมแล้วบันทึกว่าตำแหน่งใดบดบังข้อมูลน้อยที่สุด
2. เปลี่ยน Legend เป็นสองคอลัมน์และปรับ `framealpha`
3. เพิ่มโรงเรือน C แล้ววาง Legend ไว้นอก Axes
4. เลือกแสดงเฉพาะ Greenhouse A และ Outdoor Sensor ใน Legend
5. เพิ่มสถานะ Maintenance ด้วย Marker รูปสี่เหลี่ยม
6. เปลี่ยนพื้นที่ครอบคลุมใน Size Legend เป็น 10, 30 และ 60 m²
7. สร้างสอง Legend แยก Sensor Location ออกจาก Irrigation Status

อ่านโจทย์ฉบับเต็มได้ที่ [แบบฝึกหัด EP6](./exercises/exercise01.md)

## โจทย์ท้าทายย่อย

สร้าง Smart Farm Monitoring Dashboard หนึ่งหน้า โดยต้องมี:
- กราฟอุณหภูมิอย่างน้อยสาม Zone
- เส้น Threshold และช่วง Target
- Legend แยกชุดข้อมูลกับสถานะระบบ
- แผนที่ Sensor Node ที่สีแทนความชื้นและขนาดแทนพื้นที่ครอบคลุม
- Colorbar พร้อมหน่วย
- สถานะ Online, Warning และ Offline ที่ไม่พึ่งสีเพียงอย่างเดียว
- เวลาอัปเดตล่าสุดและคำอธิบายว่า Threshold มาจากไหน

## สคริปต์ฉบับเต็ม

- [basic_smart_farm_legend.py](./source-code/basic_smart_farm_legend.py)
- [legend_outside_axes.py](./source-code/legend_outside_axes.py)
- [sensor_size_legend.py](./source-code/sensor_size_legend.py)
- [multiple_legends.py](./source-code/multiple_legends.py)

## ตอนถัดไป

**EP7 — [Customizing Colorbars for Smart Building IoT Data](../ep07-customizing-colorbars/README.md)**
