import json
import re
import pandas as pd
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
# 假設 log 資料存放在一個檔案中
log_file = "test.log"

# 提取 JSON 部分的資料
car_data_list = []
with open(log_file, "r", encoding="utf-8") as file:
    for line in file:
        match = re.search(r"car_data (.+)$", line)
        if match:
            raw_data = match.group(1).replace("'", '"').strip()
            # 修正 JSON 格式
            raw_data = raw_data.replace(": None", ": null")  # 替換 None 為 null
            raw_data = raw_data.replace("True", "true").replace("False", "false")  # 處理布林值
            try:
                car_data = json.loads(raw_data)
                car_data_list.append(car_data)
            except json.JSONDecodeError as e:
                print("無法解析的資料:", raw_data)
                print("錯誤訊息:", e)

# 轉換為 DataFrame
df = pd.DataFrame(car_data_list)

df.to_csv('car_info2.csv', index=False, encoding='utf-8-sig')
save_to_sql(df)
# 檢視資料
print(df.head())