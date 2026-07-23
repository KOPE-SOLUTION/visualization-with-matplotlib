# EP7 — Customizing Colorbars for Smart Building IoT Data

Colorbar ทำหน้าที่แปลสีบนกราฟกลับมาเป็นค่าตัวเลข เช่น สีของแต่ละช่องใน Heatmap แทนค่า PM2.5 เท่าไร หรือพื้นที่สีแดงมีอุณหภูมิสูงกว่าค่าเป้าหมายกี่องศา หากไม่มี Colorbar ผู้อ่านกราฟอาจเห็นเพียงว่าสีต่างกัน แต่ไม่ทราบขนาดและหน่วยของข้อมูล

บทนี้ใช้ **ระบบติดตามคุณภาพอากาศภายใน Smart Building** เป็นกรณีศึกษา เราจะจำลองข้อมูลจาก Sensor หลายชั้นของอาคาร แล้วเรียนรู้การออกแบบ Colorbar ให้สื่อความหมายถูกต้องและเปรียบเทียบข้อมูลข้ามกราฟได้

ตัวอย่างและคำอธิบายทั้งหมดเรียบเรียงขึ้นใหม่สำหรับชุดวิดีโอนี้ ข้อมูลเป็นข้อมูลสังเคราะห์ และช่วงสถานะที่ใช้ในบทมีไว้สาธิตการเขียนโปรแกรมเท่านั้น ไม่ใช่เกณฑ์สุขภาพหรือมาตรฐานทางกฎหมาย

## วิธีเรียนจากบทนี้

- คัดลอกเซลล์ตามลำดับจากบนลงล่าง
- รันเซลล์เตรียมข้อมูลก่อนเซลล์ที่นำข้อมูลไปวาดกราฟ
- กราฟแต่ละรูปเริ่มด้วย `plt.subplots()` และจบด้วย `plt.show()` ในเซลล์เดียว
- ทดลองเปลี่ยน Colormap, `vmin`, `vmax`, Tick และตำแหน่ง Colorbar
- สคริปต์ฉบับเต็มอยู่ในโฟลเดอร์ [source-code](./source-code/)

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบบทนี้ คุณจะสามารถ:

- อธิบายความแตกต่างระหว่าง Colorbar, Colormap และ Legend
- อธิบายว่า Mappable เชื่อมข้อมูล Colormap และ Colorbar อย่างไร
- สร้าง Colorbar จาก `imshow()` และ `scatter()`
- เลือก Sequential, Diverging และ Discrete Colormap ให้เหมาะกับข้อมูล
- กำหนด Label, Tick, Orientation, ขนาด และระยะห่างของ Colorbar
- ล็อกช่วงสีด้วย `vmin` และ `vmax` เพื่อเปรียบเทียบหลายช่วงเวลา
- ใช้ `extend` แสดงว่ามีค่าที่อยู่นอกช่วง Colorbar
- กำหนดสีสำหรับค่า Over, Under และ Missing Data
- สร้าง Colorbar แบบแบ่งระดับด้วย `ListedColormap` และ `BoundaryNorm`
- กำหนดจุดกึ่งกลางของ Diverging Colorbar ด้วย `TwoSlopeNorm`
- ใช้ `LogNorm` กับข้อมูลที่มีหลายลำดับขนาด
- ระบุข้อจำกัดของการตีความสีในข้อมูล IoT จริง

## คำศัพท์สำคัญก่อนเริ่ม

| คำศัพท์ | ความหมาย |
|---------|----------|
| Colorbar | แถบอ้างอิงที่จับคู่สีกับค่าตัวเลขหรือช่วงค่า |
| Colormap | ชุดกฎที่แปลงค่าที่ Normalize แล้วให้เป็นสี |
| Mappable | Plot Object ที่เก็บข้อมูล Colormap และ Normalization เช่นผลลัพธ์จาก `imshow()` หรือ `scatter()` |
| Normalization | กระบวนการแปลงช่วงข้อมูลให้เข้าสู่ตำแหน่งบน Colormap |
| `vmin`, `vmax` | ค่าต่ำสุดและสูงสุดของช่วงสีที่ต้องการแสดง |
| Tick | ตำแหน่งตัวเลขหรือข้อความกำกับบน Colorbar |
| Sequential | Colormap ที่ความเข้มหรือความสว่างเปลี่ยนไปตามลำดับจากต่ำไปสูง |
| Diverging | Colormap ที่แยกสองทิศทางออกจากค่ากึ่งกลางที่มีความหมาย |
| Discrete | การแบ่งสีออกเป็นช่วงหรือกลุ่มที่มีขอบเขตชัดเจน |
| `extend` | สัญลักษณ์ปลาย Colorbar ที่บอกว่ามีค่านอกช่วงแสดงผล |
| Masked value | ค่าที่ตั้งใจไม่แสดง เช่นข้อมูลหายหรือ Sensor Offline |
| PM2.5 | ฝุ่นละอองขนาดเล็กที่มีเส้นผ่านศูนย์กลางไม่เกินประมาณ 2.5 ไมโครเมตร |
| µg/m³ | ไมโครกรัมต่อลูกบาศก์เมตร หน่วยความเข้มข้นเชิงมวลต่อปริมาตรอากาศ |
| Indoor Air Quality | คุณภาพอากาศภายในอาคาร ซึ่งอาจพิจารณาหลายตัวแปร ไม่ใช่ PM2.5 เพียงค่าเดียว |

