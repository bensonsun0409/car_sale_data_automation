from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from sqlalchemy import create_engine
import re
driver = webdriver.Chrome()
url = f'https://auto.8891.com.tw/usedauto-infos-3971412.html?display__sale_code=3010013&flow_id=f1718133-549a-4e7e-b0f8-05f48e1e5250'
driver.get(url)


title = driver.find_element(By.CLASS_NAME, 'breadcrumb')
link = title.find_elements(By.CLASS_NAME,'NormalLink')
print(link[2].text)
print(link[3].text)

input_string = driver.find_element(By.XPATH, '//*[@id="infos-ab-flag"]/div').text

match = re.search(r'編號：(S\d+)', input_string)
print(match.group(1))

