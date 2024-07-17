from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StringHelper:
    @staticmethod
    def get_page_info(page, brand, model):
        start_time = time.time()
        options = Options()
        options.add_argument('--headless')  # 啟用 Headless 模式
        options.add_argument('--disable-gpu')  # 禁用 GPU 加速，有助於在某些系統上避免錯誤
        url = f'https://auto.8891.com.tw/?page={page}'

        driver = webdriver.Chrome(options=options)

        driver.get(url)
        a_elements = driver.find_elements(By.XPATH, '//*[@id="search-result"]/a')
        car_views = []
        car_locations = []
        car_url = []
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
            car_views.append(views.text)
            car_locations.append(location.text)
            car_url.append(href)

        end_time = time.time()
        download_time = end_time - start_time
        print(f"Download time: {download_time} seconds")
        return car_url, car_locations, car_views

    @staticmethod
    def scan_all_pages(brand=None, model=None):
        page = 1
        all_car_url, all_car_locations, all_car_views = [], [], []
        start_time = time.time()
        while page < 2:
            result = StringHelper.get_page_info(page, brand, model)
            if not result:
                break
            car_url, car_locations, car_views = result
            all_car_url.extend(car_url)
            all_car_locations.extend(car_locations)
            all_car_views.extend(car_views)
            page += 1
            time.sleep(1)
        end_time = time.time()
        print(f'totall time is {start_time - end_time}')

        return all_car_url, all_car_locations, all_car_views

    @staticmethod
    def to_title_case(text):
        return ' '.join(word.capitalize() for word in text.split())