---

## 1. Colorbar แตกต่างจาก Legend อย่างไร

Legend เหมาะกับข้อมูลแบบหมวดหมู่ เช่น:

- Sensor Online, Warning และ Offline
- Greenhouse A, Greenhouse B และ Outdoor Sensor
- เส้นข้อมูลจริง เส้นค่าเฉลี่ย และเส้น Threshold

Colorbar เหมาะกับค่าตัวเลขที่สีเปลี่ยนอย่างต่อเนื่องหรือแบ่งเป็นช่วง เช่น:

- PM2.5 ตั้งแต่ 0–50 µg/m³
- อุณหภูมิ 18–32 °C
- ความชื้นสัมพัทธ์ 30–90%
- ค่าเบี่ยงเบนจากอุณหภูมิเป้าหมาย

หากสร้าง Legend แยกสำหรับทุกค่าความเข้มข้น จะมีรายการจำนวนมากและเทียบค่าได้ยาก Colorbar จึงทำหน้าที่เป็น Scale กลางสำหรับอ่านค่าจากสี

| คำถาม | ใช้ Legend | ใช้ Colorbar |
|-------|:----------:|:------------:|
| สีเขียวกับสีส้มคือสถานะอะไร | ใช่ | ไม่จำเป็น |
| สีนี้แทนค่า PM2.5 เท่าไร | ไม่เหมาะ | ใช่ |
| เส้นประคือ Sensor ชุดใด | ใช่ | ไม่ใช่ |
| สีแดงสูงกว่าค่าเป้าหมายกี่องศา | ไม่เหมาะ | ใช่ |

---

## 2. เตรียมไลบรารีและข้อมูล PM2.5

### เซลล์ที่ 1 — Import

~~~python
import numpy as np
import matplotlib.pyplot as plt
~~~

ติดตั้งไลบรารีได้ด้วย:

~~~bash
python -m pip install numpy matplotlib
~~~

### เซลล์ที่ 2 — สร้างเวลาและชื่อชั้น

~~~python
rng = np.random.default_rng(42)

hours = np.arange(0, 24, 2)
floor_names = [
    "Floor 1",
    "Floor 2",
    "Floor 3",
    "Floor 4",
]
~~~

- วัดค่าทุก 2 ชั่วโมง จึงมีข้อมูล 12 ช่วงเวลาต่อชั้น
- `rng` ใช้ Seed คงที่เพื่อให้ผู้เรียนได้ผลลัพธ์เหมือนกัน
- ข้อมูลจริงควรอ่าน Timestamp, Device ID และ Floor ID จากฐานข้อมูลหรือ Message Payload

### เซลล์ที่ 3 — จำลอง PM2.5

~~~python
time_pattern = 8 + 7 * np.exp(
    -((hours - 9) / 3.2) ** 2
)

floor_offset = np.array(
    [5, 2, 0, -1]
)[:, np.newaxis]

noise = rng.normal(
    0,
    1.4,
    size=(4, hours.size),
)

pm25 = np.clip(
    time_pattern + floor_offset + noise,
    0,
    None,
)
~~~

Array `pm25` มี Shape เท่ากับ `(4, 12)`:

- 4 แถวแทน 4 ชั้นของอาคาร
- 12 คอลัมน์แทนช่วงเวลา
- `np.clip(..., 0, None)` ป้องกันค่าจำลองไม่ให้ติดลบ

### เซลล์ที่ 4 — ตรวจสอบข้อมูล

~~~python
print("Shape:", pm25.shape)
print("Minimum:", pm25.min())
print("Maximum:", pm25.max())
~~~

ควรตรวจค่าต่ำสุด ค่าสูงสุด Shape และหน่วยก่อนเลือกช่วงสี เพราะ Colorbar ที่ดูสวยแต่ใช้หน่วยผิดอาจทำให้ตัดสินใจผิดได้

---

## 3. สร้าง Heatmap และ Colorbar แรก

### เซลล์ที่ 5 — แสดงข้อมูลด้วย `imshow()`

~~~python
fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    pm25,
    cmap="viridis",
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
    vmin=0,
    vmax=30,
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    pad=0.02,
)
colorbar.set_label(
    "PM2.5 concentration (µg/m³)"
)

