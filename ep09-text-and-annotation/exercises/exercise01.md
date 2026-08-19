# แบบฝึกหัด EP9 — Text and Annotation for Solar Power Operations

แบบฝึกหัดนี้ใช้ข้อมูลสังเคราะห์เพื่อฝึกวางข้อความและ Annotation บนกราฟ Solar Farm ค่า Reference, Event และ Threshold ทั้งหมดมีไว้สำหรับการเรียน Matplotlib ไม่ใช่เกณฑ์ควบคุมโรงไฟฟ้าหรืออุปกรณ์ไฟฟ้าจริง

## ส่วนที่ 1: Title, Label และหน่วย

สร้างกราฟ AC Power หนึ่งวัน โดยต้องมี:

- ชื่อกราฟที่บอก Site และช่วงเวลา
- ชื่อแกน X พร้อมระบุ Local Time หรือ UTC
- ชื่อแกน Y พร้อมหน่วย kW
- Grid ที่ไม่เด่นกว่าเส้นข้อมูล
- Figure Size ที่อ่าน Label ได้ครบ

อธิบายว่าชื่อกราฟและชื่อแกนต่างจาก Annotation ของเหตุการณ์อย่างไร

## ส่วนที่ 2: `ax.text()` และ Alignment

เลือกจุดข้อมูลหนึ่งจุด แล้ววางข้อความตำแหน่งเดียวกันด้วย:

- `ha="left"`
- `ha="center"`
- `ha="right"`
- `va="top"`
- `va="bottom"`

เพิ่ม Marker ที่จุดยึดเพื่อสังเกตว่าขอบหรือกึ่งกลางส่วนใดของข้อความตรงกับพิกัด

## ส่วนที่ 3: Style Dictionary

สร้าง Dictionary ชื่อ `event_text_style` ซึ่งมี:

- `fontsize`
- `color`
- `fontweight`
- `bbox`

ใช้ `**event_text_style` กับข้อความอย่างน้อยสามรายการ ห้ามเขียน Property ชุดเดิมซ้ำทุกคำสั่ง

## ส่วนที่ 4: Data, Axes และ Figure Coordinates

วางข้อความสามรายการ:

1. ชื่อเหตุการณ์ที่จุดข้อมูลด้วย `ax.transData`
2. Plant ID ที่มุมซ้ายบนด้วย `ax.transAxes`
3. หมายเหตุแหล่งข้อมูลด้วย `fig.text()`

เปลี่ยน `xlim` จากเต็มวันเป็นช่วง 11:00–15:00 แล้วบันทึกว่าข้อความใดขยับตามข้อมูลและข้อความใดอยู่ตำแหน่งเดิม

## ส่วนที่ 5: Annotation พื้นฐาน

คำนวณ Peak Power ด้วย `argmax()` แล้วเพิ่ม:

- Marker ที่จุด Peak
- ข้อความแสดงเวลา
- ข้อความแสดงกำลังผลิตพร้อมหน่วย kW
- ลูกศรจากข้อความไปยังจุด Peak

ห้าม Hard-code ค่า X และ Y ของ Peak

## ส่วนที่ 6: `offset points`

สร้าง Annotation ของเหตุการณ์เดียวกันสามแบบ โดยใช้ Offset:

- `(20, 30)`
- `(-40, 35)`
- `(0, -55)`

เปรียบเทียบว่า Offset แบบใดหลบเส้นและขอบ Figure ได้ดีที่สุดเมื่อเปลี่ยน Figure Size

## ส่วนที่ 7: `bbox` และ `arrowprops`

ทดลองกล่องข้อความอย่างน้อยสามแบบ และลูกศรอย่างน้อยสามแบบ จากนั้นเลือก Combination หนึ่งแบบสำหรับรายงานจริง

อธิบายเหตุผลโดยพิจารณา:

- Contrast
- ความสม่ำเสมอ
- ความชัดเมื่อย่อภาพ
- การแยก Weather Event ออกจาก Maintenance Event

## ส่วนที่ 8: Annotation จาก List และ Loop

สร้าง List ของ Dictionary สำหรับเหตุการณ์อย่างน้อยสี่รายการ แต่ละรายการต้องมี:

