from DownloadHelper.MainPageHelper import StringHelper
from DownloadHelper.CarPageHelper import CarDataScraper
import pandas as pd
from sqlalchemy import create_engine
import traceback
def save_to_csv(car_url, car_locations, car_views,car_data):
    df1 = pd.DataFrame({
        'url': car_url,
        'location': car_locations,
        'views': car_views,
        
    })
    df2 = pd.DataFrame(car_data)
    result = pd.concat([df1, df2], axis=1)
    result.to_csv('car_info2.csv', index=False, encoding='utf-8-sig')

def save_to_sql(df):
    engine = create_engine('mysql+mysqlconnector://root:b03b02019@localhost/car_info')
    try:
        df.to_sql(name='car_data', con=engine, if_exists='append', index=False) 
    except:
        print("sql儲存失敗")
        traceback.print_exc()

# car_data = [
#     {'id':1,'view':10},
#     {'id':2,'view':0},
#     {'id':3,'view':None}
# ]
# mydf=pd.DataFrame(car_data)
# save_to_sql(mydf)
# # 使用StringHelper類的方法
def main():
    helper = StringHelper()
    # 使用反轉字串方法
    all_car_url, all_car_locations, all_car_views = helper.scan_all_pages('audi','a8l')

    # save_to_csv(all_car_url, all_car_locations, all_car_views)
    print(type(all_car_url))
    print(all_car_url)

    # scraper = CarDataScraper()
    
    all_car_data = []

    for url in all_car_url:
        scraper = CarDataScraper()
        car_data = scraper.scrape_car_data(url)
        all_car_data.append(car_data)
        print(f"Processed URL: {url}")
        print(f"Car Data: {car_data}")

        scraper.close()

    print("All car data collected:")
    df1 = pd.DataFrame({
        'url': all_car_url,
        'location': all_car_locations,
        'views': all_car_views,
    })
    df2 = pd.DataFrame(all_car_data)
    result = pd.concat([df1, df2], axis=1)
    # result.to_csv('car_info2.csv', index=False, encoding='utf-8-sig')
    save_to_sql(result)
    
    # for i, car_data in enumerate(all_car_data, 1):
    #     print(f"Car {i}:")
    #     print(car_data)
    #     print("-" * 50)
        

if __name__ == "__main__":
    main()




# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import time
# import pandas as pd
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# from sqlalchemy import create_engine
# import re
# engine = create_engine('mysql+mysqlconnector://root:b03b02019@localhost/car_info')
# start_time = time.time()
# options = Options()
# options.add_argument('--headless')  # 啟用 Headless 模式
# options.add_argument('--disable-gpu')  # 禁用 GPU 加速，有助於在某些系統上避免錯誤
# url = f'https://auto.8891.com.tw/?'



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

# url = f'https://auto.8891.com.tw/usedauto-infos-3976803.html?display__sale_code=3010013&flow_id=de95bd2f-ab18-4caa-aa5b-dce5773f7ea3'
# url2= f'https://sofu.8891.com.tw/onSale/S3980152.html?display__sale_code=3010013&flow_id=e28e5f44-6c30-4305-ac37-3f8bfc6d90cb'
# driver = webdriver.Chrome()
# # driver.maximize_window()
# driver.get(url2)
# # brand = driver.find_element(By.XPATH, '//*[@id="infos-ab-flag"]/div/a[3]').text
# input_string= driver.find_element(By.XPATH, '//*[@id="infos-ab-flag"]/div').text  

# match = re.search(r'中古車 > (.*?) > .*?編號：(S\d+)', input_string)

# if match:
#     brand = match.group(1) #品牌
#     car_id = match.group(2) #車ID
#     print(f"Car Model: {brand}")
#     print(f"Car ID: {car_id}")
# else:
#     print("No match found")


# price=driver.find_element(By.ID,'price').text  #價錢

# try:
#     verify = self.driver.find_element(By.XPATH,
#                                         '//*[@id="main-box"]/div[3]/div[2]/div[3]/ul/li[2]/div[1]').text
#     car_data['verify_tag'] = 'Y' if verify != "暫未驗證" else 'N'
# except NoSuchElementException:
#     car_data['verify_tag'] = "Not found"
# print(price)
# print(verify_tag)
# long=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/ul/li[1]/span[1]').text #里程數
# print(long)
# year=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/ul/li[2]/span[1]').text #年齡
# color=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/ul/li[3]/span[1]').text #顏色

# print(year)
# print(color)
# video=""
# try:
#     driver.find_element(By.ID,'vjs_video_3')
#     video="Y"
# except:
#     video="N"
# print(f'影片看車:{video}')

# ask=driver.find_element(By.XPATH,'//*[@id="new-chat-wrapper"]/div/span').text  #詢問人數
# match=re.search(r'\d+',ask)
# if match:
#     ask_num=match.group(0)
#     print(ask_num)
# else:
#     print("No match found for ask")


# car_detail_location=driver.find_element(By.XPATH,'//*[@id="main-box"]/div[3]/div[2]/a/span').text  #車子所在地
# print(car_detail_location)
# driver.execute_script("window.scrollTo(0, 1000);") #因車行資料須下滑才會load，所以加入這行，如果

# seller=driver.find_element(By.ID,'tpl_show_market_section') #車行所有資料

# time.sleep(1)
# seller_text=seller.text
# lines = seller_text.split('\n')

# # 打印第一行文本内容
# if lines:
#     first_line = lines[0]
#     if first_line=="8891嚴選商家實車 實況 實價":
#         first_line=lines[1]
#     print(f"{first_line}")
# else:
#     print("No text found in the section.")



# car_equip=driver.find_element(By.ID,'car-equip') #在car_equip下找出有裝的設備
# equipment=car_equip.find_elements(By.CLASS_NAME,'has')
# for i in equipment:
#     if i==0:
#         continue
#     print(i.text)
# end_time=time.time()
# print(f'{end_time-start_time}s')