ax.set(
    title="Indoor PM2.5 by Floor and Time",
    xlabel="Hour",
    ylabel="Building floor",
    xticks=np.arange(0, 25, 4),
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
~~~

จุดที่ควรสังเกตคือเราเก็บผลลัพธ์ของ `ax.imshow()` ไว้ในตัวแปร `image` แล้วส่งตัวแปรนี้ให้ `fig.colorbar()`

### Mappable คืออะไร

`image` เป็น Mappable หรือ Plot Object ที่รู้ข้อมูลสำคัญสามส่วน:

1. ข้อมูลตัวเลขที่ต้องนำไปแสดง
2. วิธี Normalize ข้อมูล เช่นช่วง 0–30
3. Colormap ที่ใช้แปลงตำแหน่งบน Scale ให้เป็นสี

Colorbar อ่านข้อมูลเหล่านี้จาก Mappable จึงแสดงสีและช่วงค่าตรงกับ Heatmap

ลำดับการแปลงสีโดยย่อคือ:

~~~text
ค่าจริงจาก Sensor
→ Normalization แปลงตำแหน่งภายในช่วงสี
→ Colormap แปลงตำแหน่งนั้นเป็นสี RGBA
→ Plot แสดงสี
→ Colorbar แสดงกุญแจสำหรับอ่านสีกลับเป็นค่า
~~~

ตัวอย่าง เมื่อกำหนด `vmin=0` และ `vmax=30` ค่า 15 จะอยู่ประมาณกึ่งกลางของ Scale แล้ว `viridis` จะเลือกสีบริเวณกึ่งกลางมาแสดง ค่า 15 ในข้อมูลยังคงเป็น 15 ไม่ได้ถูกแก้เป็น 0.5 มีเพียงขั้นตอนแสดงผลที่ Normalize ตำแหน่งสี

`fig.colorbar()` สร้าง Colorbar พร้อม Axes ของตัวเองและคืนค่า Colorbar Object กลับมา ตัวแปร `colorbar` จึงใช้ปรับ Label และ Tick ได้ ส่วน `colorbar.ax` ใช้เข้าถึง Axes ภายในของ Colorbar เช่นตอนเปลี่ยนข้อความ Tick ของ Discrete Colorbar

ควรเขียน:

~~~python
image = ax.imshow(data, cmap="viridis")
fig.colorbar(image, ax=ax)
~~~

การส่ง `ax=ax` บอกว่า Colorbar นี้เป็นของ Axes ใด และช่วยให้ Matplotlib จัดพื้นที่ของกราฟอย่างชัดเจน

### ความหมายของ Parameter ใน `imshow()`

- `cmap="viridis"` เลือก Colormap
- `aspect="auto"` ปรับอัตราส่วนช่องให้พอดีกับพื้นที่ Axes
- `origin="lower"` วางแถวแรกไว้ด้านล่าง
- `extent` จับพิกัด Array ให้ตรงกับชั่วโมงและหมายเลขชั้น
- `vmin=0`, `vmax=30` กำหนดช่วงสีคงที่

ค่า `vmin` และ `vmax` เปลี่ยนการจับคู่สี แต่ไม่ได้แก้ไขตัวเลขใน Array `pm25`

---

## 4. ปรับ Label, Tick, ขนาด และตำแหน่ง

### เซลล์ที่ 6 — กำหนด Tick ของ Colorbar

ให้รันเซลล์ที่ 5 ใหม่ แล้วปรับส่วนสร้าง Colorbar เป็น:

~~~python
colorbar = fig.colorbar(
    image,
    ax=ax,
    ticks=[0, 5, 10, 15, 20, 25, 30],
    pad=0.02,
)

colorbar.set_label(
    "PM2.5 concentration (µg/m³)",
    rotation=90,
    labelpad=12,
)
~~~

- `ticks` กำหนดตำแหน่งตัวเลขที่ต้องการแสดง
- `rotation=90` หมุน Label ตามแนวตั้ง
- `labelpad` กำหนดระยะระหว่าง Label กับ Colorbar
- `pad` กำหนดระยะระหว่าง Axes หลักกับ Colorbar

อย่าใส่ Tick ถี่เกินไป เพราะตัวเลขอาจซ้อนกันและไม่ได้ช่วยให้ตีความแม่นยำขึ้น

### เซลล์ที่ 7 — Colorbar แนวนอน

~~~python
fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    pm25,
    cmap="viridis",
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
    vmin=0,
    vmax=30,
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    orientation="horizontal",
    location="bottom",
    shrink=0.8,
    aspect=35,
    pad=0.18,
)
colorbar.set_label("PM2.5 concentration (µg/m³)")

