# แบบฝึกหัด EP7 — Customizing Colorbars for Smart Building IoT

แบบฝึกหัดนี้ใช้ข้อมูลสังเคราะห์เพื่อฝึกการเลือก Colormap และ Colorbar ให้ตรงกับความหมายของข้อมูล ไม่ควรนำช่วงสถานะตัวอย่างไปใช้เป็นเกณฑ์สุขภาพหรือ Alarm ของระบบจริง

## ส่วนที่ 1: Colorbar พื้นฐาน

สร้าง Heatmap ค่า PM2.5 ของอาคารสี่ชั้น โดยต้องมี:

- ชื่อกราฟและชื่อแกน
- Colorbar พร้อมหน่วย µg/m³
- Tick ตั้งแต่ 0–30 ครั้งละ 5
- `origin="lower"`
- `aspect="auto"`

อธิบายว่า Object ที่คืนจาก `imshow()` ทำหน้าที่เป็น Mappable อย่างไร

## ส่วนที่ 2: เปรียบเทียบ Colormap

สร้างกราฟจากข้อมูลชุดเดียวกันด้วย:

- `viridis`
- `cividis`
- `magma`
- `jet`

เปรียบเทียบความต่อเนื่องของความสว่าง จุดที่สายตาสนใจ และความเหมาะสมเมื่อพิมพ์แบบ Grayscale ห้ามเลือกจากความสวยเพียงอย่างเดียว

## ส่วนที่ 3: Layout ของ Colorbar

ทดลอง Colorbar แนวตั้งและแนวนอน พร้อมปรับ:

- `pad`
- `shrink`
- `aspect`
- `labelpad`

ทดสอบบน Figure ขนาด `(6, 4)` และ `(12, 5)` แล้วบันทึกว่ารูปแบบใดเหมาะกับหน้าจอแต่ละขนาด

## ส่วนที่ 4: Fixed Scale และ Out-of-range

เพิ่มค่า PM2.5 เป็น 65 และ 90 µg/m³ แล้ว:

- ล็อกช่วงสีด้วย `vmin=0`, `vmax=50`
- ใช้ `extend="max"`
- กำหนด Over Color
- แสดงค่าสูงสุดจริงไว้ในชื่อกราฟหรือ Annotation

ตอบคำถามว่าเหตุใดสามเหลี่ยมที่ปลาย Colorbar จึงไม่ได้บอกค่าสูงสุดจริง

## ส่วนที่ 5: Diverging Colorbar

กำหนดอุณหภูมิเป้าหมายเป็น 25 °C แล้วคำนวณค่าเบี่ยงเบน จากนั้นใช้:

- Diverging Colormap
- `TwoSlopeNorm`
- `vcenter=0`
- Tick ที่ −4, −2, 0, 2 และ 4

อธิบายความหมายของค่าติดลบ ศูนย์ และค่าบวกในบริบทนี้

## ส่วนที่ 6: Discrete Colorbar

กำหนดช่วงสถานะจำลองของ CO₂ ห้าระดับ แล้วสร้าง Colorbar ด้วย:

- `ListedColormap`
- `BoundaryNorm`
- Tick อยู่กึ่งกลางแต่ละช่วง
- Label ของแต่ละสถานะ

ระบุไว้บนกราฟว่าช่วงเหล่านี้เป็นค่าฝึกหัด ไม่ใช่มาตรฐานอาคารจริง

## ส่วนที่ 7: Missing Data

เปลี่ยนค่าบางตำแหน่งเป็น `np.nan` แล้ว:

- Mask ค่าที่ไม่ถูกต้อง
- กำหนด Bad Color เป็นสีเทา
- เพิ่มคำอธิบายว่า Gray หมายถึง Missing Data
- ห้ามแทน Missing Data ด้วยศูนย์

อธิบายผลกระทบที่จะเกิดขึ้นหากระบบแทน Sensor Offline ด้วยค่า 0

## ส่วนที่ 8: Logarithmic Scale

สร้างข้อมูล Particle Count ตั้งแต่ 10 ถึง 100,000 แล้วเปรียบเทียบ:

- Linear Normalization
- `LogNorm`

ตอบคำถาม:

1. เพราะเหตุใดค่าต่ำจึงดูคล้ายกันเมื่อใช้ Linear Scale
2. เพราะเหตุใด `LogNorm` จึงใช้กับศูนย์ไม่ได้
3. ผู้อ่านกราฟจะทราบได้อย่างไรว่า Colorbar ใช้ Log Scale

## โจทย์ท้าทาย: Smart Building Air Quality Dashboard

สร้าง Dashboard อย่างน้อยสามกราฟ:

- PM2.5 Heatmap แยกตามชั้นและเวลา
- Temperature Deviation จาก Target
- แผนที่ตำแหน่ง Sensor Node ที่สีแทน CO₂

ข้อกำหนดเพิ่มเติม:

- ทุก Colorbar ต้องมีหน่วย
- กราฟที่เปรียบเทียบกันต้องใช้ช่วงสีเดียวกัน
- Missing Data ต้องแยกจากค่าต่ำสุด
- ค่านอกช่วงต้องแสดงด้วย `extend`
- มี Device ID, Timestamp และสถานะ Gateway
- อธิบายเหตุผลของ Colormap และ Normalization ที่เลือก
