from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from sqlalchemy import create_engine

driver = webdriver.Chrome()
url = f'https://auto.8891.com.tw/usedauto-infos-3984140.html?display__sale_code=3010013&flow_id=f3431831-a5cb-4e13-b791-862a551556a8'
driver.get(url)
all_equipment = [
    '胎壓偵測', '動態穩定系統', '防盜系統', 'keyless免鑰系統', '循跡系統', '中控鎖', '剎車輔助系統',
    '兒童安全椅固定裝置', 'ABS防鎖死', '安全氣囊', '定速系統', 'LED頭燈', '倒車顯影系統', '衛星導航',
    '多功能方向盤', '倒車雷達', '恆溫空調', '自動停車系統','電動天窗', '真皮/皮革座椅'
]
equipment_list = [
    'keyless免鑰系統', '循跡系統', '中控鎖', '兒童安全椅固定裝置', 'ABS防鎖死', '安全氣囊', '定速系統',
    'LED頭燈', '多功能方向盤', '倒車雷達', '恆溫空調', '電動天窗', '真皮/皮革座椅'
]
equipment_dict = {equipment: 'N' for equipment in all_equipment}
# 創建設備字典，默認所有設備標記為 'N'

car_equip = driver.find_element(By.ID, 'car-equip')
equipments = car_equip.find_elements(By.CLASS_NAME, 'has')
print(equipments)
for e in equipments:
    this_equip=e.text
    if this_equip in equipment_dict:
        equipment_dict[this_equip] = 'Y'
    

df=pd.DataFrame([equipment_dict])

print(df)