ax.set(
    title="Indoor PM2.5 by Floor and Time",
    xlabel="Hour",
    ylabel="Building floor",
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
~~~

- `orientation="horizontal"` เปลี่ยน Colorbar เป็นแนวนอน
- `location="bottom"` วางไว้ด้านล่าง
- `shrink=0.8` ลดความยาวเหลือประมาณ 80% ของพื้นที่อ้างอิง
- `aspect=35` ควบคุมสัดส่วนความยาวต่อความหนา

Colorbar แนวนอนเหมาะกับ Dashboard ที่มีพื้นที่ด้านข้างจำกัด แต่ต้องระวังไม่ให้ชนชื่อแกน X

---

## 5. เลือก Colormap ให้ตรงกับความหมาย

Colormap ไม่ได้มีหน้าที่ตกแต่งเพียงอย่างเดียว สีต้องสื่อโครงสร้างของข้อมูลโดยไม่สร้างขอบหรือจุดเด่นที่ไม่มีอยู่จริง

### Sequential Colormap

เหมาะกับข้อมูลที่เรียงจากน้อยไปมากและไม่มีจุดกึ่งกลางพิเศษ เช่น:

- PM2.5
- ความชื้นสัมพัทธ์
- จำนวน Packet
- พลังงานไฟฟ้าที่ใช้

ตัวอย่างที่ใช้บ่อย:

~~~python
cmap="viridis"
cmap="cividis"
cmap="magma"
cmap="Blues"
~~~

`viridis` และ `cividis` มีการเปลี่ยนความสว่างค่อนข้างเป็นลำดับ จึงเหมาะกับข้อมูลตัวเลขต่อเนื่องและรองรับการอ่านเมื่อพิมพ์แบบ Grayscale ได้ดีกว่า Colormap ที่สีเปลี่ยนฉับพลัน

### Diverging Colormap

เหมาะเมื่อข้อมูลมีค่ากึ่งกลางที่มีความหมาย และต้องการแยกค่าต่ำกับค่าสูงออกคนละทิศทาง เช่น:

- อุณหภูมิต่ำหรือสูงกว่าค่าเป้าหมาย 24 °C
- พลังงานที่ใช้ต่ำหรือสูงกว่า Baseline
- ค่าความคลาดเคลื่อนติดลบและบวก

ตัวอย่าง:

~~~python
cmap="RdBu_r"
cmap="coolwarm"
cmap="PuOr"
~~~

### Qualitative Colormap

เหมาะกับหมวดหมู่ที่ไม่มีลำดับ เช่นประเภทห้องหรือชนิด Sensor ไม่เหมาะกับค่าต่อเนื่อง เพราะความต่างของสีอาจทำให้ดูเหมือนข้อมูลแบ่งเป็นกลุ่มทั้งที่จริงเปลี่ยนต่อเนื่อง

### เหตุใดจึงควรระวัง `jet`

`jet` มีช่วงความสว่างที่เปลี่ยนไม่สม่ำเสมอและมีหลายสีตัดกันแรง สายตาจึงอาจเห็นขอบเขตที่เด่นกว่าความเปลี่ยนแปลงจริงของข้อมูล สำหรับค่าต่อเนื่องควรเริ่มจาก Colormap อย่าง `viridis` หรือ `cividis` แล้วตรวจสอบกับบริบทจริง

แนวทางเพิ่มเติม:

- อย่าใช้สีแดง–เขียวเพียงอย่างเดียวเพื่อแยกสถานะสำคัญ
- ตรวจกราฟในโหมด Grayscale เมื่อมีการพิมพ์เอกสาร
- ใช้ Scale และ Colormap เดียวกันเมื่อต้องเปรียบเทียบหลายกราฟ
- อย่าเปลี่ยนทิศทางสีระหว่างหน้า Dashboard โดยไม่มีเหตุผล

---

## 6. ล็อกช่วงสีและแสดงค่านอกช่วง

ถ้าไม่กำหนดช่วงสี Matplotlib จะใช้ค่าต่ำสุดและสูงสุดของข้อมูลแต่ละชุดโดยอัตโนมัติ วิธีนี้เหมาะกับการสำรวจข้อมูลชุดเดียว แต่ทำให้กราฟคนละวันใช้สีเดียวกันแทนค่าคนละค่าได้

ตัวอย่างเช่น:

- วันแรกสีเหลืองอาจแทน 20 µg/m³
- วันที่สองสีเหลืองอาจแทน 45 µg/m³

ถ้านำภาพมาวางเทียบกันโดยไม่อ่าน Colorbar อาจสรุปผิดว่าทั้งสองวันมีค่าใกล้กัน

### เซลล์ที่ 8 — เพิ่มเหตุการณ์ค่าฝุ่นสูง

~~~python
pm25_with_event = pm25.copy()

pm25_with_event[0, 5] = 72
pm25_with_event[1, 5] = 58
~~~

เราใช้ `.copy()` เพื่อไม่ให้แก้ข้อมูลเดิมโดยไม่ตั้งใจ

### เซลล์ที่ 9 — กำหนดสีสำหรับค่าเกินช่วง

~~~python
pm25_cmap = plt.get_cmap(
    "viridis"
).with_extremes(
    over="crimson",
)
~~~

`with_extremes(over="crimson")` กำหนดให้ค่าที่สูงกว่า `vmax` เป็นสีแดงเข้ม โดยไม่ได้เปลี่ยนค่าจริงในข้อมูล

### เซลล์ที่ 10 — ใช้ `extend="max"`

~~~python
fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    pm25_with_event,
    cmap=pm25_cmap,
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
    vmin=0,
    vmax=50,
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    extend="max",
    ticks=np.arange(0, 51, 10),
    pad=0.02,
)
colorbar.set_label(
    "PM2.5 concentration (µg/m³)"
)

