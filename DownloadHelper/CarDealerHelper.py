import requests
from bs4 import BeautifulSoup
import re
import logging

class WebScraper:

    def extract_car_data(url):
        # 設置 headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.8891.com.tw/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

        try:
            # 發送 GET 請求，包含 headers
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 尋找成交記錄
            rank_score = soup.select_one('span.buz-span-text.rank-score')
            transaction_record = rank_score.text if rank_score else None

            # 尋找商家地址
            address_element = soup.select_one('dl.item:has(dt.key.key_address) dd.value')
            address = address_element.text.strip().split('[')[0] if address_element else None
            location = address[0:3] if address else None
            # 如果兩個值都找到了，返回它們；否則返回 None
            if transaction_record and address:
                return transaction_record, address, location
            elif transaction_record:
                return transaction_record, None, None
            elif address:
                return None, address, location
            else:
                return None, None, None

        except requests.RequestException as e:
            logging.info(f"請求過程中發生錯誤: {str(e)}")
            return None, None
        except Exception as e:
            logging.info(f"爬取過程中發生錯誤: {str(e)}")
            return None, None

    def extract_car_data_second_temp(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # logging.info(f"Page title: {soup.title.string}")

            sales_record = None
            address = None
            location=None
            # 打印所有的 s-bus-box 內容，以便進行詳細分析
            s_bus_boxes = soup.find_all('div', class_='s-bus-box')
            for i, box in enumerate(s_bus_boxes):
                # logging.info(f"\ns-bus-box {i + 1}:")
                # logging.info(box.prettify())

                # 在每個 s-bus-box 中尋找成交積分和賞車地址
                sales_element = box.find(string=lambda text: text and '成交積分' in text)
                if sales_element:
                    logging.info(f"Found sales element: {sales_element}")
                    sales_match = re.search(r'\((\d+)輛\)', sales_element)
                    if sales_match:
                        sales_record = sales_match.group(1)
                        logging.info(f"Extracted sales record: {sales_record}")

                address_element = box.find(string=lambda text: text and '賞車地址' in text)
                if address_element:
                    logging.info(f"Found address element: {address_element}")
                    address_span = address_element.find_next('span', class_='cf00 fb like-a-block')
                    if address_span:
                        address = address_span.text.strip()
                        logging.info(f"Extracted address: {address}")

            # 如果仍然找不到，嘗試更寬鬆的搜索
            if sales_record == None:
                all_text = soup.get_text()
                sales_match = re.search(r'成交積分.*?\((\d+)輛\)', all_text, re.DOTALL)
                if sales_match:
                    sales_record = sales_match.group(1)
                    logging.info(f"Found sales record in full text: {sales_record}")

            if address == None:
                address_match = re.search(r'賞車地址.*?：(.*?)(?:\n|$)', all_text, re.DOTALL)
                if address_match:
                    address = address_match.group(1).strip()
                    logging.info(f"Found address in full text: {address}")
                     
            if(address):
                location = address[0:3]

            return sales_record, address, location

        except requests.RequestException as e:
            logging.info(f"Error fetching the webpage: {e}")
            return None, None, None

    @staticmethod
    def scrape_data(url):
        if url.endswith("index.html"):
            # 如果網址結尾是 index.html，修改成 onSale.html
            modified_url = url.replace("index.html", "onSale.html")
            sales_record, address,location = WebScraper.extract_car_data_second_temp(modified_url)
            return sales_record, address,location
        else:
            sales_record, address, location = WebScraper.extract_car_data(url)
            return sales_record, address, location

# 使用示例
if __name__ == "__main__":
    url = "https://sansin88.8891.com.tw/index.html"
    result = WebScraper.scrape_data(url)
    if result:
        transaction_record, address = result
        logging.info(f"成交記錄: {transaction_record}")
        logging.info(f"商家地址: {address}")
    else:
        logging.info("未找到所需數據")