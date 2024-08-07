from DownloadHelper.MainPageHelper import StringHelper
from DownloadHelper.CarPageHelper import CarDataScraper
import pandas as pd


def save_to_csv(car_url, car_locations, car_views):
    df = pd.DataFrame({
        'Car Url': car_url,
        'Location': car_locations,
        'Views': car_views,
    })
    df.to_csv('car_info.csv', index=False, encoding='utf-8-sig')


# 使用StringHelper類的方法
def main():
    helper = StringHelper()
    # 使用反轉字串方法
    all_car_url, all_car_locations, all_car_views = helper.scan_all_pages('ferrari')

    save_to_csv(all_car_url, all_car_locations, all_car_views)
    print(type(all_car_url))
    print(all_car_url)

    # scraper = CarDataScraper()
    all_car_data = []

    for url in all_car_url:
        scraper = CarDataScraper()
        car_data = scraper.scrape_car_data(url)
        all_car_data.append(car_data)
        print(f"Processed URL: {url}")
        print(f"Car Data: {car_data}")

        scraper.close()

    print("All car data collected:")
    for i, car_data in enumerate(all_car_data, 1):
        print(f"Car {i}:")
        print(car_data)
        print("-" * 50)

if __name__ == "__main__":
    main()