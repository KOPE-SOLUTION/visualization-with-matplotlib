# EP4 — Density and Contour Plots for IoT Sensor Data

อุปกรณ์ IoT มักส่งค่าที่ผูกกับตำแหน่ง เช่น อุณหภูมิในโรงงาน ความชื้นในแปลงเกษตร หรือความแรงสัญญาณไร้สาย บทนี้จะใช้ **ระบบติดตามอุณหภูมิในห้องเครื่องจักร** เป็นกรณีศึกษา เพื่อเรียนรู้การสร้างแผนที่สองมิติด้วย Matplotlib

เครื่องจักรจะเป็นแหล่งความร้อน เครื่องปรับอากาศจะเป็นแหล่งความเย็น และ sensor node แต่ละตัวจะติดตั้งอยู่คนละตำแหน่งภายในห้อง

## วิธีเรียนจากบทนี้

ตัวอย่างถูกแบ่งเป็นเซลล์สั้น ๆ สำหรับ Jupyter Notebook หรือ Google Colab:

1. คัดลอกโค้ดทีละเซลล์
2. รันตามลำดับจากบนลงล่าง
3. อ่านคำอธิบายใต้เซลล์ก่อนรันส่วนถัดไป
4. เมื่อทดลองเสร็จ สามารถดูสคริปต์ฉบับเต็มในโฟลเดอร์ [source-code](./source-code/)

หากเริ่ม Kernel หรือ Runtime ใหม่ ให้กลับมารันตั้งแต่เซลล์ที่ 1

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบบทนี้ คุณจะสามารถ:

- อธิบายข้อมูลเชิงพื้นที่ในรูป X, Y และ Z
- จัดเตรียมตำแหน่งและค่าจาก sensor node
- จำลอง measurement noise และแยก noise ออกจาก bias หรือ drift
- สร้างกริดสองมิติด้วย `np.meshgrid()`
- อธิบายความหมายของเส้นชั้นค่าและวาดด้วย `contour()`
- สร้างแผนที่สีด้วย `contourf()` และ `imshow()`
- เลือก colormap, colorbar และช่วงสีให้ตรงกับข้อมูล
- วางตำแหน่งและค่าของ sensor node บนแผนที่
- ทำ interpolation จากจุดวัดที่กระจายอยู่ไปยังกริด
- อธิบายข้อจำกัดและความไม่แน่นอนของแผนที่จากข้อมูลเซนเซอร์จริง
- วางแนวทางนำกราฟไปใช้กับ IoT Dashboard และ Smart Factory

## ภาพรวมแนวคิดก่อนเริ่ม

### ข้อมูล X, Y และ Z คืออะไร

ข้อมูลเชิงพื้นที่หนึ่งจุดประกอบด้วยสามส่วน:

| ตัวแปร | ความหมายในตัวอย่าง | ตัวอย่าง |
|--------|---------------------|----------|
| X | ตำแหน่งตามความกว้างห้อง | 7.5 เมตร |
| Y | ตำแหน่งตามความสูงของแผนผัง | 2.0 เมตร |
| Z | ค่าที่วัดได้ ณ ตำแหน่งนั้น | 31.4 °C |

ในกราฟสองมิติ X และ Y เป็นแกน ส่วน Z ไม่ได้สร้างเป็นแกนที่สาม แต่สื่อด้วยเส้น สี หรือความเข้มของสี

### Contour คืออะไร

**Contour หรือเส้นชั้นค่า** คือเส้นที่เชื่อมตำแหน่งซึ่งมีค่า Z เท่ากัน ตัวอย่างเช่น เส้น 30 °C จะลากผ่านทุกตำแหน่งที่มีอุณหภูมิ 30 °C แนวคิดเดียวกันพบได้ในเส้นระดับความสูงบนแผนที่ภูมิประเทศและเส้นความกดอากาศบนแผนที่อากาศ

สิ่งที่อ่านได้จาก Contour:

- ตัวเลขบนเส้นบอกค่าของระดับนั้น
- เส้นที่อยู่ใกล้กันหมายถึงค่าเปลี่ยนเร็วในระยะทางสั้น
- เส้นวงปิดอาจล้อมรอบจุดสูงสุดหรือต่ำสุด
- รูปร่างของเส้นช่วยบอกขอบเขตของ hot spot หรือพื้นที่เกิน threshold

