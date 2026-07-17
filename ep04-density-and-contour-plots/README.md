# EP4 — Density and Contour Plots for IoT Sensor Data

อุปกรณ์ IoT มักส่งค่าที่ผูกกับตำแหน่ง เช่น อุณหภูมิในโรงงาน ความชื้นในแปลงเกษตร หรือความแรงสัญญาณไร้สาย บทนี้จะใช้ **ระบบติดตามอุณหภูมิในห้องเครื่องจักร** เป็นกรณีศึกษา เพื่อเรียนรู้การสร้างแผนที่สองมิติด้วย Matplotlib

เครื่องจักรจะเป็นแหล่งความร้อน เครื่องปรับอากาศจะเป็นแหล่งความเย็น และ sensor node แต่ละตัวจะติดตั้งอยู่คนละตำแหน่งภายในห้อง

> เนื้อหา ฟังก์ชันจำลอง และแบบฝึกหัดในบทนี้เรียบเรียงขึ้นใหม่สำหรับหลักสูตรนี้

## วิธีเรียนจากบทนี้

ตัวอย่างถูกแบ่งเป็นเซลล์สั้น ๆ สำหรับ Jupyter Notebook หรือ Google Colab:

1. คัดลอกโค้ดทีละเซลล์
2. รันตามลำดับจากบนลงล่าง
3. อ่านคำอธิบายใต้เซลล์ก่อนรันส่วนถัดไป
4. เมื่อทดลองเสร็จ สามารถดูสคริปต์ฉบับเต็มในโฟลเดอร์ [source-code](./source-code/)

หากเริ่ม Kernel หรือ Runtime ใหม่ ให้กลับมารันตั้งแต่เซลล์ที่ 1

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบบทนี้ คุณจะสามารถ:

- จัดเตรียมข้อมูลตำแหน่งและค่าจากเซนเซอร์
- สร้างกริดสองมิติด้วย `np.meshgrid()`
- วาดเส้นชั้นค่าด้วย `contour()`
- สร้างแผนที่สีด้วย `contourf()` และ `imshow()`
- วางตำแหน่งและค่าของ sensor node บนแผนที่
- ใช้ colormap และ colorbar ให้ตรงกับหน่วยของข้อมูล
- อธิบายข้อจำกัดของ interpolation จากเซนเซอร์จำนวนน้อย

---

## 1. เตรียมไลบรารี

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
~~~

- NumPy ใช้สร้างกริดและคำนวณค่าจำนวนมากพร้อมกัน
- Matplotlib ใช้สร้างกราฟและแผนที่สี
- ตัวอย่างนี้ไม่ต้องติดตั้ง Pandas หรือ SciPy เพิ่ม

หากยังไม่มีไลบรารี ให้ติดตั้งก่อน:

~~~bash
python3 -m pip install numpy matplotlib
~~~

---

## 2. สร้างแบบจำลองอุณหภูมิ

ห้องตัวอย่างมีขนาด 10 × 8 เมตร อุณหภูมิพื้นฐานอยู่ที่ 26 °C

### เซลล์ที่ 2 — ฟังก์ชันคำนวณอุณหภูมิ

~~~python
def make_temperature_field(x, y):
    room_temperature = 26.0

    machine_heat = 6.0 * np.exp(
        -(((x - 7.5) ** 2) / 2.0 + ((y - 2.0) ** 2) / 1.5)
    )

    air_conditioner = 4.0 * np.exp(
        -(((x - 1.0) ** 2) / 3.0 + ((y - 6.5) ** 2) / 2.0)
    )

    airflow = 0.4 * np.sin(np.pi * x / 5) * np.cos(np.pi * y / 4)

    return room_temperature + machine_heat - air_conditioner + airflow
~~~

ฟังก์ชันรับตำแหน่ง x และ y แล้วคืนค่าอุณหภูมิ ณ ตำแหน่งนั้น:

- `room_temperature` คืออุณหภูมิพื้นฐาน
- `machine_heat` เพิ่มอุณหภูมิใกล้เครื่องจักรตำแหน่ง (7.5, 2.0)
- `air_conditioner` ลดอุณหภูมิใกล้เครื่องปรับอากาศตำแหน่ง (1.0, 6.5)
- `airflow` จำลองความผันผวนเล็กน้อยจากการไหลของอากาศ
- คำสั่ง `return` นำผลทั้งสี่ส่วนมารวมกัน

