``` bash
.
├──  Dockerfile
├──  README.md
├──  src
│    ├──  app.py
│    ├──  static
│    │    ├──  css   
│    │    │    ├──  dark-mode.css
│    │    │    ├──  portrait_black.png
│    │    │    └──  styles.css
│    │    ├──  img
│    │    │    ├──  alert_bell.png
│    │    │    ├──  app-store-badge.svg
│    │    │    ├──  bearishengulfing.png
│    │    │    ├──  breakout.png
│    │    │    ├──  bullishengulfing.png
│    │    │    ├──  candlestick.png
│    │    │    ├──  Capture.PNG
│    │    │    ├──  demo-screen.mp4
│    │    │    ├──  divergence.png
│    │    │    ├──  down-arrow.png
│    │    │    ├──  download.png
│    │    │    ├──  falsebreakout.png
│    │    │    ├──  favicon.ico
│    │    │    ├──  google-play-badge.svg
│    │    │    ├──  hangingman.jpg
│    │    │    ├──  Harami.jpg
│    │    │    ├──  line_flex.jpg
│    │    │    ├──  logo.jpg
│    │    │    ├──  Logo_LINE-Account.png
│    │    │    ├──  resistance.jpg
│    │    │    ├──  search-ion.png
│    │    │    ├──  support.jpg
│    │    │    ├──  SupportandResistance.png
│    │    │    ├──  tnw-logo.svg
│    │    │    ├──  tools.png
│    │    │    ├──  tradingview.svg
│    │    │    └──  up-arrow.png  │
│    │    ├──  js       
│    │    │    ├──  bootstrap-maxlength.min.js
│    │    │    ├──  dark-mode-switch.js
│    │    │    ├──  dark-mode-switch.min.js
│    │    │    └──  scripts.js
│    │    └──  flex.json      
│    └──  templates
│         ├──  backtest.html
│         ├──  breakout.html
│         ├──  candlestick.html
│         ├──  Cryptocurrency.html
│         ├──  divergence.html
│         ├──  Federalcurrency.html
│         ├──  guide.html
│         ├──  hello.html
│         ├──  index.html
│         ├──  keylevels.html
│         ├──  payment.html
│         ├──  quiz.html
│         ├──  setting.html
│         ├──  strategy.html
│         └──  trailingstop.html
```


# Header วิธีติดตั้ง
ระบบใช้ Dockerfile สามารถติดตั้งโดยใช้ Dockerfile ได้เลย หรือท่านใดที่ต้องการรันเว็บไซต์ไว้ทดสอบบนเครื่องของตนเองสามารถทำตามขึ้นตอนได้ตั้งนี้
1.──ติดตั้ง python เวอร์ชัน 3.9.10
2.──ติดตั้ง library ของ python 
2.1── pip install Flask gunicorn line_bot_sdk requests Flask-Session Flask-SQLAlchemy sqlalchemy pymysql pg8000 line-bot-sdk pytz backtesting yfinance scipy
3.──เข้าไปแก้ไขไฟล์ app.py เปลี่ยนรหัส *เชื่อมserver เว็บไซต์เข้ากับ ฐานข้อมูล cloud sql ของตนเอง
3.1── USERNAME 
3.2── PASSWORD
3.3── DBNAME
3.4── PROJECT_ID
3.5── INSTANCE_NAME
*แก้ไขค่าเหล่านี้ให้ตรงกับ clound sql ของตนเอง 

4.── รัน server ด้วยคำสั่ง python app.py


