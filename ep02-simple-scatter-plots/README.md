# EP2 — Simple Scatter Plots

ยินดีต้อนรับสู่ตอนที่ 2 ของชุดบทเรียน **การสร้างภาพข้อมูลด้วย Python และ Matplotlib**

## วัตถุประสงค์การเรียนรู้

- เข้าใจกราฟกระจาย (scatter plot)
- สร้างกราฟด้วย `plot()` และ `scatter()`
- ปรับรูปแบบ ขนาด สี และความโปร่งใส (`alpha`) ของจุด
- ใช้แผนผังสี (colormap)
- เลือกใช้ `plot()` หรือ `scatter()` ให้เหมาะสม

## ตัวอย่างที่ 1

~~~python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 30)
y = np.sin(x)

plt.scatter(x, y)
plt.show()
~~~

กราฟกระจายแสดงแต่ละค่าสังเกตเป็นจุดข้อมูลแยกกัน

## การปรับแต่งจุด

~~~python
plt.scatter(x, y, marker="o", color="royalblue", s=80, alpha=0.5)
~~~

- `marker` — รูปแบบจุด
- `color` — สี
- `s` — ขนาดจุด
- `alpha` — ความโปร่งใส ช่วยให้เห็นจุดที่ซ้อนทับกัน

## การแสดงข้อมูลหลายมิติ

~~~python
rng = np.random.default_rng(0)
x = rng.normal(size=100)
y = rng.normal(size=100)
sizes = rng.uniform(20, 200, 100)
colors = rng.random(100)

plt.scatter(x, y, s=sizes, c=colors, cmap="viridis", alpha=0.7)
plt.colorbar()
~~~

## `plot()` กับ `scatter()`

ใช้ `plot()` เมื่อต้องการเชื่อมจุดด้วยเส้น หรือมีข้อมูลจำนวนมากและทุกจุดใช้รูปแบบเดียวกัน ใช้ `scatter()` เมื่อต้องการให้ขนาดหรือสีของจุดแสดงข้อมูลเพิ่มเติม

## แบบฝึกหัด

1. วาดกราฟ y = x² ด้วยกราฟกระจาย
2. เปลี่ยนรูปแบบ สี และขนาดของจุด
3. เพิ่มชื่อกราฟและชื่อแกน

## โจทย์ท้าทายย่อย

ใช้ข้อมูลสุ่มสร้างกราฟกระจายที่ปรับแต่งจนพร้อมใช้ในการนำเสนอ

## ตอนถัดไป

**EP3 — Visualizing Errors**