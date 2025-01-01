執行介紹：
使用google遠端桌面連線projectscrawling@gmail.com
帳號密碼見line

目前設定每兩天執行一次爬蟲，因為爬完一次所有車款要一天又2~3小時
程式資料夾放在桌面的ScrawlProgram
執行爬蟲程式指令cmd為runcode.cmd
每次爬蟲時會紀錄資料在script_execution.log
並且記錄該車款的總爬蟲車數在crawldata.txt
這兩個檔案都在預設的C:\Windows\System32  沒有特別設定
現在採用的是利用捷徑去讀取這兩個檔案
debug可以透過這兩個log去分析
另外有安裝MySQL Workbench，帳號密碼同見Line
可以直接在Workbench root上直接查詢資料庫內的資料

網頁則要先打開app.exe為local端網頁的後端
打開後點擊8891分析網站就可以開啟分析頁面

-----
source code
爬蟲程式主程式為get_searchpage_info.py
分別取得DownloadHelper中的MainPageHelper.py和CarPageHelper.py的執行結果進行注入進SQL
MainPageHelper.py功能為爬取選定品牌或車款的所有頁面，取的列表上的資料，並存爬過的每一台車網址，回傳一個dataframe
CarPageHelper.py則透過這些網址一個個進入取得詳細資料，回傳一個dataframe
將兩個dataframe concat成一個表格後傳入sql，為了保證效率但又不會記憶體過載，目前是每500筆儲存一次資料
run_code.cmd則是執行爬蟲程式的cmd指令，可以透過這個為參數給get_searchpage_info.py，指定特定品牌和車款

商家的部分
主程式在car_store_test.py，內程式自行trace到DownloadHelper

啟動虛擬環境
.venv\Scripts\activate
每次pull下來之後若有新的library則使用下方指令
pip install -r requirements.txt

若自己有更新library則要進行更新requirements.txt
pip freeze > requirements.txt

mysql 安裝
https://downloads.mysql.com/archives/installer/

安裝後建立一個server  localhost:3306
id=root
密碼暫定=b03b02019

進入這個server後建立schema 名為car_info
在裡面建立table名為car_data
column 資料如下

id int AI PK 
url varchar(200) 
location varchar(45) 
views int 
year varchar(45) 
color varchar(45) 
milage int 
price varchar(45) 
video varchar(45) 
ask_num varchar(45) 
car_location varchar(45) 
seller_info varchar(45) 
brand varchar(45) 
model varchar(45) 
car_id varchar(45) 
product_year varchar(45) 
verify_tag varchar(45) 
scrawldate date
胎壓偵測 varchar(45) 
動態穩定系統 varchar(45) 
防盜系統 varchar(45) 
keyless免鑰系統 varchar(45) 
循跡系統 varchar(45) 
中控鎖 varchar(45) 
剎車輔助系統 varchar(45) 
兒童安全椅固定裝置 varchar(45) 
ABS防鎖死 varchar(45) 
安全氣囊 varchar(45) 
定速系統 varchar(45) 
LED頭燈 varchar(45) 
倒車顯影系統 varchar(45) 
衛星導航 varchar(45) 
多功能方向盤 varchar(45) 
倒車雷達 varchar(45) 
恆溫空調 varchar(45) 
自動停車系統 varchar(45) 
電動天窗 varchar(45) 
真皮/皮革座椅 varchar(45) 


另一table名為car_seller
id int AI PK 
title varchar(45) 
rating int 
rating_count int 
link varchar(100) 
in_stock int 
in_store int 
view_count int 
transaction_record int 
address varchar(45) 
scrawldate date 
location varchar(45)

package網站指令
1.在frontend 進行npm run build
2.將生成的靜態資料夾front-app/build覆蓋
3.後端輸入指令pip freeze > requirements.txt 確認沒有新增新的相關
pyinstaller --onefile --add-data "front-app/build;build" --add-data "fonts;fonts"  app.py

打包爬蟲程式
pyinstaller --onefile --noconsole your_script.py(替代成要打包的程式)
