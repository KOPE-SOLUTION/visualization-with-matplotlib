# EP5 — Histograms, Binning, and Density for IoT Sensor Data

Histogram ช่วยเปลี่ยนข้อมูลเซนเซอร์จำนวนมากให้เป็นภาพการกระจายที่อ่านง่าย เราสามารถใช้ตรวจสอบค่าปกติ ความผันผวน จุดผิดปกติ และรูปแบบการทำงานหลายสถานะของเครื่องจักรได้

บทนี้ใช้ข้อมูล IoT สังเคราะห์สามประเภท:
- อุณหภูมิห้องเครื่องจักร
- แรงสั่นสะเทือนในสถานะปกติและสถานะเตือน
- ความสัมพันธ์ระหว่างกระแสไฟกับอุณหภูมิมอเตอร์

> เนื้อหา ชุดข้อมูลจำลอง ตัวอย่าง และแบบฝึกหัดในบทนี้เรียบเรียงขึ้นใหม่สำหรับหลักสูตรนี้

## วิธีเรียนจากบทนี้

- คัดลอกเซลล์ตามลำดับจากบนลงล่าง
- ส่วนเตรียมข้อมูลสามารถแยกเป็นเซลล์สั้นได้
- คำสั่งสร้างกราฟหนึ่งรูปต้องเริ่มด้วย `plt.subplots()` และจบด้วย `plt.show()` ในเซลล์เดียว
- สคริปต์ฉบับเต็มอยู่ในโฟลเดอร์ [source-code](./source-code/)

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบบทนี้ คุณจะสามารถ:

- อธิบายความหมายของ Histogram, Bin, Count และ Density
- เลือกจำนวน Bin และขอบ Bin ให้เหมาะกับข้อมูล
- แยก Probability Density ออกจากจำนวนและเปอร์เซ็นต์
- เปรียบเทียบการกระจายของข้อมูลหลายชุดด้วย Shared Bin Edges
- คำนวณ Histogram โดยไม่ต้องสร้างกราฟ
- สร้าง Histogram สองมิติและ Hexagonal Binning
- อธิบาย KDE, Kernel และ Bandwidth
- คำนวณ Percentile และ Threshold เบื้องต้น
- ประยุกต์กราฟกับงาน IoT, IIoT และ Predictive Maintenance

## คำศัพท์สำคัญก่อนเริ่ม

| คำศัพท์ | ความหมาย |
|---------|----------|
| Distribution | รูปแบบการกระจายของข้อมูล เช่น ค่าส่วนใหญ่อยู่ตรงไหน กระจายกว้างเพียงใด และมีกี่กลุ่ม |
| Histogram | กราฟที่แบ่งช่วงค่าเป็น Bin แล้วนับจำนวนข้อมูลในแต่ละช่วง |
| Bin | ช่วงค่าหนึ่งช่วง เช่น 24–26 °C |
| Bin edge | ค่าขอบซ้ายและขวาของแต่ละ Bin |
| Count | จำนวนข้อมูลที่ตกอยู่ใน Bin |
| Density | ความหนาแน่นของข้อมูลต่อหนึ่งหน่วยบนแกน X ไม่ใช่จำนวนข้อมูลโดยตรง |
| Probability Density | Density ที่ปรับสเกลให้พื้นที่รวมใต้กราฟเท่ากับ 1 |
| KDE | Kernel Density Estimation วิธีประมาณเส้น Density แบบต่อเนื่องจากข้อมูลตัวอย่าง |
| RMS | Root Mean Square ค่าที่ใช้สรุปขนาดโดยรวมของสัญญาณ เช่น แรงสั่นสะเทือน |
| Threshold | ค่าขอบเขตที่ใช้แบ่งสถานะ เช่น Normal, Warning หรือ Critical |
| Edge Gateway | อุปกรณ์หรือคอมพิวเตอร์ที่รับและประมวลผลข้อมูลใกล้ Sensor ก่อนส่งต่อ |
| Cloud | ระบบส่วนกลางสำหรับจัดเก็บ วิเคราะห์ และแสดงผลข้อมูล |
| Telemetry | ข้อมูลที่อุปกรณ์ส่งกลับมาอย่างต่อเนื่อง เช่น อุณหภูมิ กระแสไฟ หรือ Vibration |
| Sampling Rate | จำนวนครั้งที่วัดต่อหนึ่งหน่วยเวลา เช่น 1 Hz คือหนึ่งครั้งต่อวินาที |
| Operating Region | บริเวณค่าที่เครื่องจักรมักทำงานอยู่ตามปกติ |
| Predictive Maintenance | การใช้ข้อมูลสภาพเครื่องจักรช่วยวางแผนบำรุงรักษาก่อนเกิดความเสียหาย |

คำศัพท์เหล่านี้จะถูกนำไปใช้และอธิบายเพิ่มเติมในแต่ละหัวข้อ

---

## 1. เตรียมไลบรารี

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
~~~