### Interpolation คืออะไร

Sensor node วัดค่าได้เฉพาะตำแหน่งที่ติดตั้ง แต่แผนที่ต้องการค่าบนพื้นที่ต่อเนื่อง **Interpolation** คือการประมาณค่าระหว่างจุดที่วัดได้ โดยอาศัยค่าจากเซนเซอร์ใกล้เคียง

ค่าจาก Interpolation ไม่ใช่ค่าที่วัดจริง และไม่ควรถูกนำเสนอว่ามีความแม่นยำเท่ากับตำแหน่ง sensor node ยิ่งเซนเซอร์ห่างกันมากหรือมีสิ่งกีดขวางทางกายภาพ ความไม่แน่นอนยิ่งสูง

---

## 1. เตรียมไลบรารี

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
~~~

- NumPy ใช้สร้างกริดและคำนวณค่าจำนวนมากพร้อมกัน
- Matplotlib ใช้สร้างกราฟและแผนที่สี
- ตัวอย่างหลักใช้เพียง NumPy และ Matplotlib ส่วนหัวข้อ Interpolation จะติดตั้ง SciPy เพิ่มภายหลัง

หากยังไม่มีไลบรารี ให้ติดตั้งก่อน:

~~~bash
python -m pip install numpy matplotlib
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

`meshgrid()` นำพิกัดหนึ่งมิติมาสร้างเป็นตารางพิกัดสองมิติ:

- `X[row, column]` เก็บตำแหน่งตามแกน x
- `Y[row, column]` เก็บตำแหน่งตามแกน y
- คู่ X และ Y ที่ index เดียวกันระบุตำแหน่งหนึ่งช่องบนพื้นห้อง
- เมื่อส่ง X และ Y เข้า `make_temperature_field()` จะได้ Z หรืออุณหภูมิของทุกช่อง

ตรวจสอบขนาดได้ด้วย:

~~~python
print("X shape:", X.shape)
print("Y shape:", Y.shape)
~~~

X, Y และอาร์เรย์อุณหภูมิที่นำไปใช้กับ `contour()` ต้องมี shape เดียวกัน
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

### เซลล์ที่ 8 — เพิ่ม Measurement Noise

~~~python
true_sensor_values = make_temperature_field(sensor_x, sensor_y)

rng = np.random.default_rng(42)
measurement_noise = rng.normal(
    loc=0.0,
    scale=0.15,
    size=len(sensor_positions),
)

sensor_values = true_sensor_values + measurement_noise
~~~

ตัวอย่างนี้แยกสามสิ่งออกจากกัน:

- `true_sensor_values` คือค่าจากแบบจำลองก่อนเกิดความคลาดเคลื่อน
- `measurement_noise` คือความผันผวนแบบสุ่ม
- `sensor_values` คือค่าที่อุปกรณ์รายงานหลังรวม noise

`loc=0.0` หมายถึง noise ไม่มีแนวโน้มเพิ่มหรือลดค่าอย่างถาวร ส่วน `scale=0.15` คือส่วนเบี่ยงเบนมาตรฐาน 0.15 °C ไม่ได้หมายความว่าทุกค่าจะอยู่ภายใน ±0.15 °C เสมอ

ตรวจสอบผลของ noise ได้ด้วย:

~~~python
for index, (true_value, measured_value) in enumerate(
    zip(true_sensor_values, sensor_values),
    start=1,
):
    error = measured_value - true_value
    print(
        f"T{index}: true={true_value:.2f}, "
        f"measured={measured_value:.2f}, error={error:+.2f} °C"
    )
~~~

คำที่มักสับสน:

- **Noise** คือความผันผวนแบบสุ่มระหว่างการวัด
- **Bias** คือค่าที่คลาดไปด้านใดด้านหนึ่งอย่างสม่ำเสมอ
- **Drift** คือ bias ที่ค่อย ๆ เปลี่ยนตามเวลา
- **Accuracy** บอกว่าค่าใกล้ค่าจริงเพียงใด
- **Precision** บอกว่าการวัดซ้ำให้ค่าใกล้กันเพียงใด

ในงานจริงควรอ้างอิง accuracy จาก datasheet ตรวจสอบ calibration และเก็บ timestamp เพื่อวิเคราะห์ drift
---

## 5. สร้างกราฟเส้นชั้นค่าด้วย `contour()`

