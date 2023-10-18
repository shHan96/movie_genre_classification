import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

while True:  # infinite loop for 'FileNotFoundError'
    try:
        with open('./chrome_driver_path.txt', 'r') as f_driverPath:
            service = Service(executable_path=f_driverPath.read())
    except FileNotFoundError:
        try:
            with open('./job1_install_chrome_driver.py', 'r') as f_install:
                exec(f_install.read())
        except FileNotFoundError:
            exit(-1)
        continue
    break

options = Options()
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
options.add_argument('user_agent=' + user_agent)

driver = webdriver.Chrome(service=service, options=options)

# categories = ['action', 'horror', 'comedy', 'sf_fantasy', 'drama', 'melo']
categories = ['indie']

df_description = pd.DataFrame()
for category in categories:
    url = 'https://serieson.naver.com/v3/movie/products/' + category
    driver.get(url)

    try:
        while True:
            button_viewMore = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/button')
            button_viewMore.click()
    except NoSuchElementException:
        pass
