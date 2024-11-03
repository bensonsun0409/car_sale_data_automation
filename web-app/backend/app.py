from flask import Flask, logging, request, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_mysqldb import MySQL
import base64
import matplotlib.pyplot as plt
import matplotlib
import io
import pandas as pd
import traceback
from mysql.connector import Error
import os
import logging
import matplotlib.font_manager as fm
app = Flask(__name__)
CORS(app)
matplotlib.use('Agg')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'b03b02019'
app.config['MYSQL_DB'] = 'car_info'
app.config['MYSQL_CHARSET'] = 'utf8'

mysql = MySQL(app)
# logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s', filename='app.log')

font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansCJK-Regular.ttc')
custom_font = fm.FontProperties(fname=font_path)

# 全局設置字體
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [custom_font.get_name()]
plt.rcParams['axes.unicode_minus'] = False 



def fetch_data(query, params=None):  # Make params optional
    conn = mysql.connection
    cursor = conn.cursor()

    try:
        cursor.execute(query, params) if params else cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(data, columns=columns)
    except Error as e:
        logging.error("Error executing query: %s", e)
        raise

def generate_plot(dataframe, x_col, y_col, title, x_col_name, y_col_name):
    if dataframe is None or dataframe.empty:
        return None
    dataframe.dropna(subset=[x_col, y_col], inplace=True)
    try:
        plt.figure(figsize=(6, 4))
        plt.plot(dataframe[x_col], dataframe[y_col], marker='o')
        plt.xlabel(x_col_name, fontproperties=custom_font)
        plt.ylabel(y_col_name, fontproperties=custom_font)
        plt.title(title, fontproperties=custom_font)
        plt.grid(True)
        
        # 設置刻度標籤的字體
        plt.xticks(fontproperties=custom_font)
        plt.yticks(fontproperties=custom_font)
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        
        img.seek(0)
        plt.close()
        
        return base64.b64encode(img.getvalue()).decode('utf-8')
    except Exception as e:
        app.logger.error(f"Plot generation error: {str(e)}")
        app.logger.exception("Exception details:")
        return None

def search_seller(startdate,enddate):
    query="""SELECT title as 店鋪名稱,
            rating as 評價星等,
            rating_count as 評價數,
            transaction_record as 成交紀錄,
            view_count as 瀏覽數,
            in_stock as 在庫數, 
            in_store as 在店數, 
            location as 地區,
            address as 地址
            FROM car_info.car_seller 
            Where scrawldate>= %s and scrawldate <= %s"""
    params=[startdate,enddate]
    try:
        df = fetch_data(query, tuple(params))
        return df
    except Exception as e:
        logging.error("Error in search_seller: %s", e)
        return None 
