import requests
from bs4 import BeautifulSoup
import re

# 目標網頁 URL
url = "https://www.8891.com.tw/findBuz-index.html"

# 發送 GET 請求獲取網頁內容
response = requests.get(url)

# 確保請求成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有的車廠列表項
    buz_list_items = soup.find_all('div', class_='buz-list-view')

    for item in buz_list_items:
        # 找到車廠名稱和連結
        name_span = item.find('span', class_='fl mr5')
        if name_span:
            link = name_span.find('a')
            if link:
                title = link.get('title')
                href = link.get('href')

                # 尋找評分
                rating_div = item.find('div', class_='rating-star-total')
                if rating_div:
                    rating_span = rating_div.find('span', class_='c404040')
                    rating = rating_span.text if rating_span else None

                    # 尋找評價數量
                    rating_num_span = rating_div.find('span', class_='rating-num')
                    rating_count = rating_num_span.text if rating_num_span else None
                    if rating_count:
                        rating_count = re.search(r'\d+', rating_count).group()
                else:
                    rating = None
                    rating_count = None

                # 尋找在庫和在店數量
                stock_li = item.find('li', class_='stock')
                if stock_li:
                    stock_spans = stock_li.find_all('span', class_='stock-value')
                    in_stock = stock_spans[0].text if len(stock_spans) > 0 else None
                    in_store = stock_spans[1].text if len(stock_spans) > 1 else None
                else:
                    in_stock = None
                    in_store = None

                # 尋找瀏覽數
                view_count_span = item.find('span', style="color: #333;")
                view_count = view_count_span.text if view_count_span else None

                print(f"標題: {title}")
                print(f"連結: {href}")
                print(f"評分: {rating}")
                print(f"評價數量: {rating_count}")
                print(f"在庫數量: {in_stock}")
                print(f"在店數量: {in_store}")
                print(f"瀏覽數: {view_count}")
                print("------------------------")
else:
    print("無法獲取網頁內容")