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
import re
engine = create_engine('mysql+mysqlconnector://root:b03b02019@localhost/car_info')
start_time = time.time()
options = Options()
options.add_argument('--headless')  # 啟用 Headless 模式
options.add_argument('--disable-gpu')  # 禁用 GPU 加速，有助於在某些系統上避免錯誤
url = f'https://auto.8891.com.tw/?'

# driver = webdriver.Chrome(options=options)

# driver.get(url)
# a_elements = driver.find_elements(By.XPATH, '//*[@id="search-result"]/a')
# car_views = []
# car_locations = []
# car_url = []
# car_id = []
# id=1
# # 遍歷每個 a 元素
# for index, a_element in enumerate(a_elements, 1):
#     href = a_element.get_attribute('href')
#     # 在每個 a 元素內部查找所需的 span 元素
#     location = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[1]')
#     views = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[3]')
#     match = re.search(r'\d+',views.text)
    
#     if(match):
#         number=int(match.group())
#     # 輸出結果
#     print(f"a 元素 {index}:{href}")
#     print(f"  位置: {location.text}")
#     print(f"  瀏覽量: {number}")
#     print()
#     car_id.append(id)
#     car_views.append(number)
#     car_locations.append(location.text)
#     car_url.append(href)
#     id=id+1
#     df = pd.DataFrame({
#     'id': car_id,
#     'url': car_url,
#     'location': car_locations,
#     'view':car_views
# })


    
# df.to_sql(name='car_data', con=engine, if_exists='append', index=False)    


# end_time = time.time()
# download_time = end_time - start_time
# print(f"df")

url = f'https://auto.8891.com.tw/usedauto-infos-3986368.html?display__sale_code=3010013&flow_id=4be8b760-49cc-4e7c-baef-76f9ab2a8124'
driver = webdriver.Chrome(options=options)
driver.get(url)
# brand = driver.find_element(By.XPATH, '//*[@id="infos-ab-flag"]/div/a[3]').text
input_string= driver.find_element(By.XPATH, '//*[@id="infos-ab-flag"]/div').text

match = re.search(r'中古車 > (.*?) > .*?編號：(S\d+)', input_string)

if match:
    brand = match.group(1)
    car_id = match.group(2)
    print(f"Car Model: {brand}")
    print(f"Car ID: {car_id}")
else:
    print("No match found")


price=driver.find_element(By.ID,'price').text
verify=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/div[3]/ul/li[2]/div[1]').text
if verify=="暫未驗證":
    verify_tag="N"
else:
    verify_tag="Y"
print(price)
print(verify_tag)
long=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/ul/li[1]/span[1]').text
print(long)
year=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/ul/li[2]/span[1]').text
color=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/ul/li[3]/span[1]').text
print(year)
print(color)


ask=driver.find_element(By.XPATH,'//*[@id="new-chat-wrapper"]/div/span').text
match=re.search(r'\d+',ask)
if match:
    ask_num=match.group(0)
    print(ask_num)
else:
    print("No match found for ask")


car_detail_location=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/a/span').text
print(car_detail_location)

equipment=driver.find_elements(By.CLASS_NAME,'has')
for i in equipment:
    
    print(i.text)