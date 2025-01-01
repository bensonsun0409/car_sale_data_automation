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
import logging

# Set up logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='script_execution.log', level=logging.INFO, format=log_format)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(console_handler)

def save_to_csv(result):
    result.to_csv('car_info2.csv', index=False, encoding='utf-8-sig')

def fetch_car_data(scraper, url, index, count_url):
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
def process_and_save(all_car_data, all_car_url, all_car_locations, all_car_views, all_year, all_car_scrawldate, index, batch_size):
    # 將目前批次的資料轉為 DataFrame 並儲存
    start_idx = max(0, index - len(all_car_data) + 1)
    end_idx = index + 1
    df1 = pd.DataFrame({
        'url': all_car_url[start_idx:end_idx],
        'location': all_car_locations[start_idx:end_idx],
        'views': all_car_views[start_idx:end_idx],
        'year': all_year[start_idx:end_idx],
        'scrawldate': all_car_scrawldate[start_idx:end_idx]
    })
    df2 = pd.DataFrame(all_car_data)
    result = pd.concat([df1, df2], axis=1)

    # 儲存到 SQL
    save_to_sql(result)

def main():
    start_time = time.time()
    helper = StringHelper()
    args = sys.argv[1:]
    scrawldate = 0
    logging.info(f"Script1 receive argument: {args}")
   
    if len(args) == 2:
        logging.info(f"Script1 process two argument: {args[0]}, {args[1]}")
        brand = args[0]
        scrawldate = args[1]
        all_car_url, all_car_locations, all_car_views, all_year, all_car_scrawldate = helper.scan_all_pages(args[1],args[0])
    elif len(args) == 3:
        logging.info(f"Script1 process three argument: {args[0]}, {args[1]}, {args[2]}")
        brand = args[0]
        model = args[1]
        scrawldate = args[2]
        all_car_url, all_car_locations, all_car_views, all_year, all_car_scrawldate = helper.scan_all_pages(args[2],args[0], args[1] )
    else:
        logging.info("Script1 error: argument number isn't right")
        return

    batch_size = 500  # 設定每批處理的URL數量
    all_car_data = []
    count_url = len(all_car_url)

    # 初始化 scraper
    scraper = CarDataScraper()  
    for index, url in enumerate(all_car_url):
        try:
            car_data = fetch_car_data(scraper, url, index, count_url)
            all_car_data.append(car_data)
            logging.info(f"Number {index+1} car_data {car_data}")

            # 批次儲存邏輯
            if (index + 1) % batch_size == 0:
                # 儲存目前的批次資料
                process_and_save(all_car_data, all_car_url, all_car_locations, all_car_views, all_year, all_car_scrawldate, index, batch_size)
                all_car_data.clear()  # 清空資料
                scraper.close()  # 關閉 scraper
                scraper = CarDataScraper()  # 初始化新的 scraper

        except Exception as e:
            logging.info(f'Number {index+1} error {e}')
            logging.info(f'find me')

    # 處理最後剩餘的資料
    if all_car_data:  # 如果還有未處理的資料
        process_and_save(all_car_data, all_car_url, all_car_locations, all_car_views, all_year, all_car_scrawldate, index, batch_size)

    scraper.close()
    gc.collect()

    # for index, url in enumerate(all_car_url):
    #     try:
    #         car_data = fetch_car_data(scraper, url, index, count_url)
    #         all_car_data.append(car_data)
    #         logging.info(f"Number {index+1} car_data {car_data}")

    #         # 當收集到500筆資料，將其儲存並釋放資源
    #         if (index + 1) % batch_size == 0 or (index + 1) == count_url:
    #             # 將目前批次的資料轉為DataFrame並儲存
    #             df1 = pd.DataFrame({
    #                 'url': all_car_url[index - batch_size + 1 : index + 1],
    #                 'location': all_car_locations[index - batch_size + 1 : index + 1],
    #                 'views': all_car_views[index - batch_size + 1 : index + 1],
    #                 'year': all_year[index - batch_size + 1 : index + 1],
    #                 'scrawldate': all_car_scrawldate[index - batch_size + 1 : index + 1]
                    
    #             })
    #             print(df1)
    #             df2 = pd.DataFrame(all_car_data)
    #             result = pd.concat([df1, df2], axis=1)

    #             # 儲存到SQL
    #             save_to_sql(result)

    #             # 清空暫存的資料並釋放資源
    #             all_car_data.clear()
    #             gc.collect()

    #             # 釋放並重新初始化 scraper
    #             scraper.close()  # 關閉目前的 scraper
    #             scraper = CarDataScraper()  # 重新開啟新的 scraper

    #     except Exception as e:
    #         logging.info(f'Number {index+1} error {e} ')
    #         logging.info(f'find me')

    # # 最後一批完成後確保 scraper 被關閉
    # scraper.close()  
    # gc.collect()
    end_time = time.time()
    total_time = end_time - start_time
    file_path = 'scrawldata.txt'
    file_exists = os.path.exists(file_path)
    
    mode = 'a' if file_exists else 'w'
    
    with open(file_path, mode, encoding='utf-8') as file:
        str1 = brand + " "
        if len(args) == 3:
            str1 += model + " "
        str1 += f'總共查詢了 {len(all_car_url)}'
        str1 += f'  總時間 {total_time} s'
        file.write(str1 + '\n')
    time.sleep(5)

if __name__ == "__main__":
    main()
