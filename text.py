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

def get_chrome_version():
    """Get the version of the installed Chrome browser."""
    try:
        output = subprocess.check_output(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            stderr=subprocess.STDOUT, text=True)
        version = output.strip().split()[-1]
        return version
    except subprocess.CalledProcessError:
        raise Exception("Could not find Chrome version. Make sure Chrome is installed.")


def get_chromedriver_version(driver_path):
    """Get the version of the installed ChromeDriver."""
    try:
        output = subprocess.check_output([driver_path, '--version'], stderr=subprocess.STDOUT, text=True)
        version = output.split()[1]
        return version
    except subprocess.CalledProcessError:
        raise Exception("Could not find ChromeDriver version. Make sure ChromeDriver is installed.")


def download_chromedriver(version):
    """Download the ChromeDriver for the specified Chrome version."""
    base_url = "https://chromedriver.storage.googleapis.com/"

    # 嘗試不同的 ChromeDriver 版本
    versions_to_try = [
        version,
        '.'.join(version.split('.')[:3]),  # 主要版本號 (例如 126.0.6478)
        '.'.join(version.split('.')[:2])  # 次要版本號 (例如 126.0)
    ]

    for v in versions_to_try:
        url = f"{base_url}LATEST_RELEASE_{v}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            driver_version = response.text.strip()

            download_url = f"{base_url}{driver_version}/chromedriver_win32.zip"
            response = requests.get(download_url)
            response.raise_for_status()

            zip_path = "chromedriver.zip"
            with open(zip_path, "wb") as file:
                file.write(response.content)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(".")

            os.remove(zip_path)
            print(f"Successfully downloaded ChromeDriver version {driver_version}")
            return
        except requests.RequestException:
            print(f"Failed to download ChromeDriver for version {v}")

    raise Exception("Failed to download ChromeDriver for all attempted versions")


def check_and_update_chromedriver():
    chrome_version = get_chrome_version()
    driver_path = "./chromedriver.exe"
    driver_version = None

    if os.path.exists(driver_path):
        driver_version = get_chromedriver_version(driver_path)

    if driver_version != chrome_version:
        print(f"Updating ChromeDriver from version {driver_version} to {chrome_version}")
        if os.path.exists(driver_path):
            os.remove(driver_path)
        download_chromedriver(chrome_version)
    else:
        print(f"ChromeDriver is up to date with version {chrome_version}")


def get_car_models(page, driver_path):
    url = f"https://auto.8891.com.tw/?page={page}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # driver_path = "./chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    # 使用 WebDriverWait 來等待元素加載
    wait = WebDriverWait(driver, 10)

    try:
        # 等待至少一個 ib-info-title 元素出現
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ib-info-title')))

        car_models = []
        info_titles = driver.find_elements(By.CLASS_NAME, 'ib-info-title')

        if not info_titles:
            print(f"No car models found on page {page}")
            driver.quit()
            return None

        for info_title in info_titles:
            try:
                model = info_title.find_element(By.CLASS_NAME, 'ib-it-text').text.strip()
                car_models.append(model)
            except:
                print(f"Failed to extract model from an ib-info-title element on page {page}")

        driver.quit()
        return car_models

    except:
        print(f"Timeout or error occurred while loading page {page}")
        driver.quit()
        return None


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

        info_titles = driver.find_elements(By.CLASS_NAME, 'ib-info-title')
        extra_infos = driver.find_elements(By.CLASS_NAME, 'ib-row.ib-extra')

        if not info_titles or not extra_infos:
            print(f"No car information found on page {page}")
            driver.quit()
            return None

        for info_title, extra_info in zip(info_titles, extra_infos):
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
                km2 = icons[1].text
                print(f'here {km}')
                car_kms.append(km)


            except Exception as e:
                print(f"Failed to extract information from an element on page {page}: {str(e)}")

        driver.quit()
        return car_models, car_prices, car_years, car_kms

    except Exception as e:
        print(f"Timeout or error occurred while loading page {page}: {str(e)}")
        driver.quit()
        return None


def get_car_info2(page, driver_path):
    url = f"https://auto.8891.com.tw/?page={page}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")


    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    wait = WebDriverWait(driver, 20)

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ib-row.ib-extra')))

        car_models = []
        car_prices = []
        car_years = []
        car_kms = []

        car_items = driver.find_elements(By.CSS_SELECTOR, '.item-block')

        for item in car_items:
            try:
                # 抓取車型
                model = item.find_element(By.CSS_SELECTOR, '.ib-info-title .ib-it-text').text.strip()
                car_models.append(model)

                # 抓取價格
                price = item.find_element(By.CSS_SELECTOR, '.ib-row.ib-extra .ib-price b').text.strip()
                car_prices.append(price)

                # 抓取年份（第一個 ib-icon）
                year = item.find_element(By.CSS_SELECTOR, '.ib-row.ib-extra .ib-icon:nth-child(2) b').text.strip()
                car_years.append(year)

                # 抓取里程（第二個 ib-icon）
                km = item.find_element(By.CSS_SELECTOR, '.ib-row.ib-extra .ib-icon:nth-child(3) b').text.strip()
                car_kms.append(km)

                print(f"Extracted: Model={model}, Price={price}, Year={year}, KM={km}")

            except NoSuchElementException as e:
                print(f"Failed to extract information from an element: {str(e)}")

        driver.quit()
        return car_models, car_prices, car_years, car_kms

    except TimeoutException as e:
        print(f"Timeout occurred while loading page {page}: {str(e)}")
        driver.quit()
        return None
    except Exception as e:
        print(f"An error occurred while processing page {page}: {str(e)}")
        driver.quit()
        return None

def crawl_all_pages(driver_path):
    page = 1
    all_car_models = []
    print(f'start to browse web')
    while page == 1:

        car_models = get_car_models(page, driver_path)
        print(f'car_models is {car_models}')
        if not car_models:
            break
        all_car_models.extend(car_models)
        page += 1
        time.sleep(1)

    return all_car_models


def crawl_all_pages2(driver_path):
    page = 1
    all_car_models = []
    all_car_prices = []
    all_car_years = []
    all_car_kms = []
    while page == 1:
        result = get_car_info(page, driver_path)
        if not result:
            break
        car_models, car_prices, car_years, car_kms = result
        all_car_models.extend(car_models)
        all_car_prices.extend(car_prices)
        all_car_years.extend(car_years)
        all_car_kms.extend(car_kms)
        page += 1
        time.sleep(1)

    return all_car_models, all_car_prices, all_car_years, all_car_kms


def save_to_csv(car_models):
    df = pd.DataFrame(car_models, columns=['Car Model'])
    df.to_csv('car_models.csv', index=False)


def save_to_csv2(car_models, car_prices, car_years, car_kms):
    df = pd.DataFrame({
        'Car Model': car_models,
        'Price': car_prices,
        'Year': car_years,
        'Kilometers': car_kms
    })
    df.to_csv('car_info.csv', index=False, encoding='utf-8-sig')


def main():
    try:
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        # driver = webdriver.Chrome(service=service)
        all_car_models, all_car_prices, all_car_years, all_car_kms = crawl_all_pages2(driver_path)
        save_to_csv2(all_car_models, all_car_prices, all_car_years, all_car_kms)
        # 其餘的代碼保持不變
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
