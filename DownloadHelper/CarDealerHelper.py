import requests
from bs4 import BeautifulSoup

class WebScraper:
    @staticmethod
    def scrape_data(url):
        try:
            # 發送 GET 請求
            response = requests.get(url)
            response.raise_for_status()

            # 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 尋找成交記錄
            rank_score = soup.select_one('span.buz-span-text.rank-score')
            transaction_record = rank_score.text if rank_score else None

            # 尋找商家地址
            address_element = soup.select_one('dl.item:has(dt.key.key_address) dd.value')
            address = address_element.text.strip().split('[')[0] if address_element else None

            # 如果兩個值都找到了，返回它們；否則返回 None
            if transaction_record and address:
                return transaction_record, address
            elif transaction_record:
                return transaction_record, None
            elif address:
                return None, address
            else:
                return None, None

        except Exception as e:
            print(f"爬取過程中發生錯誤: {str(e)}")
            return None, None

# 使用示例
if __name__ == "__main__":
    url = "https://www.8891.com.tw/findBuz-info-201.html"
    result = WebScraper.scrape_data(url)
    if result:
        transaction_record, address = result
        print(f"成交記錄: {transaction_record}")
        print(f"商家地址: {address}")
    else:
        print("未找到所需數據")