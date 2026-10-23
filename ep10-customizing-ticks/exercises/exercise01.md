# แบบฝึกหัด EP10 — Customizing Ticks

แบบฝึกหัดชุดนี้ใช้ข้อมูลจาก [`cold_chain_data.py`](../source-code/cold_chain_data.py) ให้ทดลองทีละข้อและสังเกตผลที่แกนของกราฟ ไม่จำเป็นต้องทำทุกข้อในครั้งเดียว

รอบแรกทำข้อ 1, 2, 5 และ 6–7 ก่อน ส่วนข้อ 3, 4, 8 และ Challenge เป็นการต่อยอด ทุกข้อให้เปลี่ยนครั้งละอย่าง แล้วตอบว่า **ตำแหน่งขีด ข้อความ หรือหน้าตาขีด** เปลี่ยนไปอย่างไร

## เตรียมข้อมูล

~~~python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from cold_chain_data import create_cold_chain_day

data = create_cold_chain_day()
hours = data["hours"]
temperature = data["cold_room_temperature"]
~~~

หากสร้าง Notebook ไว้นอกโฟลเดอร์ `source-code` สามารถคัดลอก Function จากไฟล์ดังกล่าวมาไว้ใน Notebook ได้

## ข้อ 1 — เปลี่ยนระยะของ Major Tick

จุดที่แก้: ตัวเลขใน `MultipleLocator(...)` ไม่ใช่ข้อมูลอุณหภูมิหรือขนาด Figure

วาดอุณหภูมิห้องเย็น แล้วกำหนด Major Tick ทุก 3 ชั่วโมงด้วย `MultipleLocator`

ผลที่ควรสังเกต:

- ตำแหน่งบนแกน X ควรเป็น `0, 3, 6, ... 24`
- Label ต้องไม่ชนกันเมื่อใช้ Figure กว้างประมาณ 10 นิ้ว

## ข้อ 2 — เพิ่ม Minor Tick ทุก 30 นาที

จุดที่แก้: ส่ง Locator ให้ `ax.xaxis.set_minor_locator(...)` ไม่ใช่ `set_major_locator(...)`

กำหนด Minor Locator ด้วย:

~~~python
mticker.MultipleLocator(0.5)
~~~

จากนั้นทำ Minor Grid ให้จางกว่า Major Grid และอธิบายว่า `0.5` ชั่วโมงเท่ากับกี่นาที

## ข้อ 3 — ตำแหน่งตายตัวกับกติกาที่ยืดหยุ่น

สร้างกราฟสองช่องโดยใช้ข้อมูลเดียวกัน:

- ช่องซ้ายใช้ `set_xticks([0, 4, 8, 12, 16, 20, 24])`
- ช่องขวาใช้ `MultipleLocator(4)`

ตั้ง `xlim` ของทั้งสองช่องเป็น `(0, 24)` ก่อน แล้วเปลี่ยนเป็น `(0, 32)` หลังคำสั่งกำหนด Tick ทั้งหมด

ผลที่ควรเห็น: ด้านที่ใช้ `MultipleLocator(4)` มี Tick ที่ 28 และ 32 เพิ่มให้ ส่วนรายการตายตัวจบที่ 24 พื้นที่หลังชั่วโมงที่ 24 ไม่มีข้อมูลทั้งสองช่อง เพราะเราเปลี่ยนช่วงแกน ไม่ได้สร้างข้อมูลเพิ่ม

ถ้าลองเพียงย่อช่วงเป็น `(8, 16)` ทั้งสองภาพอาจมี Tick เหมือนกัน จึงไม่ใช่ตัวอย่างที่แสดงความต่างได้ชัด

## ข้อ 4 — Formatter แบบ 12 ชั่วโมง

เขียน Function ให้ Major Label แสดงเป็น:

~~~text
12 AM, 4 AM, 8 AM, 12 PM, 4 PM, 8 PM, 12 AM
~~~

แล้วนำ Function ไปใช้ผ่าน `FuncFormatter`

คำใบ้: แยกกรณีเที่ยงคืน เที่ยงวัน ก่อนคำนวณชั่วโมงที่เหลือด้วย `% 12`

## ข้อ 5 — ลด Tick ในกราฟขนาดเล็ก

จุดที่แก้: `nbins` ของแกน Y เท่านั้น ใช้ข้อมูล ขนาด Figure และช่วงแกนเดิม เพื่อให้เปรียบเทียบได้ตรงกัน

