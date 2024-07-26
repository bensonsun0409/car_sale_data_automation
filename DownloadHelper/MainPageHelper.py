from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


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

            for index, a_element in enumerate(a_elements, 1):
                try:
                    href = a_element.get_attribute('href')
                    location = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[1]')
                    views = a_element.find_element(By.XPATH, './/div/div[2]/div[1]/div[3]/span[3]')

                    print(f"a 元素 {index}:{href}")
                    print(f"  位置: {location.text}")
                    print(f"  瀏覽量: {views.text}")
                    print()
                    car_views.append(views.text)
                    car_locations.append(location.text)
                    car_url.append(href)
                except NoSuchElementException:
                    print(f"無法找到元素 {index} 的某些資訊")

            end_time = time.time()
            download_time = end_time - start_time
            print(f"Download time: {download_time} seconds")
            return car_url, car_locations, car_views
        except Exception as e:
            print(f"發生錯誤: {str(e)}")
            return None
        finally:
            if 'driver' in locals():
                driver.quit()

    @staticmethod
    def scan_all_pages(brand=None, model=None):
        page = 1
        all_car_url, all_car_locations, all_car_views = [], [], []
        start_time = time.time()

        while True:
            try:
                result = StringHelper.get_page_info(page, brand, model)
                if not result or not any(result):
                    print(f"沒有更多頁面，總共掃描了 {page - 1} 頁")
                    break
                car_url, car_locations, car_views = result
                all_car_url.extend(car_url)
                all_car_locations.extend(car_locations)
                all_car_views.extend(car_views)
                page += 1
                time.sleep(1)
            except Exception as e:
                print(f"掃描頁面 {page} 時發生錯誤: {str(e)}")
                break

        end_time = time.time()
        print(f'總共耗時 {end_time - start_time} 秒')

        return all_car_url, all_car_locations, all_car_views