นี่เป็นข้อมูลสังเคราะห์เพื่อการเรียนรู้ ไม่ใช่แบบจำลองทางวิศวกรรมความร้อน

### ทดลองคำนวณหนึ่งตำแหน่ง

~~~python
test_temperature = make_temperature_field(7.5, 2.0)
print(f"Temperature near the machine: {test_temperature:.1f} °C")
~~~

จุดนี้อยู่ใกล้เครื่องจักร ค่าที่ได้จึงควรสูงกว่าอุณหภูมิพื้นฐาน 26 °C

---

## 3. สร้างกริดของห้อง

### เซลล์ที่ 3 — สร้างพิกัดหนึ่งมิติ

~~~python
x = np.linspace(0, 10, 200)
y = np.linspace(0, 8, 160)
~~~

- x แทนความกว้างห้องตั้งแต่ 0–10 เมตร
- y แทนความสูงของแผนผังตั้งแต่ 0–8 เมตร
- จำนวน 200 และ 160 คือความละเอียดของกริด ไม่ใช่จำนวนเซนเซอร์จริง

### เซลล์ที่ 4 — เปลี่ยนพิกัดเป็นกริด

~~~python
X, Y = np.meshgrid(x, y)
~~~

`meshgrid()` นำพิกัดหนึ่งมิติมาสร้างเป็นตารางสองมิติ ทำให้เราคำนวณอุณหภูมิทุกตำแหน่งได้ในครั้งเดียว

### เซลล์ที่ 5 — คำนวณอุณหภูมิบนกริด

~~~python
temperature = make_temperature_field(X, Y)

print("Grid shape:", temperature.shape)
print("Minimum:", temperature.min())
print("Maximum:", temperature.max())
~~~

`temperature` เป็นเมทริกซ์ที่มีค่าอุณหภูมิหนึ่งค่าต่อหนึ่งตำแหน่งบนพื้นห้อง การพิมพ์ค่าต่ำสุดและสูงสุดช่วยตรวจสอบข้อมูลก่อนสร้างกราฟ

---

## 4. กำหนดตำแหน่ง sensor node

### เซลล์ที่ 6 — ตำแหน่งอุปกรณ์

~~~python
sensor_positions = np.array([
    [1, 1], [3, 2], [5, 1], [8, 1],
    [2, 4], [5, 4], [8, 4],
    [1, 7], [4, 7], [7, 7], [9, 7],
])
~~~

หนึ่งแถวแทน sensor node หนึ่งตัว โดยคอลัมน์แรกคือ x และคอลัมน์ที่สองคือ y

ตัวอย่าง `[8, 1]` หมายถึงอุปกรณ์ที่ติดตั้งห่างจากผนังซ้าย 8 เมตร และห่างจากผนังล่าง 1 เมตร

### เซลล์ที่ 7 — จำลองค่าที่อุปกรณ์วัดได้

~~~python
sensor_x = sensor_positions[:, 0]
sensor_y = sensor_positions[:, 1]

sensor_values = make_temperature_field(sensor_x, sensor_y)
~~~

การใช้ `[:, 0]` เลือกตำแหน่ง x ของทุกอุปกรณ์ ส่วน `[:, 1]` เลือกตำแหน่ง y

### เซลล์ที่ 8 — เพิ่ม measurement noise

~~~python
rng = np.random.default_rng(42)
sensor_values += rng.normal(0, 0.15, len(sensor_positions))
~~~

ตัวอย่างนี้เพิ่มความคลาดเคลื่อนแบบสุ่มประมาณ ±0.15 °C เพื่อให้ใกล้เคียงอุปกรณ์จริงมากขึ้น ค่า `42` ทำให้ได้ผลเดิมทุกครั้งที่รัน เหมาะกับการสอนและทดสอบ

ในงานจริงควรใช้ค่าความแม่นยำจาก datasheet และบันทึกประวัติ calibration ของอุปกรณ์

---

## 5. สร้างกราฟเส้นชั้นค่าด้วย `contour()`

Jupyter แบบ inline จะปิด Figure เมื่อจบเซลล์ ดังนั้นคำสั่งของกราฟหนึ่งรูปต้องเริ่มด้วย `plt.subplots()` และจบด้วย `plt.show()` ภายในเซลล์เดียวกัน

ก่อนสร้างกราฟ เราจะเขียนฟังก์ชันช่วยสำหรับตั้งค่าแกน ฟังก์ชันนี้ยังไม่สร้าง Figure จึงแยกเป็นเซลล์ได้

### เซลล์ที่ 9 — ฟังก์ชันจัดรูปแบบแผนผัง

