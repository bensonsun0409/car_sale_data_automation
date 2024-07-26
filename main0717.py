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
    all_car_url, all_car_locations, all_car_views = helper.scan_all_pages('audi')

    save_to_csv(all_car_url, all_car_locations, all_car_views)
    url = 'https://auto.8891.com.tw/usedauto-infos-3976803.html?display__sale_code=3010013&flow_id=de95bd2f-ab18-4caa-aa5b-dce5773f7ea3'

    scraper = CarDataScraper()
    car_data = scraper.scrape_car_data(url)
    scraper.close()

    print(car_data)

if __name__ == "__main__":
    main()