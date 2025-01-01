from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
import logging
class StringHelper:

    @staticmethod
    def get_page_info(page, scrawldate, brand, model):
        start_time = time.time()
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        if model == None:
            url = f'https://auto.8891.com.tw/{brand}?page={page}'
        else:
            url = f'https://auto.8891.com.tw/{brand}/{model}?page={page}'
        try:
            
            driver.get(url)

            # 等待頁面加載
            time.sleep(4)

            a_elements = driver.find_elements(By.XPATH, '//*[@id="items-box"]/a')
            car_views = []
            car_locations = []
            car_url = []
            car_year = []
            car_scrawldate = []
            
            for index, a_element in enumerate(a_elements, 1):
                try:
                    title=a_element.find_element(By.XPATH,".//div/div[2]/div[1]/div[1]/span").text
                    match=re.search(r'\d{4}',title)
                    if(match):
                        year=int(match.group())
                        # logging.info(f"  年式：{year}")
                    else:
                        logging.info("no year data")
                    href = a_element.get_attribute('href')
                    location = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[1]')
                    views = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[3]')
                    car_views.append(views.text[:-3])
                    car_locations.append(location.text)
                    car_url.append(href)
                    car_year.append(year)
                    car_scrawldate.append(scrawldate)
                except NoSuchElementException:
                    logging.info(f"Can't find some information at {index} ")

            end_time = time.time()
            download_time = end_time - start_time
            logging.info(f"Page {page} Download time: {download_time} seconds")
            return car_url, car_locations, car_views, car_year, car_scrawldate
        except Exception as e:
            logging.info(f"Happen error: {str(e)}")
            return None


    @staticmethod
    def scan_all_pages(scrawldate=None, brand=None, model=None):
        page = 1
        all_car_url, all_car_locations, all_car_views, all_year, all_car_scrawldate = [], [], [], [],[]
        start_time = time.time()
    
        while True:
            try:
                result = StringHelper.get_page_info(page, scrawldate, brand, model)
                if not result or not any(result):
                    logging.info(f"no more page, only scan {page - 1} pages")
                    break
                car_url, car_locations, car_views, car_year, car_scrawldate = result
                all_car_url.extend(car_url)
                all_car_locations.extend(car_locations)
                all_car_views.extend(car_views)
                all_year.extend(car_year)
                all_car_scrawldate.extend(car_scrawldate)
                page += 1
                time.sleep(1)
            except Exception as e:
                logging.info(f" Scan {page} page error: {str(e)}")

        end_time = time.time()
        logging.info(f'Total cost {end_time - start_time} second')

        return all_car_url, all_car_locations, all_car_views, all_year, all_car_scrawldate