<br>

ตัวอย่างหลักใช้ NumPy และ Matplotlib หากต้องการทดลอง KDE ในส่วนท้าย ให้ติดตั้ง SciPy เพิ่มเติม:

~~~bash
python -m pip install numpy matplotlib scipy
~~~

---

## 2. จำลองข้อมูลอุณหภูมิจาก IoT Sensor

สมมติว่า Gateway เก็บข้อมูลอุณหภูมิจากห้องเครื่องจักร โดยข้อมูลส่วนใหญ่เป็นการทำงานปกติ แต่บางช่วงเครื่องจักรร้อนกว่าปกติ

### เซลล์ที่ 2 — สร้างข้อมูล

~~~python
rng = np.random.default_rng(42)

normal_temperature = rng.normal(loc=26.0, scale=1.1, size=1800)
hot_cycle = rng.normal(loc=31.5, scale=0.8, size=200)

temperature = np.concatenate([normal_temperature, hot_cycle])
~~~

- `loc` คือค่ากลางของข้อมูล
- `scale` คือส่วนเบี่ยงเบนมาตรฐาน
- `size` คือจำนวนค่าที่จำลอง
- ข้อมูลชุดเล็กที่มีค่าประมาณ 31.5 °C ใช้แทนช่วงเครื่องจักรทำงานหนัก

### เซลล์ที่ 3 — ตรวจสอบข้อมูลเบื้องต้น

~~~python
print("Number of readings:", temperature.size)
print("Mean:", temperature.mean())
print("Minimum:", temperature.min())
print("Maximum:", temperature.max())
~~~

การตรวจสอบจำนวน ค่าเฉลี่ย ค่าต่ำสุด และค่าสูงสุดช่วยค้นหาความผิดปกติก่อนสร้างกราฟ

---

## 3. Histogram แรก

### เซลล์ที่ 4 — สร้าง Histogram

~~~python
fig, ax = plt.subplots(figsize=(8, 5))

ax.hist(
    temperature,
    bins=30,
    color="royalblue",
    edgecolor="white",
)

ax.set(
    title="Machine-room temperature distribution",
    xlabel="Temperature (°C)",
    ylabel="Number of readings",
)
ax.grid(axis="y", alpha=0.25)
plt.show()
~~~

Histogram แบ่งช่วงอุณหภูมิออกเป็นช่องที่เรียกว่า **bin** แล้วนับจำนวนข้อมูลในแต่ละช่อง

จากกราฟควรเห็นกลุ่มหลักใกล้ 26 °C และกลุ่มขนาดเล็กใกล้ 31.5 °C ซึ่งอาจหมายถึงอีกสถานะการทำงานหนึ่งของเครื่องจักร

---

## 4. จำนวน Bin ส่งผลอย่างไร

หาก bin น้อยเกินไป รายละเอียดสำคัญอาจหายไป หากมากเกินไป กราฟอาจดูเป็นคลื่นจาก noise

### เซลล์ที่ 5 — เปรียบเทียบจำนวน Bin

~~~python
fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)

for ax, bins in zip(axes, [10, 30, 80]):
    ax.hist(
        temperature,
        bins=bins,
        color="steelblue",
        edgecolor="white",
    )
    ax.set_title(f"{bins} bins")
    ax.set_xlabel("Temperature (°C)")

axes[0].set_ylabel("Number of readings")
fig.suptitle("Effect of bin count")
fig.tight_layout()
plt.show()
~~~

- 10 bins อ่านง่าย แต่อาจซ่อนกลุ่มข้อมูลขนาดเล็ก
- 30 bins แสดงโครงสร้างได้สมดุล
- 80 bins ให้รายละเอียดมาก แต่อาจทำให้ตีความ noise เป็นรูปแบบจริง

<br>

สามารถให้ NumPy ช่วยเลือก bin ได้ด้วย:

~~~python
auto_edges = np.histogram_bin_edges(temperature, bins="auto")
fd_edges = np.histogram_bin_edges(temperature, bins="fd")

print("Auto bins:", len(auto_edges) - 1)
print("Freedman-Diaconis bins:", len(fd_edges) - 1)
~~~

คำว่า `"fd"` หมายถึงกฎ Freedman–Diaconis ซึ่งพิจารณาทั้งจำนวนข้อมูลและการกระจายของข้อมูล

---

## 5. Count กับ Density ต่างกันอย่างไร

### Count

Count คือจำนวนข้อมูลที่อยู่ภายใน Bin ตัวอย่างเช่น หากช่วง 24–26 °C มีข้อมูล 843 ค่า ความสูงของแท่งแบบ Count จะเท่ากับ 843

Count ตอบคำถามว่า:

> “มีข้อมูลอยู่ในช่วงนี้กี่ค่า?”

ข้อจำกัดคือ ถ้าชุด A มี 2,000 ค่าและชุด B มี 500 ค่า แท่งของชุด A มักสูงกว่าเพียงเพราะมีตัวอย่างมากกว่า ไม่ได้แปลว่ารูปร่างการกระจายต่างกันเสมอ

