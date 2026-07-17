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
- อธิบายความหมายของ histogram และ bin
- เลือกจำนวน bin ให้เหมาะกับข้อมูล
- แยกความแตกต่างระหว่าง count และ probability density
- เปรียบเทียบการกระจายของข้อมูลหลายชุด
- คำนวณ histogram โดยไม่ต้องสร้างกราฟ
- สร้าง histogram สองมิติและ hexagonal binning
- ใช้ KDE เพื่อประมาณเส้นความหนาแน่นแบบต่อเนื่อง
- ประยุกต์กราฟกับงาน IoT, IIoT และ Predictive Maintenance

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

Histogram แบบ count แสดงจำนวนค่าภายในแต่ละ bin ส่วน `density=True` ปรับสเกลให้พื้นที่รวมใต้ histogram เท่ากับ 1

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
    ylabel="Probability density",
)
plt.show()
~~~

Density ไม่ใช่จำนวนอุปกรณ์และไม่ใช่เปอร์เซ็นต์ของ bin โดยตรง เหมาะเมื่อต้องเปรียบเทียบข้อมูลที่มีจำนวนตัวอย่างไม่เท่ากัน

> ตัวอย่างสมัยเก่าบางแห่งใช้ `normed=True` แต่ Matplotlib รุ่นปัจจุบันควรใช้ `density=True`

---

## 6. เปรียบเทียบสถานะการสั่นสะเทือน

สมมติว่าเรามีข้อมูล RMS vibration จากมอเตอร์ในสถานะปกติและสถานะเตือน

### เซลล์ที่ 7 — สร้างข้อมูลสองสถานะ

~~~python
normal_vibration = rng.normal(loc=1.8, scale=0.35, size=1200)
warning_vibration = rng.normal(loc=3.4, scale=0.55, size=700)
~~~

หน่วยตัวอย่างคือ mm/s RMS โดยค่าจริงและ threshold ต้องอ้างอิงชนิดเครื่องจักร ตำแหน่งติดตั้ง และมาตรฐานที่องค์กรใช้งาน

### เซลล์ที่ 8 — วาง Histogram ซ้อนกัน

~~~python
fig, ax = plt.subplots(figsize=(8, 5))

histogram_style = {
    "bins": 35,
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
    ylabel="Probability density",
)
ax.legend()
plt.show()
~~~

การใช้ `density=True` ทำให้เปรียบเทียบรูปร่างของข้อมูลได้ แม้สองชุดมีจำนวนตัวอย่างต่างกัน

หากสองกลุ่มซ้อนทับกันมาก การตั้ง threshold เพียงค่าเดียวอาจทำให้เกิด false alarm หรือพลาดเหตุการณ์ผิดปกติได้

---

## 7. คำนวณ Histogram โดยไม่วาดกราฟ

บางระบบต้องการส่งเพียงค่าที่สรุปแล้วจาก Edge Gateway ไปยัง Cloud เพื่อลดปริมาณข้อมูล

### เซลล์ที่ 9 — ใช้ `np.histogram()`

~~~python
counts, bin_edges = np.histogram(temperature, bins=8)

print("Counts:", counts)
print("Bin edges:", np.round(bin_edges, 2))
~~~

- `counts` คือจำนวนข้อมูลในแต่ละ bin
- `bin_edges` คือขอบของ bin
- จำนวนขอบจะมากกว่าจำนวน count อยู่หนึ่งค่า

ตัวอย่างการอ่านช่วง:

~~~python
for left, right, count in zip(bin_edges[:-1], bin_edges[1:], counts):
    print(f"{left:5.1f} to {right:5.1f} °C: {count:4d} readings")
~~~

ผลลัพธ์สามารถนำไปเก็บในฐานข้อมูล ส่งผ่าน MQTT หรือใช้สร้าง Dashboard ได้โดยไม่ต้องส่งข้อมูลดิบทุกค่า แต่จะสูญเสียรายละเอียดตามเวลาไป

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

histogram = ax.hist2d(
    motor_current,
    motor_temperature,
    bins=35,
    cmap="YlOrRd",
    cmin=1,
)

fig.colorbar(
    histogram[3],
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

พื้นที่ถูกแบ่งเป็นช่องสี่เหลี่ยมสองมิติ สีเข้มแสดงบริเวณที่มีข้อมูลจำนวนมาก ส่วน `cmin=1` ซ่อนช่องที่ไม่มีข้อมูล

กราฟนี้ช่วยค้นหา operating region และบริเวณที่กระแสไฟกับอุณหภูมิสูงพร้อมกัน

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
- Hexbin เหมาะกับข้อมูล telemetry จำนวนมากที่ scatter plot เริ่มอ่านยาก

---

## 10. Kernel Density Estimation

KDE ประมาณเส้นความหนาแน่นแบบต่อเนื่องโดยวาง kernel รอบข้อมูลแต่ละจุดแล้วรวมผลเข้าด้วยกัน

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
    label="KDE",
)

ax.set(
    title="Temperature histogram with KDE",
    xlabel="Temperature (°C)",
    ylabel="Probability density",
)
ax.legend()
plt.show()
~~~

KDE ช่วยให้เห็นรูปทรงโดยรวมและกลุ่มข้อมูลหลายยอดได้ชัด แต่ความเรียบขึ้นกับ bandwidth:

- bandwidth ต่ำเกินไปทำให้เส้นตอบสนองต่อ noise มาก
- bandwidth สูงเกินไปอาจทำให้กลุ่มผิดปกติขนาดเล็กหายไป
- KDE ไม่ได้สร้างข้อมูลใหม่ แต่เป็นการประมาณจากตัวอย่างที่มีอยู่

---

## 11. เลือกใช้กราฟแบบไหนดี

| กราฟ | เหมาะกับ | สิ่งที่ควรระวัง |
|------|-----------|-----------------|
| Histogram | ดูการกระจายของตัวแปรเดียว | จำนวน bin มีผลต่อรูปทรง |
| Overlaid Histogram | เปรียบเทียบหลายสถานะ | สีและความโปร่งใสต้องอ่านง่าย |
| 2D Histogram | ดูความสัมพันธ์ของสองตัวแปร | ช่องสี่เหลี่ยมอาจดูหยาบ |
| Hexbin | ข้อมูลสองมิติจำนวนมาก | gridsize มีผลต่อรายละเอียด |
| KDE | ต้องการเส้นความหนาแน่นที่เรียบ | bandwidth อาจซ่อนความผิดปกติ |

## 12. แนวทางสำหรับข้อมูล IoT จริง

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