`contour()` รับกริด X, Y และค่าบนกริด Z แล้วค้นหาตำแหน่งที่ Z ตัดผ่านแต่ละระดับ จากนั้นเชื่อมตำแหน่งเหล่านั้นเป็นเส้น

ในตัวอย่างแรก ค่า Z มาจาก `make_temperature_field()` ซึ่งเป็นสนามอุณหภูมิจำลองที่เรารู้ค่าทุกตำแหน่ง กราฟนี้จึงใช้สอนวิธีอ่าน Contour ก่อน ส่วนแผนที่ที่สร้างจาก sensor node เพียงไม่กี่จุดจะทำในหัวข้อ Interpolation ภายหลัง

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

### วิธีอ่านผลลัพธ์

- เส้นที่มีป้าย 30 °C คือขอบเขตซึ่งอุณหภูมิเท่ากับ 30 °C
- บริเวณด้านในไม่ได้ร้อนกว่าเสมอ ต้องดูค่าของเส้นข้างเคียงประกอบ
- เส้นที่เบียดกันใกล้เครื่องจักรแสดงว่าอุณหภูมิเปลี่ยนเร็วตามระยะทาง
- จุดเซนเซอร์สีขาวแสดงตำแหน่งวัด แต่เส้นในกราฟนี้ยังมาจากสนามจำลอง ไม่ได้คำนวณจากจุดเหล่านั้น

> อย่าแยกบรรทัดที่สร้าง Figure ออกจากเซลล์นี้ มิฉะนั้น Notebook อาจแสดง Figure ว่างก่อนที่คำสั่งวาดกราฟจะทำงาน

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
### Filled Contour ต่างจาก Contour อย่างไร

`contour()` วาดเฉพาะเส้นที่มีค่าเท่ากัน ส่วน `contourf()` ระบายสีพื้นที่ระหว่างระดับ ตัวอย่างนี้แบ่งอุณหภูมิทุก 0.5 °C ดังนั้นสีหนึ่งแถบหมายถึง “ช่วงค่า” ไม่ใช่ค่าจุดเดียว

จำนวนระดับที่มากขึ้นทำให้ภาพดูละเอียดขึ้น แต่ไม่ได้ทำให้ข้อมูลจากเซนเซอร์แม่นยำขึ้น ความละเอียดของภาพและความแม่นยำของการวัดเป็นคนละเรื่องกัน
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
### Heatmap ในบทนี้หมายถึงอะไร

Heatmap คือภาพที่ใช้สีแทนขนาดของค่า `imshow()` แสดงสมาชิกในเมทริกซ์เป็นพิกเซล จึงไม่ได้คำนวณเส้นหรือทำ interpolation ให้โดยอัตโนมัติ ข้อมูลต้องถูกจัดให้อยู่บนกริดก่อนแล้ว

ความแตกต่างสำคัญ:

- `contour()` เน้นเส้นระดับ
- `contourf()` เน้นช่วงค่าระหว่างเส้น
- `imshow()` เน้นเมทริกซ์หรือภาพพิกเซล และมักแสดงผลได้รวดเร็ว
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

## 9. เลือก Colormap และ Colorbar ให้เหมาะกับข้อมูล

Colormap คือกฎที่แปลงค่าตัวเลขเป็นสี ส่วน Colorbar คือมาตรวัดที่บอกว่าสีแต่ละสีหมายถึงค่าเท่าใด ทั้งสองอย่างต้องออกแบบร่วมกัน

ประเภทที่ใช้บ่อย:

| ประเภท | ลักษณะข้อมูล | ตัวอย่าง |
|--------|---------------|----------|
| Sequential | ค่าจากน้อยไปมาก ไม่มีค่ากลางพิเศษ | `viridis`, `Blues`, `inferno` |
| Diverging | มีค่ากลางสำคัญ เช่น ค่าปกติหรือศูนย์ | `coolwarm`, `RdBu` |
| Categorical | กลุ่มที่ไม่มีลำดับ | ไม่เหมาะกับอุณหภูมิต่อเนื่อง |

`coolwarm` เหมาะกับบทนี้เมื่อเราต้องการเน้นบริเวณเย็นและร้อนรอบค่าปกติ แต่ถ้าต้องการสื่อเพียง “ต่ำไปสูง” ควรทดลอง `viridis` หรือ `inferno`

