# import requests
# from bs4 import BeautifulSoup
# import re
#
# # 目標網頁 URL
# url = "https://www.8891.com.tw/findBuz-index.html"
#
# # 發送 GET 請求獲取網頁內容
# response = requests.get(url)
#
# # 確保請求成功
# if response.status_code == 200:
#     # 使用 BeautifulSoup 解析 HTML
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # 找到所有的車廠列表項
#     buz_list_items = soup.find_all('div', class_='buz-list-view')
#
#     for item in buz_list_items:
#         # 找到車廠名稱和連結
#         name_span = item.find('span', class_='fl mr5')
#         if name_span:
#             link = name_span.find('a')
#             if link:
#                 title = link.get('title')
#                 href = link.get('href')
#
#                 # 尋找評分
#                 rating_div = item.find('div', class_='rating-star-total')
#                 if rating_div:
#                     rating_span = rating_div.find('span', class_='c404040')
#                     rating = rating_span.text if rating_span else None
#
#                     # 尋找評價數量
#                     rating_num_span = rating_div.find('span', class_='rating-num')
#                     rating_count = rating_num_span.text if rating_num_span else None
#                     if rating_count:
#                         rating_count = re.search(r'\d+', rating_count).group()
#                 else:
#                     rating = None
#                     rating_count = None
#
#                 # 尋找在庫和在店數量
#                 stock_li = item.find('li', class_='stock')
#                 if stock_li:
#                     stock_spans = stock_li.find_all('span', class_='stock-value')
#                     in_stock = stock_spans[0].text if len(stock_spans) > 0 else None
#                     in_store = stock_spans[1].text if len(stock_spans) > 1 else None
#                 else:
#                     in_stock = None
#                     in_store = None
#
#                 # 尋找瀏覽數
#                 view_count_span = item.find('span', style="color: #333;")
#                 view_count = view_count_span.text if view_count_span else None
#
#                 print(f"標題: {title}")
#                 print(f"連結: {href}")
#                 print(f"評分: {rating}")
#                 print(f"評價數量: {rating_count}")
#                 print(f"在庫數量: {in_stock}")
#                 print(f"在店數量: {in_store}")
#                 print(f"瀏覽數: {view_count}")
#                 print("------------------------")
# else:
#     print("無法獲取網頁內容")


# scrape_example.py
from DownloadHelper.CarPageHelper import CarDataScraper
from DownloadHelper.CarDealerScraper import CarDealerScraper
from DownloadHelper.CarDealerHelper import WebScraper

def main():
    url = "https://www.8891.com.tw/findBuz-index.html"
    # url = "https://www.8891.com.tw/findBuz-index.html?firstRow=30&totalRows=2199&"
    scraper = CarDealerScraper()
    total_data = scraper.total_counts(url)
    print(total_data)
    current_value = 0
    all_titles = []
    all_links = []
    all_ratings = []
    all_rating_counts = []
    all_in_stocks = []
    all_in_stores = []
    all_view_counts = []
    if total_data % 30 == 0:
        while current_value < total_data:
            print(current_value)
            url = f'https://www.8891.com.tw/findBuz-index.html?firstRow={current_value}&totalRows={total_data}&'
            titles, links, ratings, rating_counts, in_stocks, in_stores, view_counts = scraper.scrape_dealers(url)
            # 將新的數據添加到對應的列表中
            all_titles.extend(titles)
            all_links.extend(links)
            all_ratings.extend(ratings)
            all_rating_counts.extend(rating_counts)
            all_in_stocks.extend(in_stocks)
            all_in_stores.extend(in_stores)
            all_view_counts.extend(view_counts)
            current_value += 30
    else:
        while current_value <= total_data:
            print(current_value)
            url = f'https://www.8891.com.tw/findBuz-index.html?firstRow={current_value}&totalRows={total_data}'
            titles, links, ratings, rating_counts, in_stocks, in_stores, view_counts = scraper.scrape_dealers(url)

            # 將新的數據添加到對應的列表中
            all_titles.extend(titles)
            all_links.extend(links)
            all_ratings.extend(ratings)
            all_rating_counts.extend(rating_counts)
            all_in_stocks.extend(in_stocks)
            all_in_stores.extend(in_stores)
            all_view_counts.extend(view_counts)

            current_value += 30
    # titles, links, ratings, rating_counts, in_stocks, in_stores, view_counts = scraper.scrape_dealers(url)
    #
    # 打印結果
    print(f'車行總數{len(all_titles)}')
    for i in range(len(all_titles)):
        print(f"標題: {all_titles[i]}")
        print(f"連結: {all_links[i]}")
        print(f"評分: {all_ratings[i]}")
        print(f"評價數量: {all_rating_counts[i]}")
        print(f"在庫數量: {all_in_stocks[i]}")
        print(f"在店數量: {all_in_stores[i]}")
        print(f"瀏覽數: {all_view_counts[i]}")
        print("------------------------")

    all_car_data = []
    all_car_data2 = []
    for url in all_links:
        scraper = WebScraper()
        car_data = scraper.scrape_data(url)
        if car_data:
            transaction_record, address = car_data
            all_car_data.append(transaction_record)
            all_car_data2.append(address)
            print(f"Processed URL: {url}")
            print(f"Car Data: {transaction_record}")
            print(f"Car Data: {address}")
        else:
            print("未找到所需數據")
    print(len(all_links))
    print(len(all_car_data))
    print(len(all_car_data2))


    # 您可以在這裡進行更多的數據處理
    # 例如：計算平均評分
    valid_ratings = [float(r) for r in all_ratings if r is not None]
    avg_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0
    print(f"平均評分: {avg_rating:.2f}")

    # 找出瀏覽數最高的經銷商
    max_view_count = max([int(vc) for vc in all_view_counts if vc is not None], default=0)
    max_view_index = all_view_counts.index(str(max_view_count))
    print(f"瀏覽數最高的經銷商: {all_titles[max_view_index]} (瀏覽數: {max_view_count})")


if __name__ == "__main__":
    main()
