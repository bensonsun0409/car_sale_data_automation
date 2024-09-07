from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re

class StringHelper:
    @staticmethod
    def get_page_info(page, brand, model):
        start_time = time.time()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        url = f'https://auto.8891.com.tw/{brand}/{model}?page={page}'

        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url)

            # 等待頁面加載
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search-result"))
            )

            a_elements = driver.find_elements(By.XPATH, '//*[@id="search-result"]/a')
            car_views = []
            car_locations = []
            car_url = []
            car_year = []
            
            for index, a_element in enumerate(a_elements, 1):
                try:
                    title=a_element.find_element(By.XPATH,".//div/div[2]/div[1]/div[1]/span").text
                    match=re.search(r'\d{4}',title)
                    if(match):
                        year=int(match.group())
                        # print(f"  年式：{year}")
                    else:
                        print("no year data")
                    href = a_element.get_attribute('href')
                    location = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[1]')
                    views = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[3]')

                    # print(f"a index: {index}:{href}")
                    # print(f"  location: {location.text}")
                    # print(f"  views: {views.text}")
                    # print(f"  year:{year}")
                    # print()
                    car_views.append(views.text[:-3])
                    car_locations.append(location.text)
                    car_url.append(href)
                    car_year.append(year)
                except NoSuchElementException:
                    print(f"Can't find some information at {index} ")

            end_time = time.time()
            download_time = end_time - start_time
            # print(f"Download time: {download_time} seconds")
            return car_url, car_locations, car_views, car_year
        except Exception as e:
            print(f"Happen error: {str(e)}")
            return None
        finally:
            if 'driver' in locals():
                driver.quit()

    @staticmethod
    def scan_all_pages(brand=None, model=None):
        page = 1
        all_car_url, all_car_locations, all_car_views, all_year = [], [], [],[]
        start_time = time.time()
    
        while True:
            try:
                result = StringHelper.get_page_info(page, brand, model)
                if not result or not any(result):
                    print(f"no more page, only scan {page - 1} pages")
                    break
                car_url, car_locations, car_views, car_year = result
                all_car_url.extend(car_url)
                all_car_locations.extend(car_locations)
                all_car_views.extend(car_views)
                all_year.extend(car_year)
                page += 1
                time.sleep(1)
            except Exception as e:
                print(f" Scan {page} page error: {str(e)}")

        end_time = time.time()
        print(f'Total cost {end_time - start_time} second')

        return all_car_url, all_car_locations, all_car_views, all_year