สร้าง Subplots ขนาด 2×2 แล้วทดลองค่าต่อไปนี้กับแกน Y:

~~~python
mticker.MaxNLocator(nbins=3)
mticker.MaxNLocator(nbins=5)
mticker.MaxNLocator(nbins=8)
~~~

ตอบคำถาม:

1. ค่าใดอ่านง่ายที่สุดใน Figure ขนาดที่เลือก
2. `nbins=5` ทำให้ได้ Tick 5 จุดเสมอหรือไม่
3. หากย่อ Figure ลง ควรเพิ่มหรือลด `nbins`

## ข้อ 6 — ซ่อนเฉพาะข้อความ

จุดที่แก้: Formatter ของแกน X เริ่มจากกราฟใหม่ที่มี Major Tick และไม่มี Minor Tick

ใช้ `NullFormatter` กับแกน X และเปิด Grid ไว้ จากนั้นตรวจว่า:

- Tick positions ยังอยู่หรือไม่
- Grid lines ยังอยู่หรือไม่
- ข้อมูลใน Array เปลี่ยนหรือไม่

## ข้อ 7 — ลบตำแหน่ง Tick

สร้างกราฟใหม่เหมือนข้อ 6 แต่เปลี่ยนคำสั่งที่ทดลองเป็น:

~~~python
ax.xaxis.set_major_locator(mticker.NullLocator())
~~~

ต้องเปรียบเทียบแกน X เหมือนกัน ไม่เปลี่ยนไปทดลองกับแกน Y และไม่ต้องนำ `NullFormatter` จากข้อก่อนมารันซ้ำ

ผลที่ควรเห็น: ตัวเลข ขีดหลัก และ Grid แนวตั้งของขีดหลักหายไป แต่เส้นข้อมูลกับขอบแกนยังอยู่ อธิบายความต่างจากข้อ 6 ด้วยประโยคสั้น ๆ หนึ่งประโยค

## ข้อ 8 — หมวดหมู่ของคลังสินค้า

จุดที่เน้น: จับคู่ตำแหน่งกับชื่อผ่าน `set_xticks(..., labels=...)` ส่วน `bar()` และความสูงแท่งเป็นโครงเดิม

สร้าง Bar Chart จากข้อมูลต่อไปนี้:

~~~python
warehouse_names = [
    "North Hub",
    "East Hub",
    "Central Hub",
    "South Hub",
]

average_temperature = [
    -19.8,
    -20.3,
    -19.5,
    -20.0,
]
~~~

กำหนดตำแหน่งและ Label ด้วย `ax.set_xticks(positions, labels=...)` ในคำสั่งเดียว แล้วใช้ `MaxNLocator` ลดจำนวน Tick บนแกน Y

## Challenge — Daily Cold-Chain Report

ข้อนี้รวมสิ่งที่เรียนแล้ว ไม่ได้เพิ่ม API ใหม่ ลองทำเมื่อแยกหน้าที่ Locator กับ Formatter ได้ก่อน

สร้าง Figure สองแถวที่ใช้แกน X ร่วมกัน:

- แถวบนแสดงอุณหภูมิห้องเย็น
- แถวล่างแสดงโหลด Compressor
- Major Tick ทุก 4 ชั่วโมง พร้อม Label แบบ `HH:00`
- Minor Tick ทุก 1 ชั่วโมง
- ใช้ `MaxNLocator(nbins=5)` กับแกน Y เพื่อควบคุมความแน่นของ Tick
- Major Grid เข้มกว่า Minor Grid

เมื่อเสร็จแล้วเปรียบเทียบกับ [`cold_chain_tick_dashboard.py`](../source-code/cold_chain_tick_dashboard.py) โดยพิจารณาหลักการก่อนเปรียบเทียบรายละเอียดโค้ด

## Checklist ก่อนจบแบบฝึกหัด

- Locator เลือกตำแหน่ง Tick
- Formatter สร้างข้อความให้ตำแหน่งนั้น
- Major Tick ใช้อ่านค่าหลัก
- Minor Tick ใช้ช่วยกะระยะ
- `tick_params()` ปรับหน้าตา ไม่ได้ย้ายตำแหน่ง
- Formatter ไม่เปลี่ยนค่าจริงในข้อมูล
