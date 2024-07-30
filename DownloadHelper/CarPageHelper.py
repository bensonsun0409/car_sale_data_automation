from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import time
import json

class CarDataScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    @staticmethod
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

        return int(result * 10000) 
    
    def scrape_car_data(self, url):
        try:
            start_time = time.time()
            self.driver.get(url)

            # 等待頁面加載
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "main-box"))
            )

            car_data = {}

            # 提取品牌和車ID
            try:
                input_string = self.driver.find_element(By.XPATH, '//*[@id="infos-ab-flag"]/div').text
                match = re.search(r'中古車 > (.*?) > .*?編號：(S\d+)', input_string)
                if match:
                    car_data['brand'] = match.group(1)
                    car_data['car_id'] = match.group(2)
            except NoSuchElementException:
                car_data['brand'] = None
                car_data['car_id'] = None

            # 提取價格
            try:
                car_data['price'] = self.driver.find_element(By.ID, 'price').text
            except NoSuchElementException:
                car_data['price'] = None

            # 提取驗證狀態
            try:
                verify = self.driver.find_element(By.XPATH,
                                                  '//*[@id="main-box"]/div[3]/div[2]/div[3]/ul/li[2]/div[1]').text
                car_data['verify_tag'] = 'Y' if verify != "暫未驗證" else 'N'
            except NoSuchElementException:
                car_data['verify_tag'] = None

            # 提取里程數
            try:
                milage_text= self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[1]/span[1]').text
                car_data['milage']=self.mixed_chinese_to_arabic(milage_text[:-2])
            except NoSuchElementException:
                car_data['milage'] = None

            #提取年齡
            try:
                car_data['year'] = self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[2]/span[1]').text
            except NoSuchElementException:
                car_data['year'] = None    

            #提取顏色
            try:
                car_data['color'] = self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[3]/span[1]').text
            except NoSuchElementException:
                car_data['color'] = None    



            # 檢查是否有影片
            try:
                self.driver.find_element(By.ID, 'vjs_video_3')
                car_data['video'] = 'Y'
            except NoSuchElementException:
                car_data['video'] = 'N'

            # 提取詢問人數
            try:
                ask = self.driver.find_element(By.XPATH, '//*[@id="new-chat-wrapper"]/div/span').text
                match = re.search(r'\d+', ask)
                car_data['ask_num'] = match.group(0) if match else None
            except NoSuchElementException:
                car_data['ask_num'] = None

            # 提取車輛位置
            try:
                location= self.driver.find_element(By.XPATH,
                                                                    '//*[@id="main-box"]/div[3]/div[2]/a/span').text
                car_data['car_location'] = location[0:6]
                #取前六字
            except NoSuchElementException:
                car_data['car_location'] = None

            # 滾動頁面以加載更多內容
            self.driver.execute_script("window.scrollTo(0, 1000);")

            # 提取賣家信息
            try:
                seller = self.driver.find_element(By.ID, 'tpl_show_market_section')
                time.sleep(1)
                seller_text = seller.text.split('\n')
                if seller_text:
                    if seller_text[0] == "8891嚴選商家實車 實況 實價":
                        car_data['seller_info'] = seller_text[1]
                    else:
                        car_data['seller_info'] = seller_text[0]
            except NoSuchElementException:
                car_data['seller_info'] = None

            # 提取車輛設備
            try:
                car_equip = self.driver.find_element(By.ID, 'car-equip')
                equipment = car_equip.find_elements(By.CLASS_NAME, 'has')
                car_data['equipment'] = [item.text for item in equipment if item.text]
            except NoSuchElementException:
                car_data['equipment'] = None

            end_time = time.time()
            # car_data['scrape_time'] = end_time - start_time

            return car_data

        except TimeoutException:
            print(f"Timeout loading page: {url}")
            return None
        except Exception as e:
            print(f"Error scraping data from {url}: {str(e)}")
            return None

    def close(self):
        self.driver.quit()