- เวลา
- Label
- สี
- Offset

ใช้ Loop วาง Annotation ทั้งหมด ห้าม Copy-paste `ax.annotate()` สี่ครั้ง

## ส่วนที่ 9: Blended Transform

วาดเส้น Reference แนวนอน แล้ววางชื่อเส้นใกล้ขอบขวาของ Axes ด้วย `ax.get_yaxis_transform()`

ทดลองเปลี่ยน `xlim` และ `ylim` แล้วตอบว่า:

1. เหตุใดตำแหน่ง X จึงยังอยู่ใกล้ขอบขวา
2. เหตุใดตำแหน่ง Y จึงตามค่าจริงของ Reference
3. กรณีนี้ต่างจาก `ax.transAxes` ทั้งสองแกนอย่างไร

## ส่วนที่ 10: Function ที่ใช้ซ้ำ

เขียน Function ชื่อ `annotate_nearest()` ซึ่งรับ:

- Axes
- Array ของ X
- Array ของ Y
- เวลาเหตุการณ์
- Label
- Offset
- สี

Function ต้องหาจุดที่ใกล้เวลาเหตุการณ์ที่สุด สร้าง Annotation และคืน Annotation Object

ทดสอบการเปลี่ยน Font Size และ Visibility ผ่าน Object ที่คืนมา

## ส่วนที่ 11: Multiple Subplots

สร้าง Dashboard สองแถวด้วย `sharex=True`:

- แถวบน: AC Power และ Clear-sky Reference
- แถวล่าง: Ambient Temperature และ Inverter Temperature

เพิ่ม:

- `fig.suptitle()` หนึ่งรายการ
- ชื่อเฉพาะของแต่ละ Axes
- Annotation ของ Peak Power
- Annotation ของ Peak Temperature
- `fig.text()` สำหรับระบุว่าเป็นข้อมูลสังเคราะห์

อธิบายว่า Annotation แต่ละรายการต้องเรียกผ่าน Axes ใด

## ส่วนที่ 12: ตรวจความถูกต้องของเหตุการณ์

สมมติว่าพบกำลังผลิตลดลงช่วง 15:00 แต่ไม่มี Weather Log หรือ Equipment Event ยืนยัน

สร้าง Annotation สองเวอร์ชัน:

- เวอร์ชันที่สรุปสาเหตุเกินข้อมูล
- เวอร์ชันที่รายงานเฉพาะสิ่งที่ตรวจพบ

อธิบายว่าเหตุใดข้อความลักษณะ `Power drop under investigation` จึงเหมาะกว่าการระบุว่าอุปกรณ์เสียเมื่อยังไม่มีหลักฐาน

## โจทย์ท้าทาย: Solar Farm Daily Operations Report

สร้าง Figure สำหรับรายงานหนึ่งวัน โดยมีอย่างน้อยสาม Axes:

- AC Power เทียบ Clear-sky Reference
- Irradiance
- Ambient และ Inverter Temperature

ข้อกำหนดเพิ่มเติม:

- Annotation ของ Peak Power และ Peak Temperature คำนวณจากข้อมูล
- ช่วงสีแสดง Inspection Window
- Event Annotation อย่างน้อยสามรายการจาก List
- ใช้ Data, Axes, Figure และ Blended Coordinates อย่างน้อยชนิดละหนึ่งครั้ง
- Plant ID, วันที่, Timezone และ Data Source
- หน่วยบนทุกแกนและ Annotation ที่มีตัวเลข
- สีและ Arrow Style สอดคล้องตามประเภทเหตุการณ์
- ไม่มีข้อความซ้อนกันเมื่อ Export ที่ 1280×720 และ 1920×1080
- มีหมายเหตุว่าข้อมูลเป็นข้อมูลสังเคราะห์

เขียนสรุปท้ายงานหนึ่งย่อหน้าว่า Annotation ใดช่วยตอบคำถามด้านการผลิต สภาพอากาศ และการบำรุงรักษา และ Annotation ใดควรถูกตัดออกเพื่อลดความแน่นของกราฟ
