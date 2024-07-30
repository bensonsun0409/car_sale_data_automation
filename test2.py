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
url = f'https://auto.8891.com.tw/usedauto-infos-3976803.html?display__sale_code=3010013&flow_id=de95bd2f-ab18-4caa-aa5b-dce5773f7ea3'
driver.get(url)

def mixed_chinese_to_arabic(mixed_num):
    num_dict = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '百': 100, '千': 1000, '萬': 10000, '億': 100000000
    }
    
    result = 0
    temp = 0
    num_stack = []

    i = 0
    while i < len(mixed_num):
        if mixed_num[i].isdigit() or mixed_num[i] == '.':
            j = i
            while j < len(mixed_num) and (mixed_num[j].isdigit() or mixed_num[j] == '.'):
                j += 1
            num_stack.append(float(mixed_num[i:j]))
            i = j
        elif mixed_num[i] in num_dict:
            if num_dict[mixed_num[i]] >= 10000:
                temp = sum(num_stack) if num_stack else (temp or 1)
                result += temp * num_dict[mixed_num[i]]
                temp = 0
                num_stack = []
            elif num_dict[mixed_num[i]] >= 10:
                temp = sum(num_stack) if num_stack else (temp or 1)
                result += temp * num_dict[mixed_num[i]]
                temp = 0
                num_stack = []
            else:
                num_stack.append(num_dict[mixed_num[i]])
        i += 1

    if num_stack:
        result += sum(num_stack)
    elif temp:
        result += temp

    return int(result * 1000)  # 將結果轉換為千為單位的整數

# 測試
milage_text = "4.2萬"
test = mixed_chinese_to_arabic(milage_text[:-1])  # 注意這裡去掉了最後一個字符 '萬'
print(test)  # 應該輸出 42000



milage_text= driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[1]/span[1]').text
print(milage_text[:-2])
test=mixed_chinese_to_arabic(milage_text[:-2])

print(test)