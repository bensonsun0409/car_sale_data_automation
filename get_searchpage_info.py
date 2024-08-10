from DownloadHelper.MainPageHelper import StringHelper
from DownloadHelper.CarPageHelper import CarDataScraper
import pandas as pd
from sqlalchemy import create_engine
import traceback
import time
import logging
from sqlalchemy.exc import SQLAlchemyError
logging.basicConfig(filename='sql_error.log', level=logging.ERROR)
def save_to_csv(result):
    # df1 = pd.DataFrame({
    #     'url': car_url,
    #     'location': car_locations,
    #     'views': car_views,
        
    # })
    # df2 = pd.DataFrame(car_data)
    # result = pd.concat([df1, df2], axis=1)
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
        # Optionally, log the DataFrame that failed to save
        if not df.empty:
            logging.error(f"DataFrame content:\n{df.to_string()}")

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
def main():
    helper = StringHelper()
    # 使用 StringHelper 类的方法
    all_car_url, all_car_locations, all_car_views, all_year = helper.scan_all_pages(brand)

    print(f"Processing brand: {brand}")
    print(type(all_car_url))
    print(all_car_url)

    all_car_data = []

    for url in all_car_url:
        scraper = CarDataScraper()
        try:
            car_data = scraper.scrape_car_data(url)
            all_car_data.append(car_data)
            print(f"Processed URL: {url}")
            print(f"Car Data: {car_data}")
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
        finally:
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
    main()