~~~python
def format_room_axes(ax, title):
    ax.set(
        title=title,
        xlabel="Room width (m)",
        ylabel="Room height (m)",
        xlim=(0, 10),
        ylim=(0, 8),
        aspect="equal",
    )
~~~

ฟังก์ชันนี้ช่วยลดโค้ดซ้ำ โดยรับ Axes และชื่อกราฟ จากนั้นกำหนดชื่อแกน ขอบเขต และสัดส่วนของห้อง

### เซลล์ที่ 10 — สร้างกราฟ Contour ให้เสร็จในเซลล์เดียว

~~~python
fig, ax = plt.subplots(figsize=(8, 6))

levels = np.arange(22, 34, 1)
lines = ax.contour(
    X, Y, temperature,
    levels=levels,
    colors="black",
    linewidths=0.8,
)
ax.clabel(lines, inline=True, fontsize=8, fmt="%.0f °C")

ax.scatter(
    sensor_x, sensor_y,
    color="white",
    edgecolor="black",
    s=55,
    label="Temperature sensors",
)

format_room_axes(ax, "Temperature contour in a machine room")
ax.legend()
plt.show()
~~~

ลำดับการทำงานภายในเซลล์:

1. `plt.subplots()` สร้าง Figure และ Axes
2. `ax.contour()` วาดเส้นอุณหภูมิห่างกันระดับละ 1 °C
3. `ax.clabel()` ใส่ค่าอุณหภูมิบนเส้น
4. `ax.scatter()` วางตำแหน่ง sensor node
5. `format_room_axes()` จัดรูปแบบแผนผัง
6. `plt.show()` แสดงกราฟหลังประกอบเสร็จแล้ว

> อย่าแยกบรรทัด `fig, ax = plt.subplots(...)` ออกจากเซลล์นี้ มิฉะนั้น Notebook อาจแสดง Figure ว่างก่อนที่คำสั่งวาดกราฟจะทำงาน
---

## 6. สร้างแผนที่สีด้วย `contourf()`

กราฟนี้เป็น Figure รูปใหม่ จึงรวมคำสั่งทั้งหมดไว้ในอีกหนึ่งเซลล์

### เซลล์ที่ 11 — Filled Contour พร้อม Colorbar

~~~python
fig, ax = plt.subplots(figsize=(8, 6))

color_levels = np.arange(22, 34.5, 0.5)
filled = ax.contourf(
    X, Y, temperature,
    levels=color_levels,
    cmap="coolwarm",
    extend="both",
)

fig.colorbar(filled, ax=ax, label="Temperature (°C)")
ax.scatter(
    sensor_x, sensor_y,
    color="black",
    marker="x",
    label="Sensors",
)

format_room_axes(ax, "Machine-room temperature map")
ax.legend()
plt.show()
~~~

- `color_levels` กำหนดช่วงสีห่างกัน 0.5 °C
- `contourf()` ระบายสีพื้นที่ระหว่างระดับ
- `coolwarm` ใช้สีน้ำเงินแทนบริเวณเย็นและสีแดงแทนบริเวณร้อน
- `extend="both"` ทำให้ colorbar แจ้งเมื่อค่าหลุดจากช่วงที่กำหนด
- colorbar ต้องมีชื่อและหน่วยเพื่อให้ผู้อ่านตีความสีได้ถูกต้อง
---

## 7. แสดงข้อมูลด้วย `imshow()`

`imshow()` เหมาะกับข้อมูลที่อยู่บนกริดสม่ำเสมอ เช่น thermal camera หรือเซนเซอร์ที่ติดตั้งเป็นแถวและคอลัมน์

### เซลล์ที่ 12 — แสดงเมทริกซ์อุณหภูมิเป็นภาพ

~~~python
fig, ax = plt.subplots(figsize=(8, 6))

image = ax.imshow(
    temperature,
    extent=[0, 10, 0, 8],
    origin="lower",
    cmap="coolwarm",
    vmin=22,
    vmax=34,
    aspect="equal",
)

fig.colorbar(image, ax=ax, label="Temperature (°C)")
format_room_axes(ax, "Temperature field shown as an image")
plt.show()
~~~

