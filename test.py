import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random

# 設置並發請求的最大數量
MAX_CONCURRENT_REQUESTS = 3

# 設置請求之間的延遲範圍（秒）
MIN_DELAY = 1
MAX_DELAY = 3

# 模擬真實瀏覽器的請求頭
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


async def get_car_info_async(session, page, semaphore):
    url = f"https://auto.8891.com.tw/?page={page}"
    async with semaphore:
        # 添加隨機延遲
        await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

        async with session.get(url, headers=HEADERS) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

        car_models, car_prices, car_years, car_kms, car_locations, car_views = [], [], [], [], [], []

        info_titles = soup.find_all(class_='ib-info-title')
        extra_infos = soup.find_all(class_='ib-row ib-extra')
        info_ims = soup.find_all(class_='ib-info-im')
        print(f'{html} and {soup} and {info_ims}')
        if not info_titles or not extra_infos or not info_ims:
            print(f"No car information found on page {page}")
            return None

        for info_title, extra_info, info_im in zip(info_titles, extra_infos, info_ims):
            try:
                model = info_title.find(class_='ib-it-text').text.strip()
                car_models.append(model)

                price = extra_info.find(class_='ib-price').text.strip()
                car_prices.append(price)

                icons = extra_info.find_all(class_='ib-icon')
                year = icons[0].text.strip() if icons else "N/A"
                car_years.append(year)

                km = icons[1].text.strip() if len(icons) > 1 else "N/A"
                car_kms.append(km)

                location_items = info_im.find_all(class_='ib-ii-item')
                location = location_items[0].text.strip() if location_items else "N/A"
                car_locations.append(location)

                views = location_items[2].text.strip() if len(location_items) > 2 else "N/A"
                car_views.append(views)

            except Exception as e:
                print(f"Failed to extract information from an element on page {page}: {str(e)}")

        return car_models, car_prices, car_years, car_kms, car_locations, car_views


async def crawl_all_pages_async(max_pages=1):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = [get_car_info_async(session, page, semaphore) for page in range(1, max_pages+1)]
        results = await asyncio.gather(*tasks)

    all_car_models, all_car_prices, all_car_years, all_car_kms, all_car_locations, all_car_views = [], [], [], [], [], []
    for result in results:
        if result:
            car_models, car_prices, car_years, car_kms, car_locations, car_views = result
            all_car_models.extend(car_models)
            all_car_prices.extend(car_prices)
            all_car_years.extend(car_years)
            all_car_kms.extend(car_kms)
            all_car_locations.extend(car_locations)
            all_car_views.extend(car_views)

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


async def main():
    try:
        start_time = time.time()
        all_car_models, all_car_prices, all_car_years, all_car_kms, all_car_locations, all_car_views = await crawl_all_pages_async()
        save_to_csv(all_car_models, all_car_prices, all_car_years, all_car_kms, all_car_locations, all_car_views)
        end_time = time.time()
        print(f'Total time: {end_time - start_time} seconds')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