### Density คืออะไร

Density หรือความหนาแน่น บอกว่า “ข้อมูลหนาแน่นเพียงใดต่อหนึ่งหน่วยบนแกน X” โดยพิจารณาทั้งจำนวนข้อมูลทั้งหมดและความกว้างของ Bin

สำหรับ Histogram แบบ Density:

~~~text
Density = Count ÷ (จำนวนข้อมูลทั้งหมด × ความกว้าง Bin)
~~~

และ:

~~~text
Probability ใน Bin = Density × ความกว้าง Bin
~~~

ดังนั้น Density ไม่ใช่ Count, ไม่ใช่เปอร์เซ็นต์ และความสูงของแท่งเพียงอย่างเดียวไม่ใช่ Probability

### `bins=30` หมายถึงอะไร

`bins=30` หมายถึงให้แบ่งช่วงตั้งแต่ค่าต่ำสุดถึงค่าสูงสุดของข้อมูลออกเป็น 30 Bin ไม่ได้หมายความว่า Bin มีความกว้าง 30 หน่วย

เมื่อไม่ได้กำหนด `range` หรือขอบ Bin เอง และทุก Bin กว้างเท่ากัน:

~~~text
ความกว้าง Bin ≈ (ค่าสูงสุด − ค่าต่ำสุด) ÷ จำนวน Bin
~~~

สำหรับข้อมูลอุณหภูมิตัวอย่าง:

~~~text
ค่าต่ำสุด ≈ 21.99 °C
ค่าสูงสุด ≈ 33.27 °C
จำนวน Bin = 30

ความกว้าง Bin ≈ (33.27 − 21.99) ÷ 30
                 ≈ 0.376 °C
~~~

NumPy สร้างขอบทั้งหมด 31 ค่าเพื่อประกอบเป็น 30 ช่วง

### ตัวอย่างแทนค่า Density จาก Bin จริง

โค้ดต่อไปเลือก Bin ที่มี Count สูงที่สุด:

~~~python
example_counts, example_edges = np.histogram(
    temperature,
    bins=30,
)

peak_bin_index = np.argmax(example_counts)

example_count = example_counts[peak_bin_index]
example_left = example_edges[peak_bin_index]
example_right = example_edges[peak_bin_index + 1]
example_width = example_right - example_left

example_density = example_count / (
    temperature.size * example_width
)
example_probability = example_density * example_width

print(
    f"Bin range: {example_left:.3f} "
    f"to {example_right:.3f} °C"
)
print(f"Count: {example_count}")
print(f"Bin width: {example_width:.3f} °C")
print(f"Density: {example_density:.3f} per °C")
print(
    f"Probability: "
    f"{example_probability:.3f} "
    f"({example_probability * 100:.1f}%)"
)
~~~

จากข้อมูลที่ใช้ seed 42 จะได้ค่าประมาณ:

~~~text
Bin range: 26.124 to 26.501 °C
Count: 268
Bin width: 0.376 °C
Density: 0.356 per °C
Probability: 0.134 หรือ 13.4%
~~~

แทนค่าในสูตร:

~~~text
Density = 268 ÷ (2,000 × 0.376)
        ≈ 0.356 ต่อ °C

Probability = 0.356 × 0.376
            ≈ 0.134
            ≈ 13.4%
~~~

หากกำหนดขอบ Bin เอง เช่น `bins=[20, 22, 25, 30, 36]` แต่ละ Bin อาจกว้างไม่เท่ากัน จึงต้องคำนวณความกว้างจากขอบขวาลบขอบซ้ายของแต่ละ Bin

ตัวอย่าง หาก Density ของช่วงกว้าง 2 °C เท่ากับ 0.15 ต่อ °C:

~~~text
Probability ของช่วงนั้น = 0.15 × 2 = 0.30 หรือ 30%
~~~

### Probability Density

เมื่อใช้ `density=True` Matplotlib จะปรับความสูงของแท่งให้ **พื้นที่รวมของทุกแท่งเท่ากับ 1**

เหตุผลที่ใช้ Density:

- เปรียบเทียบรูปร่างของชุดข้อมูลที่มีจำนวนตัวอย่างไม่เท่ากัน
- เปรียบเทียบ Histogram ที่ใช้ความกว้าง Bin ต่างกันอย่างระมัดระวัง
- วางเส้น Probability Density หรือ KDE บน Histogram
- สนใจสัดส่วนการกระจายมากกว่าจำนวนข้อมูลดิบ

### เซลล์ที่ 6 — Probability Density Histogram

~~~python
fig, ax = plt.subplots(figsize=(8, 5))

ax.hist(
    temperature,
    bins=30,
    density=True,
    histtype="stepfilled",
    color="steelblue",
    alpha=0.65,
    edgecolor="none",
)