ax.set(
    title="PM2.5 with a Fixed Color Scale",
    xlabel="Hour",
    ylabel="Building floor",
    xticks=np.arange(0, 25, 4),
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
~~~

`extend="max"` เพิ่มปลายรูปสามเหลี่ยมด้านค่าสูง เพื่อบอกว่ามีข้อมูลมากกว่า 50 µg/m³ แต่ Colorbar ไม่ได้บอกว่าค่าสูงสุดจริงคือ 58 หรือ 72 ต้องอ่านจากข้อมูล ตัวเลขกำกับ หรือระบบ Tooltip เพิ่มเติม

ค่าของ `extend` ที่ใช้ได้:

| ค่า | ความหมาย |
|-----|----------|
| `"neither"` | ไม่มีปลายขยาย |
| `"min"` | มีค่าต่ำกว่า `vmin` |
| `"max"` | มีค่าสูงกว่า `vmax` |
| `"both"` | มีค่าหลุดทั้งสองด้าน |

การจำกัดช่วงสีไม่ควรใช้เพื่อซ่อน Outlier ต้องระบุให้ชัดว่ามีค่าหลุดช่วงและตรวจสอบสาเหตุ เช่น Sensor Fault, Calibration Error หรือเหตุการณ์จริง

---

## 7. Diverging Colorbar และค่ากึ่งกลาง

สมมติระบบปรับอากาศตั้งเป้าอุณหภูมิไว้ที่ 24 °C สิ่งที่ต้องการดูอาจไม่ใช่อุณหภูมิโดยตรง แต่เป็นค่าที่ต่ำหรือสูงกว่าเป้าหมาย

### เซลล์ที่ 11 — Import `TwoSlopeNorm`

~~~python
from matplotlib.colors import TwoSlopeNorm
~~~

### เซลล์ที่ 12 — จำลองอุณหภูมิและคำนวณค่าเบี่ยงเบน

~~~python
rng_temperature = np.random.default_rng(7)
target_temperature = 24.0

temperature = (
    target_temperature
    + 2.3 * np.sin(
        (hours - 7) * np.pi / 12
    )
    + np.array(
        [1.0, 0.4, -0.3, -0.8]
    )[:, np.newaxis]
    + rng_temperature.normal(
        0,
        0.35,
        size=(4, hours.size),
    )
)

deviation = temperature - target_temperature
~~~

- ค่า `0` หมายถึงเท่ากับเป้าหมาย
- ค่าติดลบหมายถึงต่ำกว่าเป้าหมาย
- ค่าบวกหมายถึงสูงกว่าเป้าหมาย

### เซลล์ที่ 13 — กำหนด Center ด้วย `TwoSlopeNorm`

~~~python
temperature_norm = TwoSlopeNorm(
    vmin=-4,
    vcenter=0,
    vmax=4,
)
~~~

`vcenter=0` ทำให้สีกึ่งกลางตรงกับอุณหภูมิเป้าหมาย ไม่ใช่ปล่อยให้ Matplotlib เลือกกึ่งกลางจาก Min และ Max ของข้อมูลแต่ละชุด

### เซลล์ที่ 14 — สร้าง Diverging Colorbar

~~~python
fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    deviation,
    cmap="RdBu_r",
    norm=temperature_norm,
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    ticks=[-4, -2, 0, 2, 4],
    extend="both",
    pad=0.02,
)
colorbar.set_label(
    "Deviation from 24 °C (°C)"
)

