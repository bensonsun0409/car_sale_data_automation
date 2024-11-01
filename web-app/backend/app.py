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

mysql = MySQL(app)
# logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s', filename='app.log')

font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansCJK-Regular.ttc')
custom_font = fm.FontProperties(fname=font_path)

# 全局設置字體
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [custom_font.get_name()]
plt.rcParams['axes.unicode_minus'] = False 

def fetch_data(query, params):
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(data, columns=columns)
    except Error as e:
        logging.error("Error executing query: %s", e)
        logging.error("Query: %s", query)
        logging.error("Parameters: %s", params)
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
def get_average_cumulative_count(startDate, endDate,  production_year=None, year=None, selected_brand=None, lowMilage=None, highMilage=None, video=None, verify=None, selectedEquip=None, color=None, city=None, loc=None, lowView=None, highView=None, lowAsknum=None, highAsknum=None, seller=None):
    query = """
        SELECT
            t1.scrawldate,
            AVG(t1.cumulative_count) as average_cumulative_count
        FROM
            (SELECT
                car_id,
                scrawldate,
                COUNT(scrawldate) OVER (PARTITION BY car_id ORDER BY scrawldate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as cumulative_count,
                product_year, year, brand, milage, video, verify_tag, location, car_location, views, ask_num, seller_info,color,model,胎壓偵測,
                動態穩定系統, 防盜系統, keyless免鑰系統, 循跡系統, 中控鎖, 剎車輔助系統, 兒童安全椅固定裝置, ABS防鎖死, 安全氣囊, 定速系統, LED頭燈, 倒車顯影系統,
                衛星導航,多功能方向盤, 倒車雷達, 恆溫空調, 自動停車系統, 電動天窗, `真皮/皮革座椅`
                FROM car_info.car_data
            WHERE scrawldate >= %s AND scrawldate <= %s) t1
        JOIN
            (SELECT
                car_id,
                scrawldate,
                COUNT(scrawldate) OVER (PARTITION BY car_id ORDER BY scrawldate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as cumulative_count
            FROM car_info.car_data
            WHERE scrawldate >= %s AND scrawldate <= %s) t2
        ON
            t1.car_id = t2.car_id
        AND
            t1.scrawldate >= t2.scrawldate
        WHERE
            1=1
    """
    params = [startDate, endDate, startDate, endDate]

    if production_year:
        query += f" AND t1.product_year IN ({production_year})"
       
    if len(selected_brand) != 0:
        str1=f' AND brand in (select brand from car_info.car_data where'
        like_conditions = []
        for i in selected_brand:
            like_conditions.append(f' brand LIKE "%%{i}%%"')

            # 將 LIKE 條件串聯起來並添加到查詢字串中
        str1 += " OR ".join(like_conditions) + ')'
        
        # 將查詢字串添加到主查詢中
        query += str1
    if year:
        query += f" AND t1.year IN ({year})"


    if lowMilage and highMilage:
        query += f" AND t1.milage >= {lowMilage} AND t1.milage <= {highMilage}"

    if video:
        query += " AND t1.video = 'Y'"
    if verify:
        query += " AND t1.verify_tag = 'Y'"
    if selectedEquip:
        for equip in selectedEquip:
            equip = equip.strip()
            query += f" AND t1.{equip} = 'Y'"
    if city:
        query += f" AND t1.location IN ({city})"

    if color:
        query += f" AND t1.color IN ({color})"

    if loc:
        query += f" AND t1.car_location IN ({loc})"

    if lowView and highView:
        query +=f" AND t1.views >= {lowView} AND t1.views <= {highView}"

    if lowAsknum and highAsknum:
        query += f" AND t1.ask_num >= {lowAsknum} AND t1.ask_num <= {highAsknum}"

    if seller:
        query += f'AND t1.seller_info LIKE "%%{seller}%%" '
       

    query += " GROUP BY t1.scrawldate ORDER BY t1.scrawldate"

    try:
        df = fetch_data(query, tuple(params))
        df['scrawldate'] = pd.to_datetime(df['scrawldate'])
        return df
    except Exception as e:
        logging.error("Error in get_average_cumulative_count: %s", e)
        return None