วิธีรันผ่าน google cloud server
1.login gmail ผ่านลิ้งค์ https://console.cloud.google.com/
2.สร้าง project ขึ้นมา
![image](https://i.ibb.co/r4H7j31/image.png)

3.ผูกบัตรเครดิต หรือ เดบิต เพื่อรับเหรียญฟรี 300 เหรียญสำหรับเช่า google cloud
![image](https://i.ibb.co/7SKhtf5/image.png)

4.มาเริ่มสร้าง cloud sql กัน เลือกเมนู SQL และกดปุ่ม Create instance
![image](https://i.ibb.co/QNtZBbQ/image.png)
5.เลือก MY SQL

6.ตั้ง instance id เป็น mytradepro และ ตั้ง password ของตัวเอง  
![image](https://i.ibb.co/PTJzXfM/image.png)

7.จากนั้นเข้าถึง mysql ของตนเองโดยเลือกตามชื่อ instance id ที่เราตั้งไว้
8.สร้าง database โดยใช้ชื่อ mytradepro
![image](https://i.ibb.co/p4JJmF6/image.png)
9.เลือกแถบ overview กดปุ่ม OPEN CLOUD SHELL เพื่อเข้าถึง terminal cloud server ของ mysql
![image](https://i.ibb.co/GF69hDt/image.png)
10.ระบบจะพิมรหัสเข้าถึง database ให้ไว้อัตโนมัติ กด enter เพื่อเข้าถึง database


11.พิมคำสั่ง  use mytradepro;
12.สร้าง 2 table ที่เว็บไซต์ต้องใช้โดยพิมพ์ตามนี้
12.1 สร้าง  users table
``` bash
CREATE TABLE users 
(
    id init NOT NULL AUTO_INCREMENT,
    uuid varchar(500) NULL,
    alert1 varchar(500) NULL,
    label1 varchar(500) NULL,
    color1 varchar(500) NULL,
    cryptocurrency1 varchar(500) NULL,
    federalcurrency1 varchar(500) NULL,
    candlestick1 varchar(500) NULL,
    category1 varchar(500) NULL,
    trend1 varchar(500) NULL,
    timeframe1 varchar(500) NULL,

    alert2 varchar(500) NULL,
    label2 varchar(500) NULL,
    color2 varchar(500) NULL,
    cryptocurrency2 varchar(500) NULL,
    federalcurrency2 varchar(500) NULL,
    candlestick2 varchar(500) NULL,
    category2 varchar(500) NULL,
    trend2 varchar(500) NULL,
    timeframe2 varchar(500) NULL,

    alert3 varchar(500) NULL,
    label3 varchar(500) NULL,
    color3 varchar(500) NULL,
    cryptocurrency3 varchar(500) NULL,
    federalcurrency3 varchar(500) NULL,
    candlestick3 varchar(500) NULL,
    category3 varchar(500) NULL,
    trend3 varchar(500) NULL,
    timeframe3 varchar(500) NULL,
    exp TIMESTAMP NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    PRIMARY KEY (id)
);
```

12.2 สร้าง alert table
``` bash
CREATE TABLE alert
(
    id int NOT NULL AUTO_INCREMENT,
    Symbol varchar(500) NULL,
    Timeframe varchar(500) NULL,
    Trend varchar(500) NULL,
    Status varchar(500) NULL,
    TEXT varchar(500) NULL,
    Close FLOAT NULL,
    RSI varchar(500) NULL,
    exp varchar(500) NULL,
    STO varchar(500) NULL,
    ts TIMESTAMP NULL,
    PRIMARY KEY(id)
);
```
13. สร้าง ฐานข้อมูลเตรียมใช้สมบรูณ์ มาเริ่มสร้าง server ของเว็บไซต์กัน
14.มาเริ่มสร้าง server กัน เลือกเมนู Cloud Run และกดปุ่ม create service
![image](https://i.ibb.co/FJM7DWk/image.png)
15.เชื่อม github repository ที่มีไฟล์งานของเรา (อัพไฟล์งานขึ้น github ของเราก่อน) เลือก
![image](https://i.ibb.co/PwsRHLy/image.png)
16.เลือก dir Dockerfile กด save
![image](https://i.ibb.co/rcXCMjc/image.png)
17.เพิ่ม Environment variables ของmysql ด้วย มี 5 ค่าตามรูปภาพ เข้าไป sql เพื่อดูบางค่าที่ต้องใช้
![image](https://i.ibb.co/cxL7srt/image.png)

18.กดปุ่มสร้างได้เลย

19.รอbuild เสร็จ ลิ้งค์เว็บไซต์สามารถเข้าถึงได้ตรงนี้เลย
![image](https://i.ibb.co/dkYwmr3/image.png)
