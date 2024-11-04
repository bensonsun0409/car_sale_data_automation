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
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
import logging

# Set up logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='script_execution.log', level=logging.INFO, format=log_format)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(console_handler)

def save_to_csv(result):
    result.to_csv('car_info2.csv', index=False, encoding='utf-8-sig')

def fetch_car_data(scraper, url, index,count_url):
    try:
        car_data = scraper.scrape_car_data(url)
        logging.info(f"Successfully scraped data for URL {index + 1} / {count_url}: {url}")
        return car_data
    except Exception as e:
        logging.error(f"Failed to scrape data for {url}: {str(e)}")
        return {}

def save_to_sql(df):
    engine = create_engine('mysql+mysqlconnector://root:Aa123456@localhost/car_info')
    try:
        df.to_sql(name='car_data', con=engine, if_exists='append', index=False) 
        logging.info("Data successfully saved to SQL.")
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemy Error: Failed to save data to SQL.\n{str(e)}\n{traceback.format_exc()}")
    except Exception as e:
        logging.error(f"Unexpected error: Failed to save data to SQL.\n{str(e)}\n{traceback.format_exc()}")
    finally:
        if not df.empty:
            logging.debug(f"DataFrame content:\n{df.to_string()}")
        del df
        gc.collect()



def main():
    start_time = time.time()
    helper = StringHelper()
    args = sys.argv[1:]

    logging.info(f"Script1 receive argument: {args}")
   
    if len(args) == 1:
        logging.info(f"Script1 process one argument: {args[0]}")
        brand = args[0]
        all_car_url, all_car_locations, all_car_views, all_year = helper.scan_all_pages(args[0])
    elif len(args) == 2:
        logging.info(f"Script1 process two argument: {args[0]}, {args[1]}")
        brand = args[0]
        model = args[1]
        all_car_url, all_car_locations, all_car_views, all_year = helper.scan_all_pages(args[0], args[1])
    else:
        logging.info("Script1 error: argument number isn't right")
        return
   

    logging.info(type(all_car_url))
    logging.info(all_car_url)
    scraper = CarDataScraper() 
    all_car_data = []
    count_url = len(all_car_url)
    
    for index, url in enumerate(all_car_url):
        try:
            car_data = fetch_car_data(scraper, url, index, count_url)
            all_car_data.append(car_data)
        except Exception as e:
            logging.info(f'Number {index} url {url} error {e} ')
            logging.info(f'find me')

    scraper.close()     
    df1 = pd.DataFrame({
        'url': all_car_url,
        'location': all_car_locations,
        'views': all_car_views,
        'year': all_year
    })
    
    df2 = pd.DataFrame(all_car_data)
    print(df2)
    result = pd.concat([df1, df2], axis=1)
    
    # save_to_csv(result)
    save_to_sql(result)
    gc.collect()
    end_time = time.time()
    total_time = end_time - start_time
    file_path = 'scrawldata.txt'
    file_exists = os.path.exists(file_path)
    
    mode = 'a' if file_exists else 'w'
    
    with open(file_path, mode, encoding='utf-8') as file:
        str1 = brand + " "
        if len(args) == 2:
            str1 += model + " "
        str1 += f'總共查詢了 {len(all_car_url)}'
        str1 += f'  總時間 {total_time} s'
        file.write(str1 + '\n')
    time.sleep(5)

if __name__ == "__main__":
    main()