ax.set(
    title="Temperature probability density",
    xlabel="Temperature (°C)",
    ylabel="Probability density (1/°C)",
)
plt.show()
~~~

เมื่อแกน X มีหน่วย °C แกน Density จะมีหน่วย 1/°C เพราะพื้นที่เกิดจาก:

~~~text
(1/°C) × °C = ไม่มีหน่วย
~~~

### ตรวจสอบพื้นที่รวมด้วย NumPy

~~~python
density_values, density_edges = np.histogram(
    temperature,
    bins=30,
    density=True,
)

bin_widths = np.diff(density_edges)
bin_probabilities = density_values * bin_widths
total_area = np.sum(bin_probabilities)

print("Probability in each bin:", bin_probabilities)
print(f"Total histogram area: {total_area:.3f}")
~~~

ผลรวมควรใกล้เคียง 1.000

ข้อควรจำ:

- เปลี่ยนความกว้าง Bin แล้วความสูงของ Density เปลี่ยนได้
- Probability ของช่วงต้องดูพื้นที่ ไม่ใช่ดูความสูงอย่างเดียว
- Density สูงหมายถึงข้อมูลกระจุกตัวแน่นในบริเวณนั้น
- Density ไม่ได้บอกลำดับเวลาและไม่ใช่ค่าความหนาแน่นทางกายภาพของวัตถุ

> ตัวอย่างสมัยเก่าบางแห่งใช้ `normed=True` แต่ Matplotlib รุ่นปัจจุบันควรใช้ `density=True`
---

## 6. เปรียบเทียบสถานะการสั่นสะเทือน

สมมติว่าเรามีข้อมูล RMS vibration จากมอเตอร์ในสถานะปกติและสถานะเตือน

**RMS ย่อมาจาก Root Mean Square** เป็นวิธีสรุปขนาดโดยรวมของสัญญาณที่แกว่งขึ้นและลง เช่น ความเร็วการสั่นสะเทือน ค่า RMS สูงขึ้นหมายถึงระดับการสั่นโดยรวมสูงขึ้น แต่ RMS เพียงค่าเดียวไม่สามารถระบุได้ว่าความเสียหายเกิดจาก Bearing, Alignment หรือ Unbalance

### เซลล์ที่ 7 — สร้างข้อมูลสองสถานะและ Shared Bin Edges

~~~python
normal_vibration = rng.normal(
    loc=1.8,
    scale=0.35,
    size=1200,
)
warning_vibration = rng.normal(
    loc=3.4,
    scale=0.55,
    size=700,
)

all_vibration = np.concatenate([
    normal_vibration,
    warning_vibration,
])

shared_edges = np.histogram_bin_edges(
    all_vibration,
    bins=35,
)
~~~

หน่วยตัวอย่างคือ mm/s RMS โดยค่าจริงและ threshold ต้องอ้างอิงชนิดเครื่องจักร ตำแหน่งติดตั้ง และมาตรฐานที่องค์กรใช้งาน

การสร้าง `shared_edges` จากข้อมูลทั้งสองชุดทำให้แท่งของ Normal และ Warning ใช้ช่วง X เดียวกัน หากส่งเพียง `bins=35` แยกให้แต่ละคำสั่ง Matplotlib จะคำนวณขอบจากช่วงข้อมูลคนละชุด ทำให้ตำแหน่งแท่งไม่ตรงกัน

### เซลล์ที่ 8 — วาง Histogram ซ้อนกัน

~~~python
fig, ax = plt.subplots(figsize=(8, 5))

histogram_style = {
    "bins": shared_edges,
    "density": True,
    "histtype": "stepfilled",
    "alpha": 0.45,
}

ax.hist(
    normal_vibration,
    label="Normal operation",
    color="royalblue",
    **histogram_style,
)
ax.hist(
    warning_vibration,
    label="Warning operation",
    color="tomato",
    **histogram_style,
)

ax.set(
    title="Motor vibration by operating state",
    xlabel="Vibration RMS (mm/s)",
    ylabel="Probability density (1/(mm/s))",
)
ax.legend()
plt.show()
~~~

การใช้ Shared Bin Edges ทำให้ช่วงของแท่งตรงกัน ส่วน `density=True` ทำให้เปรียบเทียบรูปร่างได้แม้สองชุดมีจำนวนตัวอย่างต่างกัน

**Threshold** คือค่าขอบเขตที่ใช้แบ่งสถานะ เช่น ต่ำกว่า 2.5 mm/s เป็น Normal และสูงกว่านั้นเป็น Warning ตัวเลขนี้เป็นเพียงตัวอย่างและต้องอ้างอิงมาตรฐานของระบบจริง

หากสองกลุ่มซ้อนทับกัน Threshold ค่าเดียวอาจทำให้เกิด:

- **False alarm** — ระบบแจ้งเตือนทั้งที่เครื่องจักรยังปกติ
- **Missed detection** — เครื่องจักรผิดปกติแต่ระบบไม่แจ้งเตือน

