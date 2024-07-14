# -*- coding: utf-8 -*-
import os
import requests
import zipfile
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def get_car_info(page, driver_path):
    url = f"https://auto.8891.com.tw/?page={page}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    wait = WebDriverWait(driver, 10)

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ib-info-title')))

        car_models = []
        car_prices = []
        car_years = []
        car_kms = []
        car_locations = []
        car_views = []

        info_titles = driver.find_elements(By.CLASS_NAME, 'ib-info-title')
        extra_infos = driver.find_elements(By.CLASS_NAME, 'ib-row.ib-extra')
        info_ims = driver.find_elements(By.CLASS_NAME, 'ib-info-im')

        if not info_titles or not extra_infos or not info_ims:
            print(f"No car information found on page {page}")
            driver.quit()
            return None

        for info_title, extra_info, info_im in zip(info_titles, extra_infos, info_ims):
            try:
                # 抓取車型
                model = info_title.find_element(By.CLASS_NAME, 'ib-it-text').text.strip()
                car_models.append(model)

                # 抓取價格
                price = extra_info.find_element(By.CLASS_NAME, 'ib-price').text.strip()
                car_prices.append(price)

                # 抓取年份（第一個 ib-icon）
                icons = extra_info.find_elements(By.CLASS_NAME, 'ib-icon')
                year = icons[0].text.strip() if len(icons) > 0 else "N/A"
                car_years.append(year)

                # 抓取里程（第二個 ib-icon）
                km = driver.execute_script("return arguments[0].textContent", icons[1]).strip() if len(icons) > 1 else "N/A"
                car_kms.append(km)

                # 抓取車輛位置（第一個 ib-ii-item）
                location_items = info_im.find_elements(By.CLASS_NAME, 'ib-ii-item')
                location = location_items[0].text.strip() if len(location_items) > 0 else "N/A"
                car_locations.append(location)

                # 抓取瀏覽次數（第三個 ib-ii-item）
                views = location_items[2].text.strip() if len(location_items) > 2 else "N/A"
                car_views.append(views)

            except Exception as e:
                print(f"Failed to extract information from an element on page {page}: {str(e)}")

        driver.quit()
        return car_models, car_prices, car_years, car_kms, car_locations, car_views

    except Exception as e:
        print(f"Timeout or error occurred while loading page {page}: {str(e)}")
        driver.quit()
        return None


def crawl_all_pages(driver_path):
    page = 1
    all_car_models, all_car_prices, all_car_years, all_car_kms = [], [], [], []
    all_car_locations, all_car_views = [], []
    start_time = time.time()
    while page < 2:
        result = get_car_info(page, driver_path)
        if not result:
            break
        car_models, car_prices, car_years, car_kms, car_locations, car_views = result
        all_car_models.extend(car_models)
        all_car_prices.extend(car_prices)
        all_car_years.extend(car_years)
        all_car_kms.extend(car_kms)
        all_car_locations.extend(car_locations)
        all_car_views.extend(car_views)
        page += 1
        time.sleep(1)
    end_time = time.time()
    print(f'totall time is {start_time-end_time}')

    return all_car_models, all_car_prices, all_car_years, all_car_kms, all_car_locations, all_car_views


def save_to_csv(car_models, car_prices, car_years, car_kms, car_locations, car_views):
    df = pd.DataFrame({
        'Car Model': car_models,
        'Price': car_prices,
        'Year': car_years,
        'Kilometers': car_kms,
        'Location': car_locations,
        'Views': car_views
    })
    df.to_csv('car_info.csv', index=False, encoding='utf-8-sig')


def main():
    try:
        driver_path = ChromeDriverManager().install()
        all_car_models, all_car_prices, all_car_years, all_car_kms, all_car_locations, all_car_views = crawl_all_pages(driver_path)
        save_to_csv(all_car_models, all_car_prices, all_car_years, all_car_kms, all_car_locations, all_car_views)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