@app.route('/search', methods=['POST'])
def search():
    
        filters = request.json
        startDate=filters.get('startDate')
        endDate = filters.get('endDate')
        car_brand = filters.get('carBrand')
        selected_brand = filters.get('selectedBrands')
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
            SELECT scrawldate, AVG(price) as avg_price 
            FROM car_info.car_data 
            WHERE price != "電洽" AND scrawldate >= %s AND scrawldate <= %s 
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
            brand,
            model,
            year,
            color,
            AVG(CASE WHEN milage BETWEEN 0 AND 999 THEN price END) AS avg_price_0_999,
            AVG(CASE WHEN milage BETWEEN 1000 AND 2999 THEN price END) AS avg_price_1000_2999,
            AVG(CASE WHEN milage BETWEEN 3000 AND 5999 THEN price END) AS avg_price_3000_5999,
            AVG(CASE WHEN milage BETWEEN 6000 AND 8999 THEN price END) AS avg_price_6000_8999,
            AVG(CASE WHEN milage BETWEEN 9000 AND 9999 THEN price END) AS avg_price_9000_9999,
            AVG(CASE WHEN milage BETWEEN 10000 AND 12999 THEN price END) AS avg_price_10000_12999,
            AVG(CASE WHEN milage BETWEEN 13000 AND 15999 THEN price END) AS avg_price_13000_15999,
            AVG(CASE WHEN milage BETWEEN 16000 AND 19999 THEN price END) AS avg_price_16000_19999,
            AVG(CASE WHEN milage BETWEEN 20000 AND 28999 THEN price END) AS avg_price_20000_28999,
            AVG(CASE WHEN milage BETWEEN 29000 AND 39999 THEN price END) AS avg_price_29000_39999,
            AVG(CASE WHEN milage BETWEEN 40000 AND 59999 THEN price END) AS avg_price_40000_59999,
            AVG(CASE WHEN milage BETWEEN 60000 AND 89999 THEN price END) AS avg_price_60000_89999,
            AVG(CASE WHEN milage BETWEEN 90000 AND 99999 THEN price END) AS avg_price_90000_99999,
            AVG(CASE WHEN milage >= 100000 THEN price END) AS avg_price_100000_plus
            FROM 
            cars
            WHERE 
            scrawldate >= %s AND scrawldate <= %s
           
"""


    }

        params = [startDate, endDate]


        if production_year:
            for key in queries:
                queries[key] += f" AND product_year in ({production_year})"
            
        if year:
            for key in queries:
                queries[key] += f" AND year in ({year})"
        if len(selected_brand) != 0:
            for key in queries:
                str1=f' AND brand in (select brand from car_info.car_data where'
                like_conditions = []
                for i in selected_brand:
                    like_conditions.append(f' brand LIKE "%%{i}%%"')

                # 將 LIKE 條件串聯起來並添加到查詢字串中
                str1 += " OR ".join(like_conditions) + ')'
                
                # 將查詢字串添加到主查詢中
                queries[key] += str1
        # if len(selected_model) != 0:
        #     for key in queries:
        #         str1=f' AND model in (select brand from car_info.car_data where'
        #         like_conditions = []
        #         for i in selected_brand:
        #             like_conditions.append(f' brand LIKE "%%{i}%%"')

        #         # 將 LIKE 條件串聯起來並添加到查詢字串中
        #         str1 += " OR ".join(like_conditions) + ')'
                
                # 將查詢字串添加到主查詢中
                queries[key] += str1

            
        if lowMilage and highMilage:
            for key in queries:
                queries[key] += f" AND milage >= {lowMilage} and milage <= {highMilage}"
        
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
        if lowView and highView:
            for key in queries:
                queries[key] += f" AND views >= {lowView} and views <= {highView}"
        
        if lowAsknum and highAsknum:
            for key in queries:
                queries[key] += f" AND ask_num >= {lowAsknum} and ask_num <= {highAsknum}"
        if seller:
            for key in queries:
                queries[key] += f' AND seller_info LIKE  "%%{seller}%%" '        

        
        for key in queries:
            if key != "table_avg_price":
                queries[key] += " GROUP BY scrawldate ORDER BY scrawldate"
            else:
                queries[key] +=" GROUP BY brand, model, year, colorORDER BY brand, model, year, color;"
        datas = {}
        images = {}
        print(queries)
        avg_cumulative_count_df = get_average_cumulative_count(
                startDate, endDate,  production_year, year, selected_brand,
                lowMilage, highMilage, video, verify, selectedEquip, color,
                city, loc, lowView, highView, lowAsknum, highAsknum, seller)
        for key, query in queries.items():
            try:
                df = fetch_data(query, tuple(params))
                df['scrawldate'] = pd.to_datetime(df['scrawldate'])

                print(df)
                if key == "average_price":
                    image = generate_plot(df, 'scrawldate', 'avg_price', '平均價格','日期','價格(萬)')
                elif key == "listing_count":
                    image = generate_plot(df, 'scrawldate', 'listing_count', '刊登數量','日期','刊登數')
                elif key == "avg_views":
                    image = generate_plot(df, 'scrawldate', 'avg_views', '平均瀏覽數','日期','瀏覽數')
                elif key == "avg_asknum":
                    image = generate_plot(df, 'scrawldate', 'avg_asknum', '平均諮詢數','日期','諮詢數')
                elif key ==" table_avg_price":
                    datas["table_avg_price"] = df.to_json(orient='records')
                    
    
                else:
                    continue
                images[key] = image
            except Exception as e:
                logging.error("Error in handle_queries: %s", e)
                return jsonify({"success": False, "message": str(e)})
        if avg_cumulative_count_df is not None:
            images['avg_cumulative_count_df'] = generate_plot(
                avg_cumulative_count_df, 'scrawldate', 'average_cumulative_count',
                '每日平均累計刊登數', '日期', '平均累計刊登數'
            )
       
        return jsonify({"success": True, "images": images, "data":datas})

