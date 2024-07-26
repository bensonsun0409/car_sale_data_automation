from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time


class CarDataScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def scrape_car_data(self, url):
        start_time = time.time()
        self.driver.get(url)

        car_data = {}

        # 提取品牌和車ID
        input_string = self.driver.find_element(By.XPATH, '//*[@id="infos-ab-flag"]/div').text
        match = re.search(r'中古車 > (.*?) > .*?編號：(S\d+)', input_string)
        if match:
            car_data['brand'] = match.group(1)
            car_data['car_id'] = match.group(2)

        # 提取價格
        car_data['price'] = self.driver.find_element(By.ID, 'price').text

        # 提取驗證狀態
        verify = self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/div[3]/ul/li[2]/div[1]').text
        car_data['verify_tag'] = 'Y' if verify != "暫未驗證" else 'N'

        # 提取里程數、年齡和顏色
        car_data['mileage'] = self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[1]/span[1]').text
        car_data['year'] = self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[2]/span[1]').text
        car_data['color'] = self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[3]/span[1]').text

        # 檢查是否有影片
        try:
            self.driver.find_element(By.ID, 'vjs_video_3')
            car_data['video'] = 'Y'
        except:
            car_data['video'] = 'N'

        # 提取詢問人數
        ask = self.driver.find_element(By.XPATH, '//*[@id="new-chat-wrapper"]/div/span').text
        match = re.search(r'\d+', ask)
        car_data['ask_num'] = match.group(0) if match else None

        # 提取車輛位置
        car_data['car_location'] = self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/a/span').text

        # 滾動頁面以加載更多內容
        self.driver.execute_script("window.scrollTo(0, 1000);")

        # 提取賣家信息
        seller = self.driver.find_element(By.ID, 'tpl_show_market_section')
        time.sleep(1)
        seller_text = seller.text.split('\n')
        car_data['seller_info'] = seller_text[0] if seller_text else None

        # 提取車輛設備
        car_equip = self.driver.find_element(By.ID, 'car-equip')
        equipment = car_equip.find_elements(By.CLASS_NAME, 'has')
        car_data['equipment'] = [item.text for item in equipment if item.text]

        end_time = time.time()
        car_data['scrape_time'] = end_time - start_time

        return car_data

    def close(self):
        self.driver.quit()