ดังนั้น Threshold ควรพิจารณาร่วมกับ Operating State, Time-series และข้อมูลบำรุงรักษา
---

## 7. คำนวณ Histogram โดยไม่วาดกราฟ

เส้นทางข้อมูล IoT ตัวอย่างคือ:

~~~text
Sensor → Edge Gateway → Cloud/Database → Dashboard
~~~

- **Sensor** วัดค่าจากเครื่องจักร
- **Edge Gateway** รับ กรอง และสรุปข้อมูลใกล้หน้างาน
- **Cloud/Database** เก็บและวิเคราะห์ข้อมูลระยะยาว
- **Dashboard** แสดงผลให้ผู้ใช้งานตัดสินใจ

Gateway และ Cloud ต้องตกลงใช้ขอบ Bin ชุดเดียวกัน มิฉะนั้น Counts จากคนละอุปกรณ์หรือคนละช่วงเวลาจะนำมาเปรียบเทียบและรวมกันไม่ได้

### เซลล์ที่ 9 — ใช้ Fixed Bin Edges

~~~python
temperature_bin_edges = np.arange(
    20.0,
    36.1,
    2.0,
)

counts, bin_edges = np.histogram(
    temperature,
    bins=temperature_bin_edges,
)

print("Counts:", counts)
print("Bin edges:", bin_edges)
~~~

- `counts` คือจำนวนข้อมูลในแต่ละ Bin
- `bin_edges` คือขอบที่ตกลงใช้ร่วมกัน
- จำนวนขอบมากกว่าจำนวน Count หนึ่งค่า
- ตัวอย่างนี้ใช้ช่วงคงที่ 20–36 °C และความกว้าง Bin 2 °C

### อ่านจำนวนข้อมูลในแต่ละช่วง

~~~python
for left, right, count in zip(
    bin_edges[:-1],
    bin_edges[1:],
    counts,
):
    print(
        f"{left:4.1f} to {right:4.1f} °C: "
        f"{count:4d} readings"
    )
~~~

### Metadata ที่ควรส่งพร้อม Counts

~~~python
histogram_summary = {
    "device_id": "room-temp-gateway-01",
    "window_start": "2026-07-19T10:00:00Z",
    "window_end": "2026-07-19T11:00:00Z",
    "unit": "°C",
    "sampling_rate_hz": 1,
    "bin_config_version": "temperature-v1",
    "bin_edges": bin_edges.tolist(),
    "counts": counts.tolist(),
}

print(histogram_summary)
~~~

ข้อมูลสำคัญประกอบด้วย:

- **Device ID** ระบุแหล่งที่มาของข้อมูล
- **Window start/end** ระบุช่วงเวลาที่นำมาสรุป
- **Unit** ป้องกันการนำหน่วยต่างกันมาเปรียบเทียบ
- **Sampling Rate** ระบุจำนวนครั้งที่วัดต่อวินาที เช่น 1 Hz คือหนึ่งครั้งต่อวินาที
- **Bin configuration version** ระบุชุดขอบ Bin ที่ระบบตกลงใช้
- **Bin edges และ Counts** ระบุช่วงและจำนวนข้อมูล

หาก Sampling Rate หรือความยาว Time Window ต่างกัน Count จะต่างกันแม้พฤติกรรมเครื่องจักรเหมือนกัน จึงควรเปรียบเทียบ Density, Rate หรือช่วงเวลาที่เท่ากัน

การส่ง Histogram Summary ลดปริมาณข้อมูลได้ แต่จะสูญเสียลำดับเวลา ค่าเฉพาะจุด และรายละเอียดที่ละเอียดกว่าความกว้าง Bin จึงควรเก็บข้อมูลดิบหรือสถิติสำคัญเพิ่มเติมตามข้อกำหนดของระบบ
---

## 8. Histogram สองมิติสำหรับข้อมูลเซนเซอร์สองตัวแปร

เราจะจำลองความสัมพันธ์ระหว่างกระแสไฟของมอเตอร์กับอุณหภูมิ

### เซลล์ที่ 10 — สร้างข้อมูลที่สัมพันธ์กัน

~~~python
sample_count = 6000

motor_current = rng.normal(loc=12.0, scale=2.2, size=sample_count)
motor_temperature = (
    24.0
    + 0.75 * motor_current
    + rng.normal(0, 1.5, sample_count)
)
~~~

เมื่อกระแสไฟสูงขึ้น มอเตอร์มีแนวโน้มร้อนขึ้น แต่ noise ทำให้ความสัมพันธ์ไม่เป็นเส้นตรงสมบูรณ์

### เซลล์ที่ 11 — สร้าง 2D Histogram

~~~python
fig, ax = plt.subplots(figsize=(8, 6))

counts_2d, x_edges, y_edges, image = ax.hist2d(
    motor_current,
    motor_temperature,
    bins=35,
    cmap="YlOrRd",
    cmin=1,
)

