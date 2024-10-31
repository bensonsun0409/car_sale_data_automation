import requests
from bs4 import BeautifulSoup
import re
import time
import logging

class CarDealerScraper:
    def __init__(self):

        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.8891.com.tw/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

    def scrape_dealers(self, url):
        response = self.session.get(url, headers=self.headers)

        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                buz_list_items = soup.find_all('div', class_='buz-list-view')

            titles, links, ratings, rating_counts = [], [], [], []
            in_stocks, in_stores, view_counts = [], [], []

            for item in buz_list_items:
                dealer_info = self._parse_dealer_item(item)
                if dealer_info:
                    titles.append(dealer_info['標題'])
                    links.append(dealer_info['連結'])
                    ratings.append(dealer_info['評分'])
                    rating_counts.append(dealer_info['評價數量'])
                    in_stocks.append(dealer_info['在庫數量'])
                    in_stores.append(dealer_info['在店數量'])
                    view_counts.append(dealer_info['瀏覽數'])

            return titles, links, ratings, rating_counts, in_stocks, in_stores, view_counts
        except Exception as e:
            logging.info(e)
            return [], [], [], [], [], [], []
        # return titles, links, ratings, rating_counts, in_stocks, in_stores, view_counts
        else:
            raise RequestError(f"無法獲取網頁內容, 狀態碼: {response.status_code}", response)

    def _parse_dealer_item(self, item):
        name_span = item.find('span', class_='fl mr5')
        if not name_span:
            return None

        link = name_span.find('a')
        if not link:
            return None

        title = link.get('title')
        href = link.get('href')

        rating, rating_count = self._parse_rating(item)
        in_stock, in_store = self._parse_stock(item)
        view_count = self._parse_view_count(item)

        return {
            "標題": title,
            "連結": href,
            "評分": rating,
            "評價數量": rating_count,
            "在庫數量": in_stock,
            "在店數量": in_store,
            "瀏覽數": view_count
        }

    def _parse_rating(self, item):
        rating_div = item.find('div', class_='rating-star-total')
        if not rating_div:
            return None, None

        rating_span = rating_div.find('span', class_='c404040')
        rating = rating_span.text if rating_span else None

        rating_num_span = rating_div.find('span', class_='rating-num')
        rating_count = None
        if rating_num_span:
            match = re.search(r'\d+', rating_num_span.text)
            rating_count = match.group() if match else None

        return rating, rating_count

    def _parse_stock(self, item):
        stock_li = item.find('li', class_='stock')
        if not stock_li:
            return None, None

        stock_spans = stock_li.find_all('span', class_='stock-value')
        in_stock = stock_spans[0].text if len(stock_spans) > 0 else None
        in_store = stock_spans[1].text if len(stock_spans) > 1 else None

        return in_stock, in_store

    def _parse_view_count(self, item):
        view_count_span = item.find('span', style="color: #333;")
        return view_count_span.text if view_count_span else None

    def total_counts(self, url):

        response = self.session.get(url, headers=self.headers)


        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            total_data = soup.find('span', style="color:#C00;")


            return int(total_data.text) if total_data else 0
        else:
            raise RequestError(f"無法獲取網頁內容, 狀態碼: {response.status_code}", response)


class RequestError(Exception):
    def __init__(self, message, response):
        super().__init__(message)
        self.response = response
