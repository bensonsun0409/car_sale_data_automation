from DownloadHelper.CarPageHelper import CarDataScraper
from DownloadHelper.CarDealerScraper import CarDealerScraper
from DownloadHelper.CarDealerHelper import WebScraper
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import traceback
import gc
import pandas as pd
# Set up logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='script_execution.log', level=logging.INFO, format=log_format)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(console_handler)
def convert_to_int(value):
    """
    將輸入值轉換為整數
    - 移除非數字字符
    - 處理空值或無效值
    - 返回整數或 None
    """
   
        # 如果是空值或非字符串，直接返回None
    try:
        # 如果是空值或空字串，返回 None
        if pd.isna(value) or value is None or value == '':
            return None
        # 將值轉換為整數
        return int(float(value))
    except:
        return None
        


def create_dealer_dataframe(all_titles, all_links, all_ratings, all_rating_counts, 
                          all_in_stocks, all_in_stores, all_view_counts, 
                          all_transaction_record, all_address,all_scrawldate,all_location):
    """
    將所有列表轉換為DataFrame，並將指定欄位轉換為整數
    """
    try:
        # 創建資料字典
        data_dict = {
            'title': all_titles,
            'link': all_links,
            'rating': all_ratings,
            'rating_count': all_rating_counts,
            'in_stock': all_in_stocks,
            'in_store': all_in_stores,
            'view_count': all_view_counts,
            'transaction_record': all_transaction_record,
            'address': all_address,
            'scrawldate' : all_scrawldate,
            'location': all_location
        }

        # 檢查所有列表長度是否一致
        lengths = [len(value) for value in data_dict.values()]
        if len(set(lengths)) > 1:
            logging.warning(f"列表長度不一致: {dict(zip(data_dict.keys(), lengths))}")
            min_length = min(lengths)
            for key in data_dict:
                data_dict[key] = data_dict[key][:min_length]
            logging.info(f"已將所有列表截斷至長度 {min_length}")

        # 創建 DataFrame
        df = pd.DataFrame(data_dict)
        
        # # 轉換數值欄位為整數
        numeric_columns = ['rating', 'rating_count', 'in_stock', 'in_store', 'view_count']
        for col in numeric_columns:
            df[col] = df[col].apply(convert_to_int)

        # 基本統計資訊
        logging.info("\n--- DataFrame 統計資訊 ---")
        logging.info(f"總資料筆數: {len(df)}")
        logging.info(f"欄位: {', '.join(df.columns)}")
        logging.info(f"\n缺失值統計:\n{df.isnull().sum()}")
        
        return df
    except Exception as e:
        logging.error(f"創建 DataFrame 時發生錯誤: {str(e)}")
        logging.error(traceback.format_exc())
        return None
def main(test_mode = True):
    url = "https://www.8891.com.tw/findBuz-index.html"
    # url = "https://www.8891.com.tw/findBuz-index.html?firstRow=30&totalRows=2199&"
    scraper = CarDealerScraper()
    total_data = scraper.total_counts(url)

    if test_mode:
            logging.info("執行測試模式 - 只爬取前30筆資料")
            total_data = 30
    
    logging.info(total_data)
    current_value = 0
    all_titles = []
    all_links = []
    all_ratings = []
    all_rating_counts = []
    all_in_stocks = []
    all_in_stores = []
    all_view_counts = []
    all_scrawldate = []
  
    if total_data % 30 == 0:
        # while current_value < 30:
        while current_value < total_data:
            logging.info(current_value)
            url = f'https://www.8891.com.tw/findBuz-index.html?firstRow={current_value}&totalRows={total_data}&'
            titles, links, ratings, rating_counts, in_stocks, in_stores, view_counts, scrawldate = scraper.scrape_dealers(url)
            # 將新的數據添加到對應的列表中
            all_titles.extend(titles)
            all_links.extend(links)
            all_ratings.extend(ratings)
            all_rating_counts.extend(rating_counts)
            all_in_stocks.extend(in_stocks)
            all_in_stores.extend(in_stores)
            all_view_counts.extend(view_counts)
            all_scrawldate.extend(scrawldate)
            
            current_value += 30
    else:
        while current_value <= total_data:
            logging.info(current_value)
            url = f'https://www.8891.com.tw/findBuz-index.html?firstRow={current_value}&totalRows={total_data}'
            titles, links, ratings, rating_counts, in_stocks, in_stores, view_counts,strawldate = scraper.scrape_dealers(url)

            # 將新的數據添加到對應的列表中
            all_titles.extend(titles)
            all_links.extend(links)
            all_ratings.extend(ratings)
            all_rating_counts.extend(rating_counts)
            all_in_stocks.extend(in_stocks)
            all_in_stores.extend(in_stores)
            all_view_counts.extend(view_counts)
            all_scrawldate.extend(strawldate)
            current_value += 30
    # titles, links, ratings, rating_counts, in_stocks, in_stores, view_counts = scraper.scrape_dealers(url)
    #
    # 打印結果
    logging.info(f'車行總數{len(all_titles)}')
    for i in range(len(all_titles)):
        logging.info(f"標題: {all_titles[i]}")
        logging.info(f"連結: {all_links[i]}")
        logging.info(f"評分: {all_ratings[i]}")
        logging.info(f"評價數量: {all_rating_counts[i]}")
        logging.info(f"在庫數量: {all_in_stocks[i]}")
        logging.info(f"在店數量: {all_in_stores[i]}")
        logging.info(f"瀏覽數: {all_view_counts[i]}")

        logging.info("------------------------")

    all_transaction_record = []
    all_address = []
    all_location = []
    for url in all_links:
        scraper = WebScraper()
        car_data = scraper.scrape_data(url)
        if car_data:
            transaction_record, address,location = car_data
            all_transaction_record.append(transaction_record)
            all_address.append(address)
            all_location.append(location)
            logging.info(f"Processed URL: {url}")
            logging.info(f"Car Data: {transaction_record}")
            logging.info(f"Car Data: {address}")
            logging.info(f"location: {location}")
        else:
            logging.info("未找到所需數據")
    logging.info(len(all_links))
    logging.info(len(all_transaction_record))
    logging.info(len(all_address))
    df = create_dealer_dataframe(
        all_titles, all_links, all_ratings, all_rating_counts,
        all_in_stocks, all_in_stores, all_view_counts,
        all_transaction_record, all_address,all_scrawldate,all_location
    )

    if df is not None:
        # 顯示前5筆資料
        logging.info("\n--- 資料預覽 ---")
        logging.info(df.head())
        
        # 基本統計描述
        logging.info("\n--- 數值欄位統計描述 ---")
        logging.info(df.describe())
        
        # 可以選擇將DataFrame存為CSV
        try:
            df.to_csv('car_dealers_data.csv', index=False, encoding='utf-8-sig')
            logging.info("資料已儲存至 car_dealers_data.csv")
        except Exception as e:
            logging.error(f"儲存CSV時發生錯誤: {str(e)}")
        
        # 如果需要存入資料庫
        try:
            save_to_sql(df)
        except Exception as e:
            logging.error(f"存入資料庫時發生錯誤: {str(e)}")

def save_to_sql(df):
    engine = create_engine('mysql+mysqlconnector://root:b03b02019@localhost/car_info')
    try:
        df.to_sql(name='car_seller', con=engine, if_exists='append', index=False) 
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


if __name__ == "__main__":
    main(test_mode=True)
