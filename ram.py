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
    url = f"{base_url}{version}/chromedriver_win32.zip"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download ChromeDriver from {url}")

    zip_path = "chromedriver.zip"
    with open(zip_path, "wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(".")

    os.remove(zip_path)


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


def get_car_models(page):
    url = f"https://auto.8891.com.tw/?page={page}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver_path = "./chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(5)

    car_models = []
    cars = driver.find_elements(By.CLASS_NAME, 'car-model-class')
    if not cars:
        print(f"No car models found on page {page}")
        driver.quit()
        return None

    for car in cars:
        model = car.find_element(By.CLASS_NAME, 'car-model').text.strip()
        car_models.append(model)

    driver.quit()
    return car_models


def crawl_all_pages():
    page = 1
    all_car_models = []
    while True:
        car_models = get_car_models(page)
        if not car_models:
            break
        all_car_models.extend(car_models)
        page += 1
        time.sleep(1)

    return all_car_models


def save_to_csv(car_models):
    df = pd.DataFrame(car_models, columns=['Car Model'])
    df.to_csv('car_models.csv', index=False)


def main():
    check_and_update_chromedriver()
    all_car_models = crawl_all_pages()
    save_to_csv(all_car_models)


if __name__ == "__main__":
    main()