### เซลล์ที่ 14 — เปรียบเทียบ Colormap

~~~python
fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharex=True, sharey=True)

colormaps = ["viridis", "inferno", "coolwarm"]
images = []

for ax, cmap_name in zip(axes, colormaps):
    image = ax.imshow(
        temperature,
        extent=[0, 10, 0, 8],
        origin="lower",
        cmap=cmap_name,
        vmin=22,
        vmax=34,
        aspect="equal",
    )
    images.append(image)
    ax.set_title(cmap_name)
    ax.set_xlabel("Room width (m)")

axes[0].set_ylabel("Room height (m)")
fig.colorbar(
    images[-1],
    ax=axes,
    label="Temperature (°C)",
    shrink=0.85,
)
plt.show()
~~~

หลักปฏิบัติสำหรับ Dashboard:

- ใส่ชื่อตัวแปรและหน่วยบน Colorbar
- ล็อก `vmin` และ `vmax` เมื่อต้องเปรียบเทียบหลายเวลา
- ใช้ช่วงสีเดียวกันสำหรับอุปกรณ์ชนิดเดียวกัน
- อย่าเลือกสีเพียงเพราะดูสวย ต้องตรวจว่าสื่อ “สูง–ต่ำ” ถูกต้อง
- หลีกเลี่ยงสีที่ทำให้ผู้มีภาวะตาบอดสีแยกค่าหลักไม่ได้
- ใช้สีเตือนภัยตามมาตรฐานของระบบ ไม่ใช่เปลี่ยนตามข้อมูลแต่ละรอบ

---

## 10. สร้างแผนที่จากจุดเซนเซอร์ด้วย Interpolation

กราฟก่อนหน้านี้ใช้สนามอุณหภูมิจำลองซึ่งรู้ค่าทุกตำแหน่ง แต่ข้อมูลจริงมีเพียง X, Y และค่าจาก sensor node แต่ละตัว เราจึงต้องประมาณค่าบนกริดก่อนส่งให้ `contourf()` หรือ `imshow()`

ติดตั้ง SciPy สำหรับตัวอย่างนี้:

~~~bash
python -m pip install scipy
~~~

วิธีที่พบบ่อยใน `scipy.interpolate.griddata`:

| Method | ลักษณะ | ข้อควรระวัง |
|--------|---------|---------------|
| `nearest` | ใช้ค่าจากจุดที่ใกล้ที่สุด | ภาพเป็นปื้นและกระโดด แต่ไม่สร้างค่าสูงหรือต่ำใหม่ |
| `linear` | เชื่อมค่าระหว่างจุดแบบเส้นตรง | บริเวณนอกขอบเขตจุดวัดจะเป็น NaN |
| `cubic` | ผิวเรียบกว่า | อาจ overshoot และสร้างค่าที่สูงหรือต่ำกว่าจุดวัด |

### เซลล์ที่ 15 — Interpolate จุดวัดไปยังกริด

~~~python
from scipy.interpolate import griddata

interpolated_temperature = griddata(
    points=sensor_positions,
    values=sensor_values,
    xi=(X, Y),
    method="linear",
)

interpolated_temperature = np.ma.masked_invalid(
    interpolated_temperature
)
~~~

- `points` คือตำแหน่ง X, Y ที่วัดจริง
- `values` คือค่าจากอุปกรณ์
- `xi` คือกริดปลายทาง
- `method="linear"` ประมาณค่าระหว่างจุดแบบเส้นตรง
- `masked_invalid()` ซ่อนพื้นที่นอกขอบเขตที่คำนวณไม่ได้ แทนการเติมค่าที่อาจทำให้เข้าใจผิด

### เซลล์ที่ 16 — วาดแผนที่ที่ได้จาก Sensor Node

~~~python
fig, ax = plt.subplots(figsize=(8, 6))

filled = ax.contourf(
    X,
    Y,
    interpolated_temperature,
    levels=np.arange(22, 34.5, 0.5),
    cmap="coolwarm",
    extend="both",
)

ax.scatter(
    sensor_x,
    sensor_y,
    c=sensor_values,
    cmap="coolwarm",
    vmin=22,
    vmax=34,
    edgecolor="black",
    s=80,
    label="Measured locations",
)

