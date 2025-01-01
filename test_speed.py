from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
import logging


options = Options()
options.add_argument('--disable-gpu')

url = f"https://auto.8891.com.tw/usedauto-infos-4104122.html?display__sale_code=&flow_id=4e5505ad-8b92-40e3-a781-bea9b2f28039%202024-11-17%2006:46:03,925%20-%20INFO%20-%20Number%202921%20car_data%20None"
def myurl(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
            
    car_data = {
        
        'brand': None,
        'model': None,
        'car_id': None,
        'price': None,
        'verify_tag': None,
        'milage': None,
        'ask_num': None,
        '胎壓偵測': None,
        '動態穩定系統': None,
        '防盜系統': None,
        'keyless免鑰系統': None,
        '循跡系統': None,
        '中控鎖': None,
        '剎車輔助系統': None,
        '兒童安全椅固定裝置': None,
        'ABS防鎖死': None,
        '安全氣囊': None,
        '定速系統': None,
        'LED頭燈': None,
        '倒車顯影系統': None,
        '衛星導航': None,
        '多功能方向盤': None,
        '倒車雷達': None,
        '恆溫空調': None,
        '自動停車系統': None,
        '電動天窗': None,
        '真皮/皮革座椅': None
    }           
    try:
        start_time = time.time()
        self.driver.get(url)

        # 等待頁面加載
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-content"))
        )

        car_data = {}
        try:
            title = self.driver.find_element(By.CLASS_NAME, 'breadcrumb')
            link = title.find_elements(By.CLASS_NAME,'NormalLink')
            car_data['brand'] = link[2].text
            car_data['model'] = link[3].text
        except:
            car_data['brand'] = None
            car_data['model'] = None


        try:
            input_string = self.driver.find_element(By.XPATH, '//*[@id="infos-ab-flag"]/div').text
            
            match = re.search(r'編號：(S\d+)', input_string)
            if match:
                car_data['car_id'] = match.group(1)  # 提取品牌 (例如：艾密羅密歐/Alfa Romeo)
                
        except NoSuchElementException:

            car_data['car_id'] = None

        # 提取價格
        try:
            car_data['price'] = None
            myprice = None
            temp_price = self.driver.find_element(By.ID,'price').text
            if temp_price.endswith('萬'):  # 檢查是否包含 "萬"
                temp_price = temp_price[:-1]  # 去掉最後的 "萬"
                myprice = int(float(temp_price) * 10000) 
            else :
                myprice = None
            car_data['price'] = myprice

        except NoSuchElementException:
            car_data['price'] = None

        # 提取驗證狀態
        try:
            verify = self.driver.find_element(By.XPATH,
                                                '//*[@id="main-box"]/div[3]/div[2]/div[3]/ul/li[2]/div[1]').text
            car_data['verify_tag'] = 'Y' if verify != "暫未驗證" else 'N'
        except NoSuchElementException:
            car_data['verify_tag'] = None

        # 提取里程數
        try:
            milage_text= self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[1]/span[1]').text
            car_data['milage']=self.mixed_chinese_to_arabic(milage_text[:-2])
        except NoSuchElementException:
            car_data['milage'] = None

        #提取年齡
        try:
            year_temp= self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[2]/span[1]').text
            car_data['product_year'] = year_temp[:-1]
        except NoSuchElementException:
            car_data['product_year'] = None    

        #提取顏色
        try:
            car_data['color'] = self.driver.find_element(By.XPATH, '//*[@id="main-box"]/div[3]/div[2]/ul/li[3]/span[1]').text
        except NoSuchElementException:
            car_data['color'] = None    



        # 檢查是否有影片
        try:
            self.driver.find_element(By.ID, 'vjs_video_3')
            car_data['video'] = 'Y'
        except NoSuchElementException:
            car_data['video'] = 'N'

        # 提取詢問人數
        try:
            ask = self.driver.find_element(By.XPATH, '//*[@id="new-chat-wrapper"]/div/span').text
            match = re.search(r'\d+', ask)
            car_data['ask_num'] = match.group(0) if match else None
        except NoSuchElementException:
            car_data['ask_num'] = None

        # 提取車輛位置
        try:
            location= self.driver.find_element(By.XPATH,
                                                                '//*[@id="main-box"]/div[3]/div[2]/a/span').text
            car_data['car_location'] = location[3:6]
            #取前六字
        except NoSuchElementException:
            car_data['car_location'] = None

        # 滾動頁面以加載更多內容
        self.driver.execute_script("window.scrollTo(0, 1000);")

        # 提取賣家信息
        try:
            seller = self.driver.find_element(By.ID, 'tpl_show_market_section')
            time.sleep(2)
            seller_text = seller.text.split('\n')
            if seller_text:
                if seller_text[0] == "8891嚴選商家實車 實況 實價":
                    car_data['seller_info'] = seller_text[1]
                else:
                    car_data['seller_info'] = seller_text[0]
        except NoSuchElementException:
            car_data['seller_info'] = None

        # 提取車輛設備
        all_equipment = [
            '胎壓偵測', '動態穩定系統', '防盜系統', 'keyless免鑰系統', '循跡系統', '中控鎖', '剎車輔助系統',
            '兒童安全椅固定裝置', 'ABS防鎖死', '安全氣囊', '定速系統', 'LED頭燈', '倒車顯影系統', '衛星導航',
            '多功能方向盤', '倒車雷達', '恆溫空調', '自動停車系統','電動天窗', '真皮/皮革座椅'
        ]
        equipment_dict = {equipment: 'N' for equipment in all_equipment}

        # 將在列表中的設備標記為 'Y'
        try:
            car_equip = self.driver.find_element(By.ID, 'car-equip')
            equipments = car_equip.find_elements(By.CLASS_NAME, 'has')
            for e in equipments:
                this_equip=e.text
                if this_equip in equipment_dict:
                    equipment_dict[this_equip] = 'Y'
        except NoSuchElementException:
            logging.info("Equipment not found")
        car_data.update(equipment_dict)

        
        
        end_time = time.time()
        # car_data['scrape_time'] = end_time - start_time

        return car_data

    except TimeoutException:
        logging.info(f"Timeout loading page: {url}")
        return car_data
    except Exception as e:
        logging.info(f"Error scraping data from {url}: {str(e)}")
        return car_data

print(myurl(f'https://auto.8891.com.tw/usedauto-infos-4029132.html?display__sale_code=&flow_id=45b8e4b3-4135-4ae0-8fc9-dda7763876bf'))