ax.set(
    title="Temperature Deviation from the Target",
    xlabel="Hour",
    ylabel="Building floor",
    xticks=np.arange(0, 25, 4),
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
~~~

หากค่าเป้าหมายไม่อยู่กึ่งกลางของช่วง เช่นต้องการแสดงตั้งแต่ −2 ถึง +6 °C `TwoSlopeNorm` ยังสามารถวาง `vcenter=0` ไว้ที่ค่าที่มีความหมายได้

สีแดงไม่ได้หมายถึงอันตรายโดยอัตโนมัติ ในกราฟนี้หมายถึงสูงกว่าค่าเป้าหมายตามนิยามที่กำหนดเท่านั้น

---

## 8. Discrete Colorbar สำหรับช่วงสถานะ

ข้อมูลบางระบบถูกแบ่งเป็นระดับ เช่น Very low, Low, Moderate, High และ Very high ถึงแม้ข้อมูลต้นทางเป็นตัวเลขต่อเนื่อง แต่สีที่ต้องการแสดงเป็นช่วงชัดเจน

### เซลล์ที่ 15 — Import เครื่องมือสำหรับสีแบบแบ่งช่วง

~~~python
from matplotlib.colors import (
    BoundaryNorm,
    ListedColormap,
)
~~~

### เซลล์ที่ 16 — กำหนดขอบเขต สี และชื่อสถานะ

~~~python
boundaries = [0, 15, 25, 37.5, 50, 75]

status_labels = [
    "Very low",
    "Low",
    "Moderate",
    "High",
    "Very high",
]

status_colors = [
    "#2c7bb6",
    "#abd9e9",
    "#ffffbf",
    "#fdae61",
    "#d7191c",
]

status_cmap = ListedColormap(status_colors)

status_norm = BoundaryNorm(
    boundaries,
    ncolors=status_cmap.N,
    clip=True,
)
~~~

`ListedColormap` สร้าง Colormap จากรายการสี ส่วน `BoundaryNorm` จับค่าตัวเลขลงในช่วงที่กำหนด

ตัวอย่างเช่น:

- ค่า 10 อยู่ในช่วง 0–15
- ค่า 20 อยู่ในช่วง 15–25
- ค่า 42 อยู่ในช่วง 37.5–50

> ขอบเขตเหล่านี้เป็นค่าจำลองสำหรับอธิบายโค้ด ไม่ควรนำไปใช้แจ้งเตือนด้านสุขภาพหรือการปฏิบัติงานโดยไม่ตรวจสอบมาตรฐานและข้อกำหนดของโครงการ

### เซลล์ที่ 17 — สร้าง Discrete Colorbar

~~~python
pm25_status = np.clip(
    pm25_with_event,
    0,
    74.9,
)

tick_positions = [
    (lower + upper) / 2
    for lower, upper in zip(
        boundaries[:-1],
        boundaries[1:],
    )
]

fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    pm25_status,
    cmap=status_cmap,
    norm=status_norm,
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    boundaries=boundaries,
    ticks=tick_positions,
    spacing="proportional",
    pad=0.02,
)
colorbar.ax.set_yticklabels(status_labels)
colorbar.set_label(
    "Building-specific PM2.5 status"
)

