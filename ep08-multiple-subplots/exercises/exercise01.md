# แบบฝึกหัด EP8 — Multiple Subplots for Manufacturing Monitoring

แบบฝึกหัดนี้ใช้ข้อมูลสังเคราะห์เพื่อฝึกออกแบบ Figure ที่มีหลาย Axes ค่า Target และ Threshold ที่ผู้เรียนกำหนดขึ้นมีไว้เพื่อทดลองเขียนโปรแกรมเท่านั้น ไม่ใช่ข้อกำหนดสำหรับเครื่องจักรจริง

## ส่วนที่ 1: Figure และ Axes

สร้าง Figure ที่มี Axes หนึ่งช่อง แล้วพิมพ์:

- Type ของ `fig`
- Type ของ `ax`
- จำนวน Axes ใน `fig.axes`

อธิบายความแตกต่างระหว่าง Figure, Axes และ Axis ด้วยภาษาของตนเอง

## ส่วนที่ 2: กริด 1×3

สร้าง Subplot หนึ่งแถวสามคอลัมน์สำหรับ Output Rate ของ Line A, B และ C โดยต้องมี:

- Figure Size ที่อ่าน Label ได้ครบ
- ชื่อกราฟทุกช่อง
- ชื่อแกนและหน่วย
- Grid โปร่งใส
- Figure Title หนึ่งรายการ

ตรวจและรายงาน `axes.shape`

## ส่วนที่ 3: กริด 2×2 และ `axes.flat`

แสดงข้อมูลสี่ชุด:

- Output Rate
- Motor Temperature
- Vibration
- Defect Rate

เก็บข้อมูลสำหรับ Plot ไว้ใน List แล้วใช้ `zip()` ร่วมกับ `axes.flat` ห้ามเขียนคำสั่ง Plot ซ้ำสี่ชุดแบบ Copy-paste

## ส่วนที่ 4: Shared Axes

สร้างกราฟสามแถวสำหรับ Output Rate ของ Line A, B และ C แล้วทดลอง:

1. ไม่ Share Axis
2. `sharex=True`
3. `sharex=True, sharey=True`

ตอบคำถามว่ารูปแบบใดเปรียบเทียบประสิทธิภาพของแต่ละ Line ได้ตรงที่สุด และเหตุใดไม่ควร Share Y Axis ระหว่าง Temperature กับ Vibration

## ส่วนที่ 5: `squeeze=False`

เขียน Function ชื่อ `make_grid(nrows, ncols)` ซึ่งสร้าง Subplot ด้วย `squeeze=False` แล้วคืน `fig, axes`

ทดสอบกับ:

- 1×1
- 1×3
- 3×1
- 2×2

พิมพ์ Shape ทุกกรณีและอธิบายประโยชน์ของการคง Array สองมิติ

## ส่วนที่ 6: อัตราส่วนพื้นที่

สร้าง Layout หนึ่งแถวสองคอลัมน์:

- ด้านซ้ายเป็นแนวโน้ม Output Rate
- ด้านขวาเป็น Bar Chart ของ Output เฉลี่ย

ทดลอง `width_ratios` เป็น `[1, 1]`, `[2, 1]` และ `[3, 1]` แล้วเลือกค่าที่เหมาะกับการนำเสนอ พร้อมอธิบายเหตุผล

## ส่วนที่ 7: GridSpec

สร้าง GridSpec ขนาด 2×3 โดยกำหนดให้:

- Output Rate ครอบคลุมสองคอลัมน์ด้านบน
- Summary อยู่ขวาบน
- Temperature, Vibration และ Defect Rate อยู่แถวล่าง

เพิ่ม `layout="constrained"` และตรวจว่า Label ทุกส่วนไม่ซ้อนกัน

## ส่วนที่ 8: Subplot Mosaic

สร้าง Layout จากชื่อ:

~~~text
output output quality
temperature vibration quality
~~~

ข้อกำหนด:

- เรียก Axes ผ่าน Dictionary ด้วยชื่อ
- `output` ต้องมีเส้นของสาม Production Line
- `quality` ต้องครอบคลุมสองแถว
- ทุก Axes ต้องมีหน่วย

เปรียบเทียบความอ่านง่ายของโค้ด Mosaic กับ GridSpec

## ส่วนที่ 9: Manual Inset

ใช้ `fig.add_axes()` สร้าง:

- Main Axes สำหรับ Output Rate
- Inset Axes สำหรับ Defect Rate

ทดลองเปลี่ยน `[left, bottom, width, height]` ของ Inset และบันทึกว่าค่าใดทำให้ Inset ไม่บดบังจุดสำคัญ

## ส่วนที่ 10: Missing Data

เปลี่ยนค่า Vibration บางช่วงเป็น `np.nan` เพื่อจำลอง Sensor Offline แล้วแสดงใน Dashboard โดยห้ามแทนค่าที่หายด้วยศูนย์

เพิ่มข้อความสั้น ๆ ว่าช่วงว่างหมายถึง Missing Data และอธิบายผลเสียหากเชื่อมเส้นผ่านช่วงที่ไม่มีการวัดจริง

## โจทย์ท้าทาย: Manufacturing Shift Dashboard

สร้าง Dashboard สำหรับหนึ่งกะการผลิต โดยมีอย่างน้อยห้า Axes:

- Output Rate ของสามสายการผลิต
- Output เฉลี่ยของแต่ละ Line
- Motor Temperature
- Vibration
- Defect Rate หรือ Reject Count

ข้อกำหนดเพิ่มเติม:

- กราฟหลักต้องมีพื้นที่มากกว่ากราฟสรุป
- Share Axis เฉพาะข้อมูลที่มีหน่วยและช่วงเวลาเดียวกัน
- ใช้สีเดียวกันสำหรับ Line เดียวกันทุก Axes
- แสดง Target หรือ Threshold พร้อมคำอธิบาย
- แสดง Missing Data แยกจากค่าศูนย์
- ระบุรหัสเครื่องจักร ช่วงเวลากะ และเวลาที่อัปเดตล่าสุด
- Export เป็น PNG แล้วตรวจว่า Title, Legend และ Label ไม่ถูกตัด

เขียนสรุปท้ายงานว่า Layout ที่เลือกช่วยตอบคำถามด้านการผลิต การบำรุงรักษา และคุณภาพอย่างไร