fig.colorbar(filled, ax=ax, label="Estimated temperature (°C)")
format_room_axes(ax, "Temperature estimated from IoT sensors")
ax.legend()
plt.show()
~~~

ตอนนี้พื้นที่สีสร้างจากค่าของ sensor node จริงในตัวอย่าง ไม่ได้ใช้สนามอุณหภูมิเต็มโดยตรง จุดที่อยู่นอกขอบเขตการติดตั้งเซนเซอร์จะไม่มีสี เพราะ Linear Interpolation ไม่ควรคาดเดาออกไปไกลจากจุดวัด

### เซลล์ที่ 17 — ประเมินความคลาดเคลื่อนของ Interpolation

ในข้อมูลจำลอง เรารู้ค่าอุณหภูมิจริงทุกตำแหน่ง จึงเปรียบเทียบกับค่าประมาณได้:

~~~python
valid_area = ~interpolated_temperature.mask

mean_absolute_error = np.mean(
    np.abs(
        interpolated_temperature.data[valid_area]
        - temperature[valid_area]
    )
)

print(f"Interpolation MAE: {mean_absolute_error:.2f} °C")
~~~

ในงานจริงเราไม่รู้ค่าจริงทุกตำแหน่ง วิธีประเมินที่เหมาะกว่าคือซ่อนข้อมูลเซนเซอร์บางตัวไว้ ทำ Interpolation จากเซนเซอร์ที่เหลือ แล้วเปรียบเทียบค่าประมาณกับค่าที่ซ่อนไว้ แนวทางนี้คล้าย cross-validation

### ข้อจำกัดสำคัญของ Interpolation

- ผลลัพธ์ขึ้นกับจำนวนและตำแหน่งเซนเซอร์
- เครื่องจักร ผนัง และทิศทางลมอาจทำให้จุดที่อยู่ใกล้กันมีค่าต่างกัน
- ภาพที่เรียบไม่ได้แปลว่าค่ามีความแม่นยำสูง
- อย่าเพิ่มจำนวน grid แล้วอ้างว่าความละเอียดของการวัดเพิ่มขึ้น
- จุดวัดต้องมาจาก timestamp เดียวกันหรือช่วงเวลาที่ใกล้กัน
- ควรแสดงตำแหน่ง sensor node ทับบนแผนที่เสมอ
- พื้นที่นอกขอบเขตจุดวัดเป็น Extrapolation ซึ่งเสี่ยงกว่า Interpolation
- ระบบที่มีความเสี่ยงสูงควรใช้แบบจำลองทางฟิสิกส์หรือการตรวจสอบเพิ่มเติม

---

## 11. เมื่อนำข้อมูลเซนเซอร์จริงมาใช้

ตัวอย่างในบทนี้มีทั้งสนามอุณหภูมิจำลองที่รู้ค่าทุกตำแหน่ง และแผนที่ที่ประมาณจาก sensor node เพียงไม่กี่จุด เมื่อเปลี่ยนไปใช้ข้อมูลจริงต้องแยกค่าที่วัดได้ออกจากค่าที่ประมาณอย่างชัดเจน

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

## 12. ประยุกต์กับเซนเซอร์ IoT ชนิดอื่น

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

## 13. เลือกใช้ฟังก์ชันไหนดี

| ฟังก์ชัน | เหมาะกับ | จุดเด่น |
|----------|-----------|---------|
| `contour()` | ต้องการเห็นขอบเขต threshold | ระบุเส้นเตือนภัยได้ชัด |
| `contourf()` | ต้องการเปรียบเทียบพื้นที่สูง–ต่ำ | ควบคุมระดับสีได้ละเอียด |
| `imshow()` | ข้อมูลอยู่บนกริดสม่ำเสมอ | แสดงผลเร็ว เหมาะกับ heatmap |
| ใช้ร่วมกัน | IoT Dashboard | เห็นภาพรวม ระดับ และจุดเซนเซอร์ |

## 14. แนวทางสำหรับ IoT Dashboard

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
6. ทดลอง Interpolation แบบ nearest, linear และ cubic แล้วเปรียบเทียบผล
7. สร้างกราฟสามช่องเพื่อเปรียบเทียบ `contour()`, `contourf()` และ `imshow()`

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
- [sensor_interpolation.py](./source-code/sensor_interpolation.py)

## ตอนถัดไป

**EP5 — Histograms, Binning, and Density**
