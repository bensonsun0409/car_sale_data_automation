import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time


async def get_car_info_async(session, url):
    async with session.get(url) as response:
        html = await response.text()
        # 尝试使用 lxml，如果失败则使用 html.parser
        try:
            soup = BeautifulSoup(html, 'lxml')
        except:
            soup = BeautifulSoup(html, 'html.parser')
        car_info_items = soup.find_all(class_='car-info')
        car_info_data = []
        for item in car_info_items:
            spans = item.find_all('span')
            for span in spans:
                mydata = span.text.strip()
                car_info_data.append(mydata)
        return car_info_data


async def main():
    url = "https://auto.8891.com.tw/usedauto-infos-3948006.html?display__sale_code=3010013&flow_id=fd19fd6f-7c8b-4b40-88a2-a815277a3fd5"
    async with aiohttp.ClientSession() as session:
        start = time.time()
        car_info = await get_car_info_async(session, url)
        end = time.time()
        print(f'Car info: {car_info}')
        print(f'Time taken: {end - start} seconds')

if __name__ == "__main__":
    asyncio.run(main())