fig.colorbar(
    image,
    ax=ax,
    label="Readings per bin",
)
ax.set(
    title="Motor current vs. temperature",
    xlabel="Motor current (A)",
    ylabel="Motor temperature (°C)",
)
plt.show()
~~~

`hist2d()` คืนค่าสี่รายการ:

- `counts_2d` คือจำนวนข้อมูลในแต่ละช่อง
- `x_edges` คือขอบ Bin ของกระแสไฟ
- `y_edges` คือขอบ Bin ของอุณหภูมิ
- `image` คือวัตถุกราฟที่ส่งให้ Colorbar

การแยกชื่อทั้งสี่ค่าทำให้โค้ดอ่านง่ายกว่าใช้ `histogram[3]`
พื้นที่ถูกแบ่งเป็นช่องสี่เหลี่ยมสองมิติ สีเข้มแสดงบริเวณที่มีข้อมูลจำนวนมาก ส่วน `cmin=1` ซ่อนช่องที่ไม่มีข้อมูล

**Operating Region** คือบริเวณบนกราฟที่ข้อมูลปรากฏหนาแน่นและเครื่องจักรมักทำงานอยู่ เช่น กระแส 10–14 A กับอุณหภูมิ 31–36 °C

หากกลุ่มข้อมูลค่อย ๆ เคลื่อนออกจาก Operating Region เดิม อาจเกิดจาก Load เปลี่ยน ระบบระบายความร้อนผิดปกติ Sensor drift หรือสภาพเครื่องจักรเปลี่ยน แต่กราฟเพียงอย่างเดียวยังไม่เพียงพอสำหรับสรุปสาเหตุ

---

## 9. Hexagonal Binning

เมื่อต้องแสดงข้อมูลสองมิติจำนวนมาก `hexbin()` ช่วยลดการซ้อนทับของจุดและให้รูปทรงที่ดูต่อเนื่องกว่าช่องสี่เหลี่ยม

### เซลล์ที่ 12 — สร้าง Hexbin Plot

~~~python
fig, ax = plt.subplots(figsize=(8, 6))

hexagons = ax.hexbin(
    motor_current,
    motor_temperature,
    gridsize=35,
    cmap="viridis",
    mincnt=1,
)

fig.colorbar(
    hexagons,
    ax=ax,
    label="Readings per hexagon",
)
ax.set(
    title="Motor operating density",
    xlabel="Motor current (A)",
    ylabel="Motor temperature (°C)",
)
plt.show()
~~~

- `gridsize` ควบคุมความละเอียดของตารางหกเหลี่ยม
- `mincnt=1` ซ่อนช่องว่าง
- Hexbin เหมาะกับข้อมูล Telemetry จำนวนมากที่ Scatter Plot เริ่มอ่านยาก

**Telemetry** คือข้อมูลที่อุปกรณ์ส่งกลับมาอย่างต่อเนื่อง เช่น อุณหภูมิ กระแสไฟ ความเร็วรอบ แรงสั่นสะเทือน และสถานะเครื่องจักร

---

## 10. Kernel Density Estimation

**KDE ย่อมาจาก Kernel Density Estimation** เป็นวิธีประมาณเส้น Probability Density แบบต่อเนื่องจากข้อมูลตัวอย่าง โดยไม่ต้องแสดงผลเป็นแท่งเหมือน Histogram

### ทำ KDE ไปทำไม

- ช่วยมองเห็นรูปร่างการกระจายโดยรวม
- ช่วยสังเกตข้อมูลที่มีหลายยอด เช่น Normal operation กับ Overheat
- ลดการพึ่งพาตำแหน่งขอบ Bin ของ Histogram
- ใช้เปรียบเทียบรูปทรงของข้อมูลหลายชุดได้

KDE ไม่ได้ใช้ทำนายค่าถัดไป ไม่ได้สร้างข้อมูลวัดใหม่ และไม่ได้พิสูจน์ว่ากลุ่มที่เห็นคือความผิดปกติจริง

### Kernel คืออะไร

Kernel คือเส้นโค้งขนาดเล็กที่วางไว้รอบข้อมูลแต่ละจุด `gaussian_kde()` ใช้ Gaussian Kernel ซึ่งมีรูปร่างคล้ายระฆังคว่ำ

แนวคิดการทำงาน:

~~~text
ข้อมูลหนึ่งจุด → วาง Gaussian Kernel หนึ่งลูก
ข้อมูลทุกจุด → วาง Kernel ครบทุกจุด
รวมความสูงของ Kernel → ได้เส้น KDE
~~~

บริเวณที่มีข้อมูลอยู่ใกล้กันมาก Kernel จะซ้อนกันสูง จึงได้ Density สูง บริเวณที่มีข้อมูลน้อยเส้นจะต่ำลง

### KDE กับ Histogram ต่างกันอย่างไร

