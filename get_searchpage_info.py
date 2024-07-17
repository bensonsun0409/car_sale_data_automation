import time
import requests
import concurrent.futures 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed 
# 開啟瀏覽器視窗(Chrome)
# 方法一：執行前需開啟chromedriver.exe且與執行檔在同一個工作目錄
start_time = time.time()
options = Options()
options.add_argument('--headless')  # 啟用 Headless 模式
options.add_argument('--disable-gpu')  # 禁用 GPU 加速，有助於在某些系統上避免錯誤
url = 'https://auto.8891.com.tw/?'

driver = webdriver.Chrome(options=options)

driver.get(url)
a_elements = driver.find_elements(By.XPATH, '//*[@id="search-result"]/a')
print(a_elements)
# 遍歷每個 a 元素
for index, a_element in enumerate(a_elements, 1):
    href = a_element.get_attribute('href')
    # 在每個 a 元素內部查找所需的 span 元素
    location = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[1]')
    views = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[3]')

    # 輸出結果
    print(f"a 元素 {index}:{href}")
    print(f"  位置: {location.text}")
    print(f"  瀏覽量: {views.text}")
    print()

end_time = time.time()
download_time = end_time - start_time
print(f"Download time: {download_time} seconds")