- `extent` จับขอบภาพให้ตรงกับขนาดห้องจริง
- `origin="lower"` กำหนดจุด (0, 0) ให้อยู่มุมซ้ายล่าง
- `vmin` และ `vmax` ล็อกช่วงสีไว้ที่ 22–34 °C
- การล็อกช่วงสีสำคัญเมื่อเปรียบเทียบข้อมูลต่างเวลา เพราะสีเดียวกันจะหมายถึงค่าเดียวกันเสมอ
- หากไม่กำหนด `extent` แกนจะแสดงหมายเลขแถวและคอลัมน์ของเมทริกซ์แทนตำแหน่งจริง
---

## 8. รวมภาพสี เส้นระดับ และค่าจากเซนเซอร์

กราฟสุดท้ายรวมภาพรวมของอุณหภูมิ ระดับสำคัญ ตำแหน่งอุปกรณ์ และค่าที่วัดได้ไว้ด้วยกัน

### เซลล์ที่ 13 — สร้าง IoT Temperature Dashboard

~~~python
fig, ax = plt.subplots(figsize=(9, 6))

image = ax.imshow(
    temperature,
    extent=[0, 10, 0, 8],
    origin="lower",
    cmap="coolwarm",
    vmin=22,
    vmax=34,
    aspect="equal",
)

lines = ax.contour(
    X, Y, temperature,
    levels=[24, 26, 28, 30, 32],
    colors="black",
    linewidths=0.8,
)
ax.clabel(lines, inline=True, fontsize=8, fmt="%.0f °C")

ax.scatter(
    sensor_x, sensor_y,
    color="white",
    edgecolor="black",
    s=65,
)

for index, ((x_pos, y_pos), value) in enumerate(
    zip(sensor_positions, sensor_values),
    start=1,
):
    ax.annotate(
        f"T{index}: {value:.1f}",
        (x_pos, y_pos),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=7,
    )

fig.colorbar(image, ax=ax, label="Temperature (°C)")
format_room_axes(ax, "IoT temperature monitoring")
plt.show()
~~~

กราฟนี้ประกอบด้วย:

1. `imshow()` แสดงภาพรวมของอุณหภูมิ
2. `contour()` แสดงขอบเขตระดับสำคัญ
3. `scatter()` แสดงตำแหน่งที่มีการวัดจริง
4. `annotate()` แสดงรหัสและค่าของ sensor node
5. colorbar อธิบายความสัมพันธ์ระหว่างสีกับอุณหภูมิ

`zip()` จับคู่ตำแหน่งกับค่าของอุปกรณ์ ส่วน `enumerate(..., start=1)` ใช้สร้างรหัส T1, T2 และ T3 ตามลำดับ
---

## 9. เมื่อนำข้อมูลเซนเซอร์จริงมาใช้

ตัวอย่างด้านบนใช้ฟังก์ชันคำนวณค่าทุกตำแหน่ง แต่ระบบ IoT จริงมักมีจุดวัดเพียงไม่กี่จุด

- หากเซนเซอร์ติดตั้งเป็นกริด สามารถจัดค่าเป็นเมทริกซ์ได้โดยตรง
- หากตำแหน่งกระจายไม่สม่ำเสมอ ต้องทำ interpolation ก่อน
- ไม่ควรแสดงพื้นที่ไกลเกินขอบเขตเซนเซอร์โดยไม่มีคำเตือน
- เก็บค่าที่หายไปเป็น `NaN`
- แสดงสถานะอุปกรณ์ offline แยกจากค่าปกติ
- เลือกข้อมูลจาก timestamp เดียวกันหรือใกล้เคียงกัน
- ตรวจสอบ outlier, sensor drift, calibration และหน่วยก่อนวาดกราฟ

โครงสร้างข้อมูลที่แนะนำ:

| ฟิลด์ | ตัวอย่าง | ความหมาย |
|------|----------|----------|
| `device_id` | `temp-07` | รหัสอุปกรณ์ |
| `timestamp` | `2026-07-17T10:30:00Z` | เวลาที่วัด |
| `x`, `y` | `7.5, 2.0` | ตำแหน่งติดตั้ง |
| `value` | `31.4` | ค่าที่วัดได้ |
| `unit` | `°C` | หน่วย |
| `status` | `online` | สถานะอุปกรณ์ |

ข้อมูลตำแหน่งไม่สม่ำเสมอสามารถศึกษา `scipy.interpolate.griddata` เพิ่มเติมได้ แต่ต้องเลือกวิธี interpolation ให้เหมาะกับธรรมชาติของข้อมูล ไม่ใช่เลือกเพียงเพราะภาพดูเรียบ

---

## 10. ประยุกต์กับเซนเซอร์ IoT ชนิดอื่น

