# EP1 — Introduction to Matplotlib

ยินดีต้อนรับสู่ตอนแรกของชุดบทเรียน **การสร้างภาพข้อมูลด้วย Python และ Matplotlib**

## วัตถุประสงค์การเรียนรู้

เมื่อเรียนจบตอนนี้ คุณจะสามารถ:
- อธิบายบทบาทของ Matplotlib ใน Python
- สร้างและจัดการออบเจ็กต์ Figure และ Axes
- สร้างกราฟเส้นและแสดงข้อมูลหลายชุดในกราฟเดียว
- ปรับแต่งสี รูปแบบเส้น และช่วงของแกน
- เพิ่มชื่อกราฟ ชื่อแกน และคำอธิบายกราฟ
- เข้าใจสถาปัตยกรรม Figure–Axes

## สิ่งที่ต้องมีก่อนเริ่ม

Python 3, NumPy, Matplotlib และโปรแกรมเขียนโค้ดหรือ Notebook ที่คุณถนัด

## การติดตั้ง

~~~bash
python -m pip install matplotlib numpy
~~~

## ตัวอย่างที่ 1 — กราฟเส้นแรก

~~~python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 500)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("คลื่นไซน์")
plt.show()
~~~

## Figure กับ Axes ต่างกันอย่างไร

- **Figure** คือพื้นที่ทั้งหมดของภาพ
- **Axes** คือพื้นที่ภายใน Figure ที่ใช้วาดกราฟ

Figure หนึ่งภาพสามารถมี Axes ได้หนึ่งหรือหลายชุด

## การแสดงเส้นหลายเส้น

~~~python
ax.plot(x, np.sin(x), label="sin(x)")
ax.plot(x, np.cos(x), label="cos(x)")
ax.legend()
~~~

## การปรับแต่งรูปแบบ

ลองปรับ `color` (สี), `linestyle` (รูปแบบเส้น), `linewidth` (ความหนา) และ `marker` (สัญลักษณ์จุด)

~~~python
ax.plot(x, np.sin(x), color="royalblue", linestyle="--", linewidth=2)
ax.set_xlim(0, 10)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("กราฟอย่างง่าย")
~~~

## แบบฝึกหัด

1. วาดกราฟ y = x²
2. วาดกราฟ sin(x) และ cos(x) ในภาพเดียวกัน
3. เปลี่ยนสีและรูปแบบเส้น
4. เพิ่มชื่อกำกับและคำอธิบายกราฟ
5. ส่งออกกราฟเป็นไฟล์ PNG

## โจทย์ท้าทาย

สร้างกราฟที่มีฟังก์ชันทางคณิตศาสตร์สามฟังก์ชัน และปรับแต่งให้พร้อมใช้ในการนำเสนอ

## ตอนถัดไป

**EP2 — Simple Scatter Plots**