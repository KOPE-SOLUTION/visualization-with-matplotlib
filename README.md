# Visualization with Matplotlib

หลักสูตรภาษาไทยสำหรับเรียนรู้การสร้างภาพข้อมูลด้วย Python, NumPy และ Matplotlib ตั้งแต่กราฟพื้นฐานไปจนถึงการออกแบบ Figure สำหรับการวิเคราะห์และการสื่อสารข้อมูล

เนื้อหาใน Repository นี้ใช้ประกอบวิดีโอบน YouTube แต่ละตอนมีบทอธิบาย ตัวอย่างโค้ด และกรณีศึกษาจากงานหลายสาขา เช่น IoT อาคารอัจฉริยะ การผลิต พลังงานแสงอาทิตย์ และระบบ Cold Chain

[ดูเพลย์ลิสต์ Visualization with Matplotlib บน YouTube](https://www.youtube.com/playlist?list=PLea-bfI_jPIA)

## เกี่ยวกับหลักสูตร

หลักสูตรออกแบบให้เรียนตามลำดับได้โดยไม่จำเป็นต้องมีพื้นฐานด้าน Data Visualization มาก่อน เนื้อหาเน้นการทำความเข้าใจว่า Matplotlib สร้างกราฟอย่างไร ควบคู่กับการทดลองปรับโค้ดและอ่านผลลัพธ์ด้วยตนเอง

เหมาะสำหรับ:

- ผู้ที่มีพื้นฐาน Python และต้องการเริ่มสร้างกราฟ
- นักเรียน นักศึกษา และผู้เริ่มต้นด้าน Data Science
- นักวิเคราะห์ข้อมูลและวิศวกรข้อมูล
- นักพัฒนา IoT และระบบสมองกลฝังตัว
- วิศวกรที่ต้องจัดทำกราฟ รายงาน หรือ Dashboard จากข้อมูลหน้างาน

## เนื้อหาที่เผยแพร่แล้ว

| ตอน | บทเรียน | กรณีศึกษาและทักษะหลัก |
|:---:|---|---|
| EP1 | [Introduction to Matplotlib and Your First Line Plot](./ep01-introduction-to-matplotlib/README.md) | โครงสร้าง Figure, Axes และกราฟเส้นแรก |
| EP2 | [Simple Scatter Plots](./ep02-simple-scatter-plots/README.md) | ความสัมพันธ์ของข้อมูลด้วยกราฟกระจาย |
| EP3 | [Visualizing Errors](./ep03-visualizing-errors/README.md) | การแสดงความไม่แน่นอนและ Error Bar |
| EP4 | [Density and Contour Plots for IoT Sensor Data](./ep04-density-and-contour-plots/README.md) | Contour Plot และข้อมูลเซนเซอร์ IoT |
| EP5 | [Histograms, Binning, and Density for IoT Sensor Data](./ep05-histograms-binning-density/README.md) | Histogram, Bin และการกระจายของข้อมูล |
| EP6 | [Customizing Plot Legends for Smart Farm Data](./ep06-customizing-plot-legends/README.md) | การออกแบบ Legend สำหรับข้อมูล Smart Farm |
| EP7 | [Customizing Colorbars for Smart Building IoT Data](./ep07-customizing-colorbars/README.md) | Colormap, Normalization และ Colorbar |
| EP8 | [Multiple Subplots for Manufacturing Production Monitoring](./ep08-multiple-subplots/README.md) | Subplots, GridSpec และ Dashboard การผลิต |
| EP9 | [Text and Annotation for Solar Power Plant Operations](./ep09-text-and-annotation/README.md) | Text, Annotation และระบบพิกัดของ Matplotlib |
| EP10 | [Customizing Ticks for Cold-Chain Logistics Monitoring](./ep10-customizing-ticks/README.md) | Major Tick, Minor Tick, Locator และ Formatter |

## หัวข้อที่วางแผนไว้

| ตอน | หัวข้อ |
|:---:|---|
| EP11 | Matplotlib Configurations and Styles |
| EP12 | Three-Dimensional Plotting with Matplotlib |
| EP13 | Geographic Data Visualization |
| EP14 | Data Visualization with Seaborn |
| EP15 | Visualization Mini Project |

ปัจจุบันเนื้อหาเผยแพร่ถึง EP10 ส่วนชื่อและลำดับของบทถัดไปอาจปรับเปลี่ยนระหว่างการพัฒนา

## สิ่งที่ต้องเตรียม

- Python 3
- NumPy
- Matplotlib
- โปรแกรมเขียนโค้ดหรือ Notebook ที่ถนัด เช่น VS Code หรือ Jupyter Notebook

ติดตั้งไลบรารีหลักด้วยคำสั่ง:

~~~bash
python -m pip install numpy matplotlib
~~~

บางบทอาจใช้ Pandas, Seaborn หรือไลบรารีเสริม โดยจะระบุไว้ใน README ของบทนั้น

## วิธีเรียนจาก Repository นี้

1. เลือกบทจากตารางเนื้อหาที่เผยแพร่แล้ว
2. อ่าน README ของบทเพื่อทำความเข้าใจแนวคิดและลำดับการทดลอง
3. เปิดไฟล์ในโฟลเดอร์ `source-code` แล้วรันทีละตัวอย่าง
4. เปลี่ยนค่า Parameter และเปรียบเทียบผลลัพธ์ด้วยตนเอง
5. ทำโจทย์ในโฟลเดอร์ `exercises` หากบทนั้นมีแบบฝึกหัด

แนะนำให้เรียนตามลำดับตั้งแต่ EP1 เพราะเนื้อหาในตอนหลังจะนำแนวคิดเรื่อง Figure, Axes, NumPy Array และ Object-oriented API จากตอนก่อนหน้ามาใช้ต่อ

## โครงสร้าง Repository

~~~text
visualization-with-matplotlib/
├── README.md
├── assets/
│   └── thumbnails/
├── ep01-introduction-to-matplotlib/
├── ep02-simple-scatter-plots/
├── ...
└── ep10-customizing-ticks/
~~~

โครงสร้างภายในแต่ละบทโดยทั่วไปเป็นดังนี้:

~~~text
epXX-topic/
├── README.md
├── source-code/
└── exercises/       # มีในบทที่จัดเตรียมแบบฝึกหัดไว้
~~~

- `README.md` อธิบายแนวคิดและลำดับการทดลอง
- `source-code` เก็บสคริปต์หรือ Notebook ที่ใช้ในบทเรียน
- `exercises` เก็บโจทย์สำหรับฝึกเพิ่มเติม
- `assets` เก็บภาพประกอบหรือไฟล์ที่ใช้ร่วมกับเอกสาร

## ผลลัพธ์การเรียนรู้

เมื่อเรียนตามลำดับ ผู้เรียนจะสามารถ:

- สร้างและปรับแต่งกราฟด้วย Matplotlib Object-oriented API
- ใช้ NumPy เตรียมข้อมูลสำหรับการสร้างภาพ
- เลือกชนิดกราฟให้เหมาะกับคำถามและลักษณะข้อมูล
- ออกแบบ Label, Legend, Colorbar, Tick และ Annotation ให้อ่านง่าย
- จัดวางหลาย Axes ภายใน Figure เดียว
- สร้างกราฟสำหรับการสำรวจข้อมูล รายงาน และ Dashboard

## หมายเหตุเกี่ยวกับข้อมูลตัวอย่าง

ข้อมูลและเหตุการณ์จำลองในหลักสูตรสร้างขึ้นเพื่อการเรียนรู้ ไม่ใช่ข้อมูลจากสถานประกอบการจริง และไม่ควรนำค่าจากตัวอย่างไปใช้เป็นเกณฑ์ตัดสินใจด้านวิศวกรรม ความปลอดภัย หรือการควบคุมกระบวนการ

## การใช้งานเนื้อหา

Repository นี้จัดทำเพื่อการศึกษา ตัวอย่างโค้ด แบบฝึกหัด รูปภาพ และคำอธิบายได้รับการพัฒนาสำหรับหลักสูตร Visualization with Matplotlib ของ KOPE SOLUTION
