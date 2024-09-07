import asyncio
import aiohttp
import logging
import sys
import gc
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import traceback
from DownloadHelper.MainPageHelper import StringHelper
from DownloadHelper.CarPageHelper import CarDataScraper

gc.collect()
logging.basicConfig(filename='sql_error.log', level=logging.ERROR)

semaphore = asyncio.Semaphore(3)  # 限制並發請求數量為3

async def fetch_car_data(url, session):
    async with semaphore:
        scraper = CarDataScraper()
        try:
            car_data = await asyncio.wait_for(scraper.scrape_car_data(url), timeout=10)
        except asyncio.TimeoutError:
            logging.error(f"Timeout while scraping data for {url}")
            car_data = {}
        except Exception as e:
            logging.error(f"Failed to scrape data for {url}: {str(e)}")
            car_data = {}
        finally:
            scraper.close()
        return car_data

async def fetch_all_car_data(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch_car_data(url, session))
        responses = await asyncio.gather(*tasks)
        return responses

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

def main():
    helper = StringHelper()
    args = sys.argv[1:]

    print(f"Script1 receive argument: {args}")
    if len(args) == 1:
        print(f"Script1 process one argument: {args[0]}")
        brand = args[0]
        all_car_url, all_car_locations, all_car_views, all_year = helper.scan_all_pages(args[0])
    elif len(args) == 2:
        print(f"Script1 process two argument: {args[0]}, {args[1]}")
        brand = args[0]
        model = args[1]
        all_car_url, all_car_locations, all_car_views, all_year = helper.scan_all_pages(args[0], args[1])
    else:
        print("Script1 error: argument number isn't right")
        return

    print(type(all_car_url))
    print(all_car_url)

    all_car_data = []
    for url in all_car_url:
        car_data = asyncio.run(fetch_car_data(url, session))
        all_car_data.append(car_data)
        if len(all_car_data) >= 100:
            save_to_sql(pd.DataFrame(all_car_data))
            all_car_data = []
            gc.collect()

    if all_car_data:
        save_to_sql(pd.DataFrame(all_car_data))

    file_path = 'scrawldata.txt'
    file_exists = os.path.exists(file_path)
    
    mode = 'a' if file_exists else 'w'
    
    with open(file_path, mode, encoding='utf-8') as file:
        str1 = brand + " "
        if len(args) == 2:
            str1 += model + " "
        str1 += f'總共查詢了 {len(all_car_url)}'
        file.write(str1 + '\n')

if __name__ == "__main__":
    main()
