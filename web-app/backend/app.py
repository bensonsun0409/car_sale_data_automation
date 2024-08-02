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

import logging
app = Flask(__name__)
CORS(app)
matplotlib.use('Agg')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'b03b02019'
app.config['MYSQL_DB'] = 'car_info'

mysql = MySQL(app)
# logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s', filename='app.log')



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

def generate_plot(dataframe, x_col, y_col, title):
    if dataframe is None or dataframe.empty:
        return None
    
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(dataframe[x_col], dataframe[y_col], marker='o')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(title)
        plt.grid(True)
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        return base64.b64encode(img.getvalue()).decode('utf-8')
    except Exception as e:
        app.logger.error(f"Plot generation error: {str(e)}")
        return None

@app.route('/search', methods=['POST'])
def search():
    
        filters = request.json
        start_date = filters.get('startDate')
        end_date = filters.get('updateDate')
        car_brand = filters.get('carBrand')
        production_year = filters.get('productionYear')
        lowMilage = filters.get('lowMilage')
        highMilage = filters.get('highMilage')
        video = filters.get('video')

        queries = {
            "average_price": """
                SELECT startDate, AVG(price) as avg_price 
                FROM car_info.car_data 
                WHERE startDate >= %s AND startDate <= %s
            """,
            "listing_count": """
                SELECT startDate, COUNT(*) as listing_count 
                FROM car_info.car_data 
                WHERE startDate >= %s AND startDate <= %s
            """
        }

        params = [start_date, end_date]

        if production_year:
            for key in queries:
                queries[key] += " AND productionYear in (%s)"
            params.append(production_year)

        if car_brand:
            for key in queries:
                queries[key] += " AND brand in (%s)"
            params.append(car_brand)
        if lowMilage and highMilage:
            for key in queries:
                queries[key] += f"AND milage >= {lowMilage} and milage <= {highMilage}"
        
        if video:
            for key in queries:
                queries[key] += f'AND video = "Y" '

        for key in queries:
            queries[key] += " GROUP BY startDate ORDER BY startDate"

        images = {}
        for key, query in queries.items():
            try:
                df = fetch_data(query, tuple(params))
                df['startDate'] = pd.to_datetime(df['startDate'])
                print(df)
                if key == "average_price":
                    image = generate_plot(df, 'startDate', 'avg_price', 'Average Price by Start Date')
                elif key == "listing_count":
                    image = generate_plot(df, 'startDate', 'listing_count', 'Listing Count by Start Date')
                else:
                    continue
                images[key] = image
            except Exception as e:
                logging.error("Error in handle_queries: %s", e)
                return jsonify({"success": False, "message": str(e)})
        return jsonify({"success": True, "images": images})

