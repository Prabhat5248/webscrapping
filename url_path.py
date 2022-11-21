from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import docx2txt
import pandas as pd
import textract
from selenium import webdriver
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
driver = webdriver.Chrome(ChromeDriverManager().install())
url ='https://ournewenglandlegends.com/?s=podcast'

action = ActionChains(driver)
url_list = []

try:
    driver.get(url)
    time.sleep(3)
    count=1

    for page in range(40):
        podcast = driver.find_elements(By.XPATH, '//h2[@class="title front-view-title"]/a')
        for x in podcast:
            links=x.get_attribute('href')
            print(count,'>>',links,'podcast_link')
            url_list.append(links)
            count = count + 1
        qq1=driver.find_element(By.XPATH, '//a[@class="next page-numbers"]')
        qq=qq1.get_attribute('href')
        print(qq,'-------------next page-------------')
        driver.get(qq)
        time.sleep(3)

except Exception as e:
    print(e,'0000000000000')
    pass
print(len(url_list),'???????????????????????????????????????????')
data_list=set(url_list)
print(len(data_list), "final....#####")
df = pd.DataFrame(data_list)
df.to_csv('urls_data2.csv')