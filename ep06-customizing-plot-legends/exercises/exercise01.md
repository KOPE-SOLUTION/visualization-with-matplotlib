# แบบฝึกหัด EP6 — Customizing Plot Legends for Smart Farm

แบบฝึกหัดนี้ใช้ข้อมูลสังเคราะห์จากบทหลัก ผู้เรียนสามารถเพิ่ม Noise เล็กน้อยด้วย NumPy เพื่อให้ข้อมูลใกล้เคียงการวัดจริงขึ้น

## ส่วนที่ 1: Legend พื้นฐาน

สร้างกราฟอุณหภูมิของ Greenhouse A, Greenhouse B และ Outdoor Sensor แล้ว:

- ใส่ `label` ให้ทุกเส้น
- เรียก `ax.legend()`
- ทดลอง `loc` อย่างน้อยสี่ตำแหน่ง
- อธิบายว่าตำแหน่งใดบดบังข้อมูลน้อยที่สุด

## ส่วนที่ 2: รูปแบบและ Layout

ปรับ Legend ให้มี:

- Title เป็น `Sensor location`
- สองคอลัมน์
- กรอบมุมโค้ง
- `framealpha=0.8`
- ระยะห่างระหว่างรายการที่อ่านง่าย

จากนั้นทดสอบบน Figure ขนาด `(6, 4)` และ `(12, 5)` แล้วเปรียบเทียบผล

## ส่วนที่ 3: Legend ด้านนอก

เพิ่มข้อมูล Greenhouse C และ Greenhouse D แล้ววาง Legend ด้านขวานอก Axes ด้วย `bbox_to_anchor`

บันทึกกราฟเป็น PNG โดย Legend ต้องไม่ถูกตัดออกจากภาพ

## ส่วนที่ 4: เลือก Handles

สร้างกราฟที่มีเส้น Sensor สี่เส้น แต่ให้ Legend แสดงเพียง:

- Greenhouse A
- Greenhouse C
- Outdoor Sensor

ห้ามลบเส้นอื่นออกจากกราฟ ให้เลือกเฉพาะ Handles ที่ต้องการ

## ส่วนที่ 5: Custom Status Legend

สร้าง Custom Legend สำหรับสถานะ:

- Online: วงกลมสีเขียว
- Warning: สามเหลี่ยมสีส้ม
- Offline: กากบาทสีเทา
- Maintenance: สี่เหลี่ยมสีน้ำเงิน

อธิบายว่าทำไม Marker Shape จึงช่วยให้กราฟเข้าถึงได้ดีกว่าการใช้สีอย่างเดียว

## ส่วนที่ 6: Size Legend และ Colorbar

จำลอง Sensor Node อย่างน้อยแปดตัว โดยกำหนด:

- X, Y เป็นตำแหน่งในแปลง
- สีเป็น Soil Moisture (%)
- ขนาดเป็น Coverage Area (m²)

สร้าง Size Legend ที่มีค่าตัวอย่าง 10, 30 และ 60 m² พร้อม Colorbar สำหรับความชื้นดิน

ตอบคำถาม:

1. ทำไม Soil Moisture จึงควรใช้ Colorbar แทน Legend หลายรายการ
2. ค่า `s` ใน `scatter()` มีหน่วยเป็นอะไร
3. ทำไมขนาด Marker ของ `Line2D` จึงต้องสัมพันธ์กับรากที่สองของพื้นที่

## ส่วนที่ 7: Multiple Legends

สร้างกราฟที่มี Legend สองกล่อง:

- กล่องแรกอธิบาย Sensor Location
- กล่องที่สองอธิบาย Target Range และ Warning Threshold

ทดลองลบ `ax.add_artist(first_legend)` แล้วบันทึกว่าเกิดอะไรขึ้น

## โจทย์ท้าทาย: Smart Farm Monitoring Dashboard

สร้าง Dashboard ด้วย Matplotlib ที่ประกอบด้วยกราฟอย่างน้อยสอง Axes:

- Axes แรกแสดงอุณหภูมิรายชั่วโมงของสาม Zone
- Axes ที่สองแสดงตำแหน่ง Soil Moisture Sensor
- มี Threshold, Target Range, Colorbar และ Legend ที่จำเป็น
- มีสถานะ Online, Warning, Offline และ Maintenance
- มี Device ID และเวลาที่อัปเดตล่าสุด
- สีและ Marker ต้องอ่านได้แม้ผู้ชมแยกบางสีได้ยาก

เขียนคำอธิบายสั้น ๆ ว่า Legend แต่ละกล่องตอบคำถามอะไร และข้อมูลใดไม่ควรใส่ใน Legend