| Histogram | KDE |
|-----------|-----|
| แสดงผลเป็นแท่ง | แสดงผลเป็นเส้นต่อเนื่อง |
| รูปร่างขึ้นกับ Bin edges และจำนวน Bin | รูปร่างขึ้นกับ Kernel และ Bandwidth |
| อ่าน Count ได้โดยตรงเมื่อไม่ใช้ Density | ไม่ได้แสดง Count โดยตรง |
| เห็นช่วงข้อมูลเป็นช่อง | เห็นภาพรวมที่เรียบกว่า |

### เซลล์ที่ 13 — Import SciPy และคำนวณ KDE

~~~python
from scipy.stats import gaussian_kde

temperature_grid = np.linspace(
    temperature.min() - 1,
    temperature.max() + 1,
    400,
)

temperature_kde = gaussian_kde(temperature)
density_curve = temperature_kde(temperature_grid)
~~~

### เซลล์ที่ 14 — วาง KDE บน Histogram

~~~python
fig, ax = plt.subplots(figsize=(8, 5))

ax.hist(
    temperature,
    bins=30,
    density=True,
    color="steelblue",
    alpha=0.35,
    label="Histogram",
)
ax.plot(
    temperature_grid,
    density_curve,
    color="darkorange",
    linewidth=2.5,
    label="Default KDE",
)

ax.set(
    title="Temperature histogram with KDE",
    xlabel="Temperature (°C)",
    ylabel="Probability density (1/°C)",
)
ax.legend()
plt.show()
~~~

### Bandwidth คืออะไร

Bandwidth ควบคุมว่าการกระจายรอบข้อมูลแต่ละจุดกว้างเพียงใด:

- Bandwidth แคบทำให้เห็นรายละเอียดมาก แต่ตอบสนองต่อ Noise ง่าย
- Bandwidth กว้างทำให้เส้นเรียบ แต่อาจซ่อนกลุ่ม Overheat ขนาดเล็ก
- ค่าเริ่มต้นของ `gaussian_kde()` ใช้กฎเชิงสถิติเลือกค่าให้โดยอัตโนมัติ

### เซลล์ที่ 15 — เปรียบเทียบ KDE Bandwidth

~~~python
kde_narrow = gaussian_kde(
    temperature,
    bw_method=0.12,
)
kde_default = gaussian_kde(temperature)
kde_wide = gaussian_kde(
    temperature,
    bw_method=0.50,
)

fig, ax = plt.subplots(figsize=(9, 5))

ax.hist(
    temperature,
    bins=30,
    density=True,
    color="lightgray",
    alpha=0.45,
    label="Histogram",
)

ax.plot(
    temperature_grid,
    kde_narrow(temperature_grid),
    linewidth=2,
    label="Narrow bandwidth (0.12)",
)
ax.plot(
    temperature_grid,
    kde_default(temperature_grid),
    linewidth=2.5,
    label="Default bandwidth",
)
ax.plot(
    temperature_grid,
    kde_wide(temperature_grid),
    linewidth=2,
    label="Wide bandwidth (0.50)",
)

ax.set(
    title="Effect of KDE bandwidth",
    xlabel="Temperature (°C)",
    ylabel="Probability density (1/°C)",
)
ax.legend()
plt.show()
~~~

ค่า 0.12 และ 0.50 ใช้เพื่อสาธิตผลของความเรียบ ไม่ใช่ค่ามาตรฐานสำหรับเซนเซอร์ทุกชนิด การเลือก Bandwidth ควรพิจารณาจำนวนข้อมูล Noise และความผิดปกติขนาดเล็กที่ต้องการตรวจจับ

KDE ไม่ได้สร้างข้อมูลใหม่ และเส้นที่เรียบไม่ได้แปลว่าเซนเซอร์มีความแม่นยำสูงขึ้น
---

## 11. Percentile และสถิติสรุปสำหรับ Predictive Maintenance

Histogram ช่วยให้เห็นรูปทรง ส่วนสถิติสรุปช่วยให้ได้ตัวเลขสำหรับรายงานและตั้งเกณฑ์เบื้องต้น

### Percentile คืออะไร

Percentile บอกว่ามีข้อมูลกี่เปอร์เซ็นต์ที่น้อยกว่าหรือเท่ากับค่านั้น ตัวอย่างเช่น Percentile ที่ 95 หรือ P95 เท่ากับ 2.4 mm/s หมายความว่า 95% ของข้อมูลมีค่าไม่เกิน 2.4 mm/s

P95 ไม่ได้หมายถึง Accuracy 95% และไม่ใช่ Probability ที่เครื่องจักรจะเสีย

### เซลล์ที่ 16 — คำนวณสถิติสรุป

~~~python
mean_vibration = np.mean(normal_vibration)
std_vibration = np.std(normal_vibration)
p95_vibration = np.percentile(
    normal_vibration,
    95,
)

example_threshold = 2.5
values_above_threshold = np.count_nonzero(
    normal_vibration > example_threshold
)

