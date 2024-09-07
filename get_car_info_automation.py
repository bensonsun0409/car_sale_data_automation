from DownloadHelper.MainPageHelper import StringHelper
from DownloadHelper.CarPageHelper import CarDataScraper
import pandas as pd
from sqlalchemy import create_engine
import traceback
import time
import logging
from sqlalchemy.exc import SQLAlchemyError
import sys
import gc
import asyncio

gc.collect()
logging.basicConfig(filename='sql_error.log', level=logging.ERROR)

def save_to_csv(result):
    result.to_csv('car_info2.csv', index=False, encoding='utf-8-sig')

def save_to_sql(df):
    engine = create_engine('mysql+mysqlconnector://root:b03b02019@localhost/car_info')
    try:
        df.to_sql(name='car_data', con=engine, if_exists='append', index=False)
        print("Data successfully saved to SQL.")
    except SQLAlchemyError as e:
        error_message = "SQLAlchemy Error: Failed to save data to SQL."
        print(error_message)
        logging.error(f"{error_message}\n{str(e)}\n{traceback.format_exc()}")
    except Exception as e:
        error_message = "Unexpected error: Failed to save data to SQL."
        print(error_message)
        logging.error(f"{error_message}\n{str(e)}\n{traceback.format_exc()}")
    finally:
        if not df.empty:
            logging.error(f"DataFrame content:\n{df.to_string()}")

async def process_car_data(scraper, url):
    car_data = await scraper.scrape_car_data(url)
    print(f"Processed URL: {url}")
    print(f"Car Data: {car_data}")
    return car_data

async def main():
    helper = StringHelper()
    args = sys.argv[1:]

    print(f"Script1 接收到的參數：{args}")

    if len(args) == 1:
        print(f"Script1 處理單個參數: {args[0]}")
        all_car_url, all_car_locations, all_car_views, all_year = helper.scan_all_pages(args[0])
    elif len(args) == 2:
        print(f"Script1 處理兩個參數: {args[0]}, {args[1]}")
        all_car_url, all_car_locations, all_car_views, all_year = helper.scan_all_pages(args[0], args[1])
    else:
        print("Script1 錯誤：參數數量不正確")
        return

    print(type(all_car_url))
    print(all_car_url)

    scraper = CarDataScraper()
    all_car_data = await asyncio.gather(*[process_car_data(scraper, url) for url in all_car_url])
    scraper.close()

    print("All car data collected:")
    df1 = pd.DataFrame({
        'url': all_car_url,
        'location': all_car_locations,
        'views': all_car_views,
        'year': all_year
    })
    df2 = pd.DataFrame(all_car_data)
    result = pd.concat([df1, df2], axis=1)
    print(result)

    save_to_sql(result)
    save_to_csv(result)

if __name__ == "__main__":
    asyncio.run(main())
