from DownloadHelper.MainPageHelper import StringHelper
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
    all_car_url, all_car_locations, all_car_views = helper.scan_all_pages('audi','q3')
    save_to_csv(all_car_url, all_car_locations, all_car_views)


if __name__ == "__main__":
    main()