def total_onMarket_day_ralative(startDate, endDate, selected_brand, selected_model, production_year, lowMilage, highMilage, video, verify, selectedEquip, 
                                color, city, loc, year, lowView, highView, lowAsknum, highAsknum, seller, datas, images):
    beforeData = f"""WITH distinct_data AS (
            SELECT DISTINCT
                car_id,
                scrawldate
            FROM 
                car_info.car_data
            WHERE 
                scrawldate >= "{startDate}" AND scrawldate <= "{endDate}"
        """
       
        

    if production_year:
        beforeData += f" AND product_year in ({production_year})"
            
    if year:
        beforeData += f" AND year in ({year})"
    if len(selected_brand) != 0:
        # 使用列表推導式來將每個品牌轉換成 LIKE 條件
        like_conditions = [f"LOWER(brand) LIKE '%{brand.lower()}%'" for brand in selected_brand]
        
        # 使用 OR 來串聯所有 LIKE 條件，並添加到查詢字串中
        str1 = f" AND ({' OR '.join(like_conditions)})"
        
        # 將查詢字串添加到主查詢中
        beforeData += str1

        if len(selected_model) != 0:
            model_list = [f"'{model}'" for model in selected_model]
            
            # 使用 join 來串聯品牌，形成 IN 的條件
            str2 = f" AND model IN ({', '.join(model_list)})"

            
            beforeData += str2



        
    if lowMilage and highMilage:
        beforeData += f" AND milage >= {lowMilage} "
    if highMilage:
  
        beforeData += f" AND milage <= {highMilage}"
    
    if video:
        beforeData += f' AND video = "Y" '
    
    if verify:
        beforeData += f' AND verify_tag = "Y" '

    if len(selectedEquip)!=0:
        for equip in selectedEquip:
            equip=equip.strip()
            print(equip)
            beforeData += f' AND {equip} = "Y" '
    if city:
        beforeData += f" AND location in ({city}) "
    if color:
        beforeData += f" AND color in ({color}) "
    if loc:
        beforeData += f' AND car_location in ({loc}) '
    if lowView :
        
        beforeData += f" AND views >= {lowView} "
    if highView :
        beforeData +=f" AND views <= {highView} "
    
    if lowAsknum :
        
        beforeData += f" AND ask_num >= {lowAsknum} "
    if highAsknum:
        beforeData += f" AND ask_num <= {highAsknum}"
    if seller:
        
        beforeData += f' AND seller_info LIKE  "%%{seller}%%" '        

    queries = {
        "avg_market_date":f"""{beforeData}),
        date_records AS (
            SELECT 
                car_id,
                scrawldate,
                LEAD(scrawldate) OVER (PARTITION BY car_id ORDER BY scrawldate) AS next_date
            FROM 
                distinct_data
        ),
        scrawltable AS (
            SELECT 
                car_id,
                scrawldate,
                next_date,
                CASE
                    WHEN next_date IS NULL THEN
                        CASE
                            WHEN scrawldate != "{endDate}" THEN DATEDIFF("{endDate}", scrawldate)
                            ELSE 1
                        END
                    ELSE DATEDIFF(next_date, scrawldate)
                END AS day_diff
            FROM 
                date_records
        ),
        total_count AS (
            SELECT car_id,
                SUM(
                    CASE
                        WHEN day_diff >= 3 THEN 3
                        ELSE day_diff
                    END
                ) AS total_day_count
            FROM 
                scrawltable
            GROUP BY 
                car_id
        ),
        newtable as
		(
        select distinct  a.car_id,a.scrawldate,b.total_day_count as day_count from car_info.car_data as a
        join total_count b 
        on a.car_id=b.car_id
        )
        select scrawldate,AVG(day_count) as avg_market_date from newtable """,


        "avg_ask_price":f"""{beforeData}),
        date_records AS (
            SELECT 
                car_id,
                scrawldate,
                LEAD(scrawldate) OVER (PARTITION BY car_id ORDER BY scrawldate) AS next_date
            FROM 
                distinct_data
        ),
        scrawltable AS (
            SELECT 
                car_id,
                scrawldate,
                next_date,
                CASE
                    WHEN next_date IS NULL THEN
                        CASE
                            WHEN scrawldate != "{endDate}" THEN DATEDIFF("{endDate}", scrawldate)
                            ELSE 1
                        END
                    ELSE DATEDIFF(next_date, scrawldate)
                END AS day_diff
            FROM 
                date_records
        ),
        total_count AS (
            SELECT car_id,
                SUM(
                    CASE
                        WHEN day_diff >= 3 THEN 3
                        ELSE day_diff
                    END
                ) AS total_day_count
            FROM 
                scrawltable
            GROUP BY 
                car_id
        ),

        newtable as(
        SELECT distinct a.car_id,
            a.brand,
            a.model,
            a.year,
            a.product_year,
            a.color,
            a.milage,
            a.price,
            b.total_day_count
            
        FROM 
            car_info.car_data as a
            join total_count as b
            on a.car_id = b.car_id
        WHERE 
            a.car_id IS NOT NULL
            and b.total_day_count > 0
        
        )
        select brand as 品牌,
        model as 型號,
        year as 年份,
        color as 顏色,
        milage as 里程數,
        count(*) as 上架數量,
        round(avg(price),2) as 平均價格,
        round(avg(total_day_count),2) as 平均上架天數
        from newtable
        where price is not null
        """,
        
        "avg_day_on_market":f"""{beforeData}
        ),
        date_records AS (
            SELECT 
                car_id,
                scrawldate,
                LEAD(scrawldate) OVER (PARTITION BY car_id ORDER BY scrawldate) AS next_date
            FROM 
                distinct_data
        ),
        scrawltable AS (
            SELECT 
                car_id,
                scrawldate,
                next_date,
                CASE
                    WHEN next_date IS NULL THEN
                        CASE
                            WHEN scrawldate != "{endDate}" THEN DATEDIFF("{endDate}", scrawldate)
                            ELSE 1
                        END
                    ELSE DATEDIFF(next_date, scrawldate)
                END AS day_diff
            FROM 
                date_records
        ),
        total_count AS (
            SELECT car_id,
                SUM(
                    CASE
                        WHEN day_diff >= 3 THEN 3
                        ELSE day_diff
                    END
                ) AS total_day_count
            FROM 
                scrawltable
            GROUP BY 
                car_id
        ),
        newtable as
		(
        select distinct  a.car_id,a.brand,a.model,a.year,a.color,a.milage,b.total_day_count from car_info.car_data as a
        join total_count b 
        on a.car_id=b.car_id
        )
        SELECT 
            brand as 品牌,
            model as 型號,
            year as 年份,
            color as 顏色,
            ROUND(AVG(CASE WHEN milage BETWEEN 0 AND 999 THEN total_day_count END), 1) AS `999公里內`,
            ROUND(AVG(CASE WHEN milage BETWEEN 1000 AND 2999 THEN total_day_count END), 1) AS `1000-2999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 3000 AND 5999 THEN total_day_count END), 1) AS `3000-5999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 6000 AND 8999 THEN total_day_count END), 1) AS `6000-8999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 9000 AND 9999 THEN total_day_count END), 1) AS `9000-9999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 10000 AND 12999 THEN total_day_count END), 1) AS `10000-12999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 13000 AND 15999 THEN total_day_count END), 1) AS `13000-15999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 16000 AND 19999 THEN total_day_count END), 1) AS `16000-19999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 20000 AND 28999 THEN total_day_count END), 1) AS `20000-28999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 29000 AND 39999 THEN total_day_count END), 1) AS `29000-39999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 40000 AND 59999 THEN total_day_count END), 1) AS `40000-59999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 60000 AND 89999 THEN total_day_count END), 1) AS `60000-89999公里`,
            ROUND(AVG(CASE WHEN milage BETWEEN 90000 AND 99999 THEN total_day_count END), 1) AS `90000-99999公里`,
            ROUND(AVG(CASE WHEN milage >= 100000 THEN total_day_count END), 1) AS `10萬公里以上`

        FROM 
            newtable
        WHERE
            brand is not null"""}
        
    for key in queries:
        if  key =="avg_day_on_market"  :
            queries[key] +=" GROUP BY brand, model, year, color ORDER BY brand, model, year, color;"
        elif key =="avg_ask_price" :
            queries[key] += "group by brand,model,year,color,milage order by brand,model,year,color,milage"
        elif key =="avg_market_date":
            queries[key] += "group by scrawldate order by scrawldate"
    print("avg_market_date 的query sql指令: "+ queries["avg_market_date"])
    for key, query in queries.items():
        try:
            if key =="avg_day_on_market":
                df = fetch_data(query)
                datas["avg_day_on_market"] = df.to_json(orient='records', force_ascii=False)
            elif key == "avg_market_date":
                df = fetch_data(query)
                image = generate_plot(df, 'scrawldate', 'avg_market_date', '平均上架天數', '日期', '天數')
                images[key] = image
            elif key == "avg_ask_price":
                df = fetch_data(query)
                datas["avg_ask_price"] = df.to_json(orient='records', force_ascii=False)       
        except Exception as e:
            logging.info(f"Error in {key} : {e}")                            

    return datas, images

@app.route('/search', methods=['POST'])
def search():
    
        filters = request.json
        startDate=filters.get('startDate')
        endDate = filters.get('endDate')
        selected_brand = filters.get('selectedBrands', [])
        selected_model = filters.get('selectedModels', [])
        production_year = filters.get('productYear')
        lowMilage = filters.get('lowMilage')
        highMilage = filters.get('highMilage')
        video = filters.get('video')
        verify = filters.get('verify')
        selectedEquip = filters.get('selectedEquip')
        color = filters.get('color')
        city = filters.get('city')
        loc = filters.get('loc')
        year = filters.get('typeYear')
        lowView = filters.get('lowView')
        highView = filters.get('highView')
        lowAsknum = filters.get('lowAsknum')
        highAsknum = filters.get('highAsknum')
        seller = filters.get('seller')
        
        queries = {
 
        "average_price": """
            SELECT scrawldate, AVG(price) as 平均價格 
            FROM car_info.car_data 
            WHERE price is not null AND scrawldate >= %s AND scrawldate <= %s 
        """,

        "listing_count": """
            SELECT scrawldate, COUNT(*) as listing_count 
            FROM car_info.car_data 
            WHERE scrawldate >= %s AND scrawldate <= %s
        """,

        "avg_views": """
            SELECT scrawldate, AVG(views) as avg_views 
            FROM car_info.car_data 
            WHERE scrawldate >= %s AND scrawldate <= %s
        """,

        "avg_asknum": """
            SELECT scrawldate, AVG(ask_num) as avg_asknum
            FROM car_info.car_data 
            WHERE scrawldate >= %s AND scrawldate <= %s
        """,
        "table_avg_price":"""SELECT 
            brand AS 品牌,
            model AS 型號,
            year AS 年份,
            color AS 顏色,
            AVG(CASE WHEN milage BETWEEN 0 AND 999 THEN price END) AS `999公里內`,
            AVG(CASE WHEN milage BETWEEN 1000 AND 2999 THEN price END) AS `1000-2999公里`,
            AVG(CASE WHEN milage BETWEEN 3000 AND 5999 THEN price END) AS `3000-5999公里`,
            AVG(CASE WHEN milage BETWEEN 6000 AND 8999 THEN price END) AS `6000-8999公里`,
            AVG(CASE WHEN milage BETWEEN 9000 AND 9999 THEN price END) AS `9000-9999公里`,
            AVG(CASE WHEN milage BETWEEN 10000 AND 12999 THEN price END) AS `10000-12999公里`,
            AVG(CASE WHEN milage BETWEEN 13000 AND 15999 THEN price END) AS `13000-15999公里`,
            AVG(CASE WHEN milage BETWEEN 16000 AND 19999 THEN price END) AS `16000-19999公里`,
            AVG(CASE WHEN milage BETWEEN 20000 AND 28999 THEN price END) AS `20000-28999公里`,
            AVG(CASE WHEN milage BETWEEN 29000 AND 39999 THEN price END) AS `29000-39999公里`,
            AVG(CASE WHEN milage BETWEEN 40000 AND 59999 THEN price END) AS `40000-59999公里`,
            AVG(CASE WHEN milage BETWEEN 60000 AND 89999 THEN price END) AS `60000-89999公里`,
            AVG(CASE WHEN milage BETWEEN 90000 AND 99999 THEN price END) AS `90000-99999公里`,
            AVG(CASE WHEN milage >= 100000 THEN price END) AS `10萬公里以上`
        FROM 
            car_info.car_data
        WHERE 
            scrawldate >= %s AND scrawldate <= %s


           
""",
        "car_detail":"""SELECT DISTINCT 
    car_id as 編號,
    brand as 品牌,
    model as 車款,
    year as 年式,
    product_year as 出廠年份,
    milage as 里程數,
    color as 顏色,
    video as 影片看車,
    verify_tag as 第三方鑒定,
        TRIM(TRAILING ',' FROM (
        CONCAT(
            CASE WHEN 胎壓偵測 = 'Y' THEN '胎壓偵測,' ELSE '' END,
            CASE WHEN 動態穩定系統 = 'Y' THEN '動態穩定系統,' ELSE '' END,
            CASE WHEN 防盜系統 = 'Y' THEN '防盜系統,' ELSE '' END,
			CASE WHEN keyless免鑰系統 = 'Y' THEN 'keyless免鑰系統,' ELSE '' END,
            CASE WHEN 循跡系統 = 'Y' THEN '循跡系統,' ELSE '' END,
            CASE WHEN 剎車輔助系統 = 'Y' THEN '剎車輔助系統,' ELSE '' END,
			CASE WHEN 兒童安全椅固定裝置 = 'Y' THEN '兒童安全椅固定裝置,' ELSE '' END,
            CASE WHEN ABS防鎖死 = 'Y' THEN 'ABS防鎖死,' ELSE '' END,
            CASE WHEN 安全氣囊 = 'Y' THEN '安全氣囊,' ELSE '' END,
			CASE WHEN 定速系統 = 'Y' THEN '定速系統,' ELSE '' END,
            CASE WHEN LED頭燈 = 'Y' THEN 'LED頭燈,' ELSE '' END,
            CASE WHEN 倒車顯影系統 = 'Y' THEN '倒車顯影系統,' ELSE '' END,
			CASE WHEN 衛星導航 = 'Y' THEN '衛星導航,' ELSE '' END,
            CASE WHEN 多功能方向盤 = 'Y' THEN '多功能方向盤,' ELSE '' END,
            CASE WHEN 倒車雷達 = 'Y' THEN '倒車雷達,' ELSE '' END,
			CASE WHEN 恆溫空調 = 'Y' THEN '恆溫空調,' ELSE '' END,
            CASE WHEN 動態穩定系統 = 'Y' THEN '動態穩定系統,' ELSE '' END,
            CASE WHEN 自動停車系統 = 'Y' THEN '自動停車系統,' ELSE '' END,
			CASE WHEN 電動天窗 = 'Y' THEN '電動天窗,' ELSE '' END,
            CASE WHEN `真皮/皮革座椅` = 'Y' THEN '真皮/皮革座椅,' ELSE '' END
        )
    )) AS 配備,
    CONCAT(location,car_location) as 所在區域,
    views as 瀏覽數,
    ask_num as 諮詢數,
    seller_info as 店鋪名稱

FROM 
    car_info.car_data
WHERE 
    scrawldate >= %s AND scrawldate <= %s"""

    }

        params = [startDate, endDate]
        

        if production_year:
            for key in queries:
                queries[key] += f" AND product_year in ({production_year})"
            
        if year:
            for key in queries:
                queries[key] += f" AND year in ({year})"
        if len(selected_brand) != 0:
            # 使用列表推導式來將每個品牌包裹在單引號中
            for key in queries:
                brands_list = [f"'{brand}'" for brand in selected_brand]
                
                # 使用 join 來串聯品牌，形成 IN 的條件
                str1 = f" AND brand IN ({', '.join(brands_list)})"

                    
                    # 將查詢字串添加到主查詢中
                queries[key] += str1

                if len(selected_model) != 0:
                    model_list = [f"'{model}'" for model in selected_model]
                    
                    # 使用 join 來串聯品牌，形成 IN 的條件
                    str2 = f" AND model IN ({', '.join(model_list)})"

                    
                    queries[key]  += str2



            
        if lowMilage :
            for key in queries:
                queries[key] += f" AND milage >= {lowMilage} "
        if highMilage:
            for key in queries:
                queries[key] += f" AND milage <= {highMilage}"

        
        if video:
            for key in queries:
                queries[key] += f' AND video = "Y" '
        
        if verify:
            for key in queries:
                queries[key] += f' AND verify_tag = "Y" '

        if len(selectedEquip)!=0:
            for equip in selectedEquip:
                equip=equip.strip()
                print(equip)
                for key in queries:
                    queries[key] += f' AND {equip} = "Y" '
        if city:
            for key in queries:
                queries[key] += f" AND location in ({city}) "
        if color:
            for key in queries:
                queries[key] += f" AND color in ({color}) "
        if loc:
            for key in queries:
                queries[key] += f' AND car_location in ({loc}) '
        if lowView :
            for key in queries:
                queries[key] += f" AND views >= {lowView} "
        if highView:
            for key in queries:
                queries[key] += f"and views <= {highView}"
        
        if lowAsknum:
            for key in queries:
                queries[key] += f" AND ask_num >= {lowAsknum} "
        if highAsknum:
            for key in queries:
                queries[key] +=f" and ask_num <= {highAsknum} "
        if seller:
            for key in queries:
                queries[key] += f' AND seller_info LIKE  "%%{seller}%%" '        

        
        for key in queries:

            if key == "car_detail":
                continue
            elif key =="table_avg_price":
                queries[key] += " GROUP BY brand, model,year,color ORDER BY brand, model,year,color "
            else:
                queries[key] += " GROUP BY scrawldate ORDER BY scrawldate"
        datas = {}
        images = {}
        print(queries)
        seller_info = search_seller(startDate, endDate)
        datas["seller_info"] = seller_info.to_json(orient='records', force_ascii=False)
        for key, query in queries.items():
            try:
                if key !="avg_ask_price" and key!="avg_day_on_market" and key !="avg_market_date":
                    print("here")
                    print(key)
                    df = fetch_data(query, tuple(params))
                    
                    if 'scrawldate' in df.columns:
                        df['scrawldate'] = pd.to_datetime(df['scrawldate'])

                        print(df)  # 確認 df 的內容
                        if key == "average_price":
                            image = generate_plot(df, 'scrawldate', '平均價格', '平均價格', '日期', '價格(萬)')
                        elif key == "listing_count":
                            image = generate_plot(df, 'scrawldate', 'listing_count', '刊登數量', '日期', '刊登數')
                        elif key == "avg_views":
                            image = generate_plot(df, 'scrawldate', 'avg_views', '平均瀏覽數', '日期', '瀏覽數')
                        elif key == "avg_asknum":
                            image = generate_plot(df, 'scrawldate', 'avg_asknum', '平均諮詢數', '日期', '諮詢數')
                        images[key] = image
                
                    # 處理不需要 'scrawldate' 的查詢
                    else:
                        if key =="table_avg_price":
                            datas["table_avg_price"] = df.to_json(orient='records', force_ascii=False)
                        elif key =="car_detail":
                            datas["car_detail"] = df.to_json(orient='records', force_ascii=False)


            

                
                
            except Exception as e:
                logging.error(f"Error in handle_queries for {key}: %s", e)
                return jsonify({"success": False, "message": str(e)})
        
        datas, images = total_onMarket_day_ralative(startDate, endDate, selected_brand, selected_model, production_year, lowMilage, highMilage, video, verify, selectedEquip, 
                                    color, city, loc, year, lowView, highView, lowAsknum, highAsknum, seller, datas, images)
        print(datas["avg_ask_price"]) 
        return jsonify({"success": True, "images": images, "tabledata":datas})