print(f"Mean: {mean_vibration:.2f} mm/s")
print(f"Standard deviation: {std_vibration:.2f} mm/s")
print(f"P95: {p95_vibration:.2f} mm/s")
print(
    "Values above threshold:",
    values_above_threshold,
)
~~~

- **Mean** คือค่าเฉลี่ย
- **Standard deviation** บอกระดับการกระจายรอบค่าเฉลี่ย
- **P95** ช่วยบอกขอบบนของข้อมูลส่วนใหญ่
- **Values above threshold** นับเหตุการณ์ที่เกินเกณฑ์ตัวอย่าง

Threshold ไม่ควรสร้างจาก P95 เพียงอย่างเดียว ควรอ้างอิงมาตรฐานของเครื่องจักร Baseline ตาม Operating State และผลกระทบของ False Alarm กับ Missed Detection

### Predictive Maintenance คืออะไร

Predictive Maintenance คือการใช้ข้อมูลสภาพเครื่องจักร เช่น Vibration, Temperature และ Motor Current เพื่อประเมินแนวโน้มและวางแผนตรวจสอบก่อนเกิดความเสียหาย

Histogram และ Percentile ช่วยสรุปพฤติกรรม แต่ควรใช้ร่วมกับ:

- Time-series และแนวโน้มตามเวลา
- Spectrum หรือ Frequency Analysis สำหรับ Vibration
- Alarm history
- Maintenance records
- Operating State และ Load ของเครื่องจักร

---
## 12. เลือกใช้กราฟแบบไหนดี

| กราฟ | เหมาะกับ | สิ่งที่ควรระวัง |
|------|-----------|-----------------|
| Histogram | ดูการกระจายของตัวแปรเดียว | จำนวน bin มีผลต่อรูปทรง |
| Overlaid Histogram | เปรียบเทียบหลายสถานะ | สีและความโปร่งใสต้องอ่านง่าย |
| 2D Histogram | ดูความสัมพันธ์ของสองตัวแปร | ช่องสี่เหลี่ยมอาจดูหยาบ |
| Hexbin | ข้อมูลสองมิติจำนวนมาก | gridsize มีผลต่อรายละเอียด |
| KDE | ต้องการเส้นความหนาแน่นที่เรียบ | bandwidth อาจซ่อนความผิดปกติ |

## 13. แนวทางสำหรับข้อมูล IoT จริง

- ตรวจสอบหน่วยและ calibration ก่อนรวมข้อมูล
- แยกข้อมูลตามสถานะการทำงานของเครื่องจักร
- ระวัง missing data และช่วงเวลาที่ Gateway offline
- อย่าปะปน sampling rate ที่ต่างกันโดยไม่ปรับข้อมูล
- กำหนดช่วง bin คงที่เมื่อเปรียบเทียบหลายวันหรือหลายอุปกรณ์
- เก็บ timestamp ไว้เสมอ เพราะ histogram ทำให้ลำดับเวลาหายไป
- ใช้ histogram ร่วมกับ time-series plot และ alarm log
- อย่าสรุปสาเหตุของความผิดปกติจากกราฟเพียงชนิดเดียว

## แบบฝึกหัด

1. เปลี่ยนจำนวน bin ของอุณหภูมิเป็น 15, 40 และ 100
2. เพิ่มข้อมูลช่วง overheat ที่ 35 °C แล้วตรวจสอบว่ากราฟมองเห็นหรือไม่
3. สร้าง histogram เปรียบเทียบ vibration ของมอเตอร์สามตัว
4. กำหนด bin edges คงที่เพื่อเปรียบเทียบข้อมูลสองวัน
5. เปลี่ยน 2D histogram เป็นความสัมพันธ์ระหว่างความชื้นกับอุณหภูมิ
6. ทดลองเปลี่ยน `gridsize` ของ hexbin
7. ทดลอง bandwidth ของ `gaussian_kde` แล้วอธิบายผล

อ่านโจทย์ฉบับเต็มได้ที่ [แบบฝึกหัด EP5](./exercises/exercise01.md)

## โจทย์ท้าทายย่อย

สร้างรายงาน Predictive Maintenance จากข้อมูล vibration โดยประกอบด้วย:
- Histogram ของสถานะปกติและสถานะเตือน
- ค่าเฉลี่ย ส่วนเบี่ยงเบนมาตรฐาน และ percentile ที่ 95
- เส้น threshold ที่องค์กรกำหนด
- จำนวนข้อมูลที่เกิน threshold
- คำอธิบายข้อจำกัดของการใช้ histogram

## สคริปต์ฉบับเต็ม

- [temperature_histogram.py](./source-code/temperature_histogram.py)
- [compare_vibration.py](./source-code/compare_vibration.py)
- [iot_hist2d_hexbin.py](./source-code/iot_hist2d_hexbin.py)
- [kde_sensor_density.py](./source-code/kde_sensor_density.py)

## ตอนถัดไป

**EP6 — Customizing Plot Legends**