| ตัวแปร | หน่วยตัวอย่าง | การใช้งาน | Colormap ตัวอย่าง |
|--------|---------------|-----------|-------------------|
| อุณหภูมิ | °C | ห้องเครื่อง, cold chain, data center | `coolwarm`, `inferno` |
| ความชื้นสัมพัทธ์ | %RH | อาคาร, คลังสินค้า, ฟาร์ม | `Blues`, `YlGnBu` |
| PM2.5 | µg/m³ | คุณภาพอากาศ | `YlOrRd` |
| CO₂ | ppm | การระบายอากาศในอาคาร | `viridis`, `YlOrRd` |
| ความชื้นดิน | % หรือ ADC | Smart farming | `YlGnBu` |
| RSSI | dBm | ตรวจสอบ Wi-Fi หรือ LoRa | `viridis` |
| แรงสั่นสะเทือน RMS | mm/s หรือ g | Predictive maintenance | `magma`, `inferno` |
| ระดับเสียง | dB | โรงงานและ Smart city | `plasma` |

ช่วงสีและ threshold ควรอ้างอิงข้อกำหนดของระบบจริง ไม่ควรปรับตามค่าสูงสุดและต่ำสุดของข้อมูลทุกครั้ง เพราะจะทำให้สีเดียวกันเปลี่ยนความหมาย

---

## 11. เลือกใช้ฟังก์ชันไหนดี

| ฟังก์ชัน | เหมาะกับ | จุดเด่น |
|----------|-----------|---------|
| `contour()` | ต้องการเห็นขอบเขต threshold | ระบุเส้นเตือนภัยได้ชัด |
| `contourf()` | ต้องการเปรียบเทียบพื้นที่สูง–ต่ำ | ควบคุมระดับสีได้ละเอียด |
| `imshow()` | ข้อมูลอยู่บนกริดสม่ำเสมอ | แสดงผลเร็ว เหมาะกับ heatmap |
| ใช้ร่วมกัน | IoT Dashboard | เห็นภาพรวม ระดับ และจุดเซนเซอร์ |

## แนวทางสำหรับ IoT Dashboard

- แสดงหน่วยบน colorbar และ tooltip
- ใช้ช่วงสีคงที่เมื่อเปรียบเทียบข้อมูลต่างเวลา
- แสดงตำแหน่ง sensor node
- แยกสีของอุปกรณ์ offline หรือข้อมูลเก่า
- แสดงเวลาอัปเดตล่าสุด
- ใช้ threshold จากข้อกำหนดของระบบ
- ระบุว่าพื้นที่ระหว่างเซนเซอร์เป็นค่าประมาณ

---

## แบบฝึกหัด

1. เปลี่ยนตำแหน่งเครื่องจักรและเครื่องปรับอากาศ
2. เพิ่ม sensor node ใกล้จุดร้อนอีกสองตัว
3. ทำเส้น 30 °C ให้เป็นสีแดงและหนากว่าเส้นอื่น
4. จำลองอุปกรณ์ T3 และ T8 ให้ offline
5. เปลี่ยนกรณีศึกษาจากอุณหภูมิเป็นความชื้นสัมพัทธ์
6. สร้างกราฟสามช่องเพื่อเปรียบเทียบ `contour()`, `contourf()` และ `imshow()`

อ่านโจทย์ฉบับเต็มได้ที่ [แบบฝึกหัด EP4](./exercises/exercise01.md)

## โจทย์ท้าทายย่อย

เลือกหนึ่งสถานการณ์:

- แผนที่ PM2.5 ในอาคาร
- แผนที่ความชื้นดินในแปลงเกษตร
- แผนที่ RSSI สำหรับ LoRa หรือ Wi-Fi
- แผนที่แรงสั่นสะเทือนรอบเครื่องจักร

สร้าง Dashboard ที่มีแผนที่สี เส้น threshold ตำแหน่งอุปกรณ์ หน่วย สถานะ online/offline เวลาอัปเดต และคำอธิบายบริเวณที่เป็นค่าจาก interpolation

---

## สคริปต์ฉบับเต็ม

เมื่อเข้าใจแต่ละเซลล์แล้ว สามารถคัดลอกหรือรันไฟล์ฉบับเต็มได้จาก:

- [contour_lines.py](./source-code/contour_lines.py)
- [filled_contour.py](./source-code/filled_contour.py)
- [image_and_contour.py](./source-code/image_and_contour.py)

## ตอนถัดไป

**EP5 — Histograms, Binning, and Density**