ax.set(
    title="Discrete Indoor Air Quality Status",
    xlabel="Hour",
    ylabel="Building floor",
    xticks=np.arange(0, 25, 4),
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
~~~

ตำแหน่ง Tick อยู่กึ่งกลางของแต่ละช่วง เพื่อให้ชื่อสถานะอยู่ตรงกับแถบสี ส่วนขอบเขตจริงยังอยู่ในตัวแปร `boundaries`

หากผู้ใช้งานต้องทราบตัวเลขขอบเขตด้วย ควรแสดงค่าเหล่านั้นใน Tooltip, ตารางอธิบาย หรือใช้ Tick ที่ขอบแทนชื่อสถานะ ไม่ควรทำให้ Colorbar แน่นจนอ่านยาก

---

## 9. Missing Data และสีพิเศษ

Sensor อาจไม่ส่งข้อมูลเพราะแบตเตอรี่หมด Gateway Offline หรือ Packet สูญหาย ค่าที่หายไม่ควรถูกแสดงเป็นศูนย์ เพราะศูนย์เป็นค่าตัวเลขที่มีความหมายและอาจทำให้เข้าใจว่าอากาศสะอาดมาก

### เซลล์ที่ 18 — Mask ค่า `NaN`

~~~python
pm25_missing = pm25.copy()
pm25_missing[1, 4] = np.nan
pm25_missing[3, 8] = np.nan

masked_pm25 = np.ma.masked_invalid(
    pm25_missing
)

missing_cmap = plt.get_cmap(
    "viridis"
).with_extremes(
    bad="lightgray",
)
~~~

- `np.nan` แทนข้อมูลที่ไม่มีค่า
- `np.ma.masked_invalid()` Mask ค่า `NaN` และค่าที่ไม่เป็นจำนวนปกติ
- `bad="lightgray"` กำหนดสีสำหรับค่าที่ถูก Mask

### เซลล์ที่ 19 — แสดง Missing Data

~~~python
fig, ax = plt.subplots(figsize=(10, 5.5))

image = ax.imshow(
    masked_pm25,
    cmap=missing_cmap,
    aspect="auto",
    origin="lower",
    extent=[0, 24, 0.5, 4.5],
    vmin=0,
    vmax=30,
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    pad=0.02,
)
colorbar.set_label(
    "PM2.5 concentration (µg/m³)"
)

ax.set(
    title="PM2.5 with Missing Sensor Data",
    xlabel="Hour",
    ylabel="Building floor",
    yticks=np.arange(1, 5),
    yticklabels=floor_names,
)

fig.tight_layout()
plt.show()
~~~

สีเทาในตัวอย่างหมายถึง “ไม่มีข้อมูล” ไม่ได้หมายถึงค่าต่ำสุด ควรเพิ่ม Annotation หรือ Legend สั้น ๆ เพื่ออธิบายความหมายของสี Missing Data เพราะสีนี้อยู่นอก Scale ตัวเลขของ Colorbar

---

## 10. Logarithmic Color Scale

ข้อมูล IoT บางชนิดมีค่าต่างกันหลายลำดับขนาด เช่น 10, 100, 1,000 และ 10,000 หากใช้ Linear Scale ค่าสูงสุดจะครองช่วงสีส่วนใหญ่จนค่าต่ำดูคล้ายกันทั้งหมด

### เซลล์ที่ 20 — Import `LogNorm` และเตรียมข้อมูล

~~~python
from matplotlib.colors import LogNorm

particle_count = np.array(
    [
        [18, 25, 60, 450, 1200, 95, 35, 20],
        [12, 19, 45, 300, np.nan, 70, 28, 16],
        [8, 15, 32, 180, 6500, 55, 22, 11],
    ],
    dtype=float,
)

masked_count = np.ma.masked_invalid(
    particle_count
)
~~~

### เซลล์ที่ 21 — สร้าง Colorbar แบบ Logarithmic

~~~python
fig, ax = plt.subplots(figsize=(9, 4.8))

particle_cmap = plt.get_cmap(
    "magma"
).with_extremes(
    bad="lightgray",
    over="cyan",
)

image = ax.imshow(
    masked_count,
    cmap=particle_cmap,
    norm=LogNorm(
        vmin=10,
        vmax=5000,
    ),
    aspect="auto",
    origin="lower",
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    extend="max",
    ticks=[10, 100, 1000, 5000],
    pad=0.02,
)
colorbar.set_label(
    "Particle count (particles/L)"
)

ax.set(
    title="Particle Count with Logarithmic Color Scaling",
    xlabel="Measurement window",
    ylabel="Sensor node",
    yticks=[0, 1, 2],
    yticklabels=["AQ-01", "AQ-02", "AQ-03"],
)

fig.tight_layout()
plt.show()
~~~

`LogNorm` ทำให้ระยะจาก 10 ไป 100 ใกล้เคียงกับระยะจาก 100 ไป 1,000 บน Scale สี เพราะแต่ละช่วงเพิ่มขึ้นสิบเท่า

ข้อควรระวัง:

- Log Scale ใช้กับศูนย์และค่าติดลบไม่ได้
- ต้องบอกให้ชัดว่า Colorbar เป็น Logarithmic
- ความต่างของระยะสีไม่ได้แทนผลต่างแบบบวก–ลบตาม Linear Scale
- อย่าใช้ Log Scale เพียงเพื่อทำให้กราฟดูมีรายละเอียดมากขึ้นโดยไม่อธิบายเหตุผล

---

## 11. Colorbar กับ Scatter Plot

Colorbar ไม่ได้ใช้เฉพาะกับ `imshow()` หากสีของจุดใน Scatter Plot มาจากตัวเลข สามารถส่งผลลัพธ์ของ `scatter()` ให้ Colorbar ได้เช่นกัน

### เซลล์ที่ 22 — สีของ Sensor Node แทนค่า PM2.5

~~~python
sensor_x = np.array([1, 3, 5, 7, 9, 4])
sensor_y = np.array([1, 4, 2, 4, 1, 3])
sensor_pm25 = np.array([8, 14, 22, 35, 48, 18])

fig, ax = plt.subplots(figsize=(9, 5))

points = ax.scatter(
    sensor_x,
    sensor_y,
    c=sensor_pm25,
    cmap="viridis",
    vmin=0,
    vmax=50,
    s=180,
    edgecolor="black",
)

colorbar = fig.colorbar(
    points,
    ax=ax,
    pad=0.02,
)
colorbar.set_label(
    "PM2.5 concentration (µg/m³)"
)

ax.set(
    title="Indoor Air Quality Sensor Map",
    xlabel="Building X position (m)",
    ylabel="Building Y position (m)",
)
ax.grid(alpha=0.2)

fig.tight_layout()
plt.show()
~~~

ตัวแปร `points` เป็น Mappable เหมือนกับ `image` เพราะเก็บ Colormap และ Normalization ของสีจุดไว้

ถ้าสีของจุดถูกกำหนดเป็นสีคงที่ เช่น `color="royalblue"` สีจะไม่ได้มาจากค่าตัวเลข จึงไม่จำเป็นต้องมี Colorbar

---

## 12. แนวทางสำหรับ IoT Dashboard จริง

### ใช้ช่วงสีคงที่เมื่อเปรียบเทียบ

- Dashboard หลาย Device ควรใช้ `vmin` และ `vmax` เดียวกันเมื่อหน่วยและบริบทเหมือนกัน
- กราฟวันนี้กับเมื่อวานควรใช้ Scale เดียวกันเพื่อให้สีเปรียบเทียบได้
- หากเปลี่ยน Scale แบบอัตโนมัติ ต้องแสดงช่วงค่าให้เด่นและแจ้งให้ผู้ใช้งานทราบ

### ระบุหน่วยและแหล่งข้อมูล

- Colorbar Label ต้องมีหน่วย เช่น °C, %, ppm หรือ µg/m³
- ตรวจการแปลงหน่วยก่อนรวม Sensor ต่างรุ่น
- เก็บ Device ID, Calibration Date และ Timestamp ไว้กับข้อมูล

### แยก Missing Data ออกจากค่าต่ำ

- Sensor Offline ไม่ควรกลายเป็นค่า 0
- ใช้ Mask และสี `bad` สำหรับข้อมูลที่หาย
- แสดง Last Update หรือ Data Freshness เพิ่มเติม

### ระวังการ Interpolation

Heatmap จาก Sensor ที่ติดตั้งห่างกันอาจมีพื้นที่ซึ่งเป็นค่าประมาณ สีที่เรียบไม่ได้หมายความว่ามีการวัดจริงทุกตำแหน่ง ควรแสดงตำแหน่ง Sensor และอธิบายวิธี Interpolation เมื่อมีการประมาณค่าเชิงพื้นที่

### อย่าให้สีตัดสินสถานะแทนกฎระบบ

Colorbar แสดงการจับคู่สี ไม่ได้กำหนด Alarm Logic โดยอัตโนมัติ Threshold ต้องมาจากข้อกำหนดของระบบ มาตรฐานที่เกี่ยวข้อง ผู้เชี่ยวชาญ และผลกระทบของ False Alarm กับ Missed Detection

---

## 13. เลือก Colorbar แบบไหนดี

| ลักษณะข้อมูล | แนวทาง | ตัวอย่าง |
|--------------|--------|----------|
| ค่าต่ำไปสูง | Sequential Colormap | PM2.5, Humidity, Energy |
| เบี่ยงเบนจากค่ากลาง | Diverging + `TwoSlopeNorm` | ต่างจาก Target Temperature |
| แบ่งระดับชัดเจน | `ListedColormap` + `BoundaryNorm` | Building Status Level |
| ค่าห่างกันหลายลำดับขนาด | `LogNorm` | Particle Count |
| มีค่าหลุดช่วง | `extend` + Over/Under Color | Pollution Event |
| มีข้อมูลหาย | Mask + Bad Color | Sensor Offline |
| สีแทนหมวดหมู่ไม่ต่อเนื่อง | พิจารณา Legend | Device Type, Online/Offline |

## แบบฝึกหัด

1. เปลี่ยน Colormap ของ PM2.5 เป็น `cividis`, `magma` และ `Blues` แล้วเปรียบเทียบ
2. สร้าง Colorbar แนวนอนและปรับ `shrink`, `aspect` กับ `pad`
3. ล็อก Scale ที่ 0–40 µg/m³ แล้วเพิ่มค่าที่สูงกว่า 40
4. ทดลอง `extend="max"` และกำหนด Over Color
5. เปลี่ยน Target Temperature จาก 24 เป็น 25 °C แล้วคำนวณ Deviation ใหม่
6. สร้าง Discrete Colorbar จากช่วงที่กำหนดโดยผู้สอน
7. เพิ่ม Missing Data และอธิบายด้วยสีที่ไม่ซ้ำกับค่าต่ำสุด
8. เปรียบเทียบ Linear Scale กับ `LogNorm` สำหรับ Particle Count

อ่านโจทย์ฉบับเต็มได้ที่ [แบบฝึกหัด EP7](./exercises/exercise01.md)

## โจทย์ท้าทายย่อย

สร้าง Smart Building Air Quality Dashboard ที่มี:

- Heatmap ของ PM2.5 แยกตามชั้นและเวลา
- Colorbar พร้อมหน่วยและ Tick ที่อ่านง่าย
- ช่วงสีคงที่สำหรับเปรียบเทียบหลายวัน
- สีเฉพาะสำหรับ Missing Data และค่าที่เกินช่วง
- กราฟอุณหภูมิเบี่ยงเบนจาก Target ด้วย Diverging Colormap
- ตำแหน่ง Sensor Node บนแผนผังอาคาร
- Device ID, เวลาที่อัปเดตล่าสุด และสถานะ Gateway
- คำอธิบายว่า Threshold และช่วงสีมาจาก Config ใด

## สคริปต์ฉบับเต็ม

- [basic_pm25_colorbar.py](./source-code/basic_pm25_colorbar.py)
- [fixed_scale_and_extend.py](./source-code/fixed_scale_and_extend.py)
- [temperature_deviation_colorbar.py](./source-code/temperature_deviation_colorbar.py)
- [discrete_air_quality_colorbar.py](./source-code/discrete_air_quality_colorbar.py)
- [log_scale_and_missing_data.py](./source-code/log_scale_and_missing_data.py)

## ตอนถัดไป

**EP8 — Multiple Subplots**
