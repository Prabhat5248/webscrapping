import PyPDF2
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os.path
import sys
import requests
from dateutil.parser import parse
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import io
import urllib.request as urllib2
from PyPDF2 import PdfFileReader
from dateutil.parser import parse

from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--incognito')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
action = ActionChains(driver)
url_list = []
skip_list = []
base_dir = './ournewenglandlegends.com'
count = 1

# driver.maximize_window()
driver.set_window_position(1000, 0)


action = ActionChains(driver)
url_path = pd.read_csv("urls_data2.csv")
url_list = list(url_path['0'])
url_list = list(set(url_list))
len_1 = len(url_list)
print(url_list)
for za in url_list:
    print("Opening Post url number:", str(count) + '/' + str(len_1))
    print(za, 'llllllllllllllllllllll')
    try:
        driver.get(za)
        time.sleep(2)
        title1 = ''
        title = ''
        transcript1 = ''
        transcript = ''
        audio_path = ''
        audio = ''
        post_date = ''
        file_name = ''

        title1 = driver.find_element(By.XPATH, '//h1[@class="title single-title entry-title"]')
        title = title1.text
        title = title.replace("\n", " ")
        print(title, '--------------TITLE')

        file_name = title.replace(" ", "_")
        file_name = file_name.replace("\n", "_")
        if os.path.exists(base_dir + '/' + file_name):
            pass
        else:
            print('&&&&&&&')
            date_ = driver.find_element(By.XPATH, '//span[@class="thetime date updated"]/span')
            date_ = date_.text
            print(date_)
            from dateutil.parser import parse

            date = parse(date, fuzzy=True)
            print(date_, 'parse')
            post_date = datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            print(post_date, "------------------------post_date")
            time.sleep(0.5)

            driver.find_element(By.LINK_TEXT, 'Read the episode transcript.').click()
            time.sleep(2)
            transcript1 = driver.find_element(By.XPATH,
                                              '//div[@class="thecontent"]')
            transcript = transcript1.text
            transcript = transcript.rsplit('EPISODE TRANSCRIPT:', 1)
            transcript = transcript[1]
            print(transcript, '_________________________transcript___________________________')
            try:
                try:
                    iframe = driver.find_element(By.XPATH, '//iframe[@title="Embed Player"]')

                    
                    iframe = iframe.get_attribute('src')
                    print(iframe)
                    driver.get(iframe)
                    time.sleep(2)
                    audio_lnk1 = driver.find_element(By.XPATH, '//*[@id="libsyn-player"]/div[2]/div[2]/div/span[3]/a')

                    audio_lnk = audio_lnk1.get_attribute('href')
                    print('audio +++++++++++++++++++++++++', audio_lnk)
                    text = "audio_file"
                    params = {
                        "ie": "UTF-8",
                        "client": "tw-ob",
                        "q": text,
                        "tl": "en",
                        "total": "1",
                        "idx": "0",
                        "textlen": str(len(text))
                    }
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                    response = requests.get(audio_lnk, headers=headers, params=params, stream=True)
                    with open("output.mp3", "wb") as handle:
                        for data in tqdm(response.iter_content()):
                            handle.write(data)
                except:
                    iframe = driver.find_element(By.XPATH, '//iframe[@loading="lazy"]')
                    iframe = iframe.get_attribute('src')
                    print(iframe)
                    driver.get(iframe)
                    time.sleep(2)
                    audio_lnk = driver.find_element(By.XPATH, '//img[@alt="Download This Episode"]').click()
                    time.sleep(1)
                    for i in range(30, 0, -1):
                        sys.stdout.write("\r")
                        sys.stdout.write("{:2d} seconds remaining.".format(i))
                        sys.stdout.flush()
                        time.sleep(1)
                    time.sleep(3)
                    filepath = '/home/webtunixi5/Downloads'
                    filename = max([filepath + "/" + f for f in os.listdir(filepath)], key=os.path.getctime)
                    print(filename)
                    shutil.move(os.path.join('.', filename), 'output.mp3')

                    print('audio +++++++++++++++++++++++++', audio_lnk)

                print("--------------------------DATA SCRAP SUCCESSFULLY--------------------")

                time.sleep(1)
                os.rename("output.mp3", file_name + ".mp3")

                path = os.path.join(base_dir, file_name)
                os.mkdir(path)
                try:
                    with open(file_name + '_orig.txt', 'w') as f:
                        f.write(transcript)
                except:
                    with open(file_name + '_orig.txt', 'wb') as f:
                        f.write(transcript)
                with open(file_name + '.txt', 'w') as f:
                    for line in title:
                        f.write(line)
                with open(file_name + '_info.txt', 'w') as f:
                    f.write(za + '\n')
                    f.write(post_date)
                print("Scraped transcript data")

                shutil.move(file_name + ".mp3", path + "/" + file_name + ".mp3")
                print('audio moved successful')
                shutil.move(file_name + '_orig.txt', path + '/' + file_name + '_orig.txt')
                shutil.move(file_name + '_info.txt', path + '/' + file_name + '_info.txt')
                shutil.move(file_name + '.txt', path + '/' + file_name + '.txt')
                print("--------------------------DATA MOVE SUCCESSFULLY--------------------")
               
            except Exception as e:

                print(e)
                pass
        driver.close()
        time.sleep(10)
       

    except Exception as e:
        print("++++++++++++++++++")
        pass
    count += 1

