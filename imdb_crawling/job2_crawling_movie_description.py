import re
import sys
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

#  install chrome driver
while True:  # infinite loop for 'FileNotFoundError'
    try:
        with open('../chrome_driver_path.txt', 'r') as f_driverPath:
            service = Service(executable_path=f_driverPath.read())
    except FileNotFoundError:
        try:
            with open('job1_install_chrome_driver.py', 'r') as f_install:
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

categories = ['Action', 'Comedy', 'Documentary', 'Drama', 'Romance', 'Thriller']

min_movie_cnt = sys.maxsize
for category_idx in range(len(categories)):
    url = f'https://www.imdb.com/search/title/?title_type=movie&genres={categories[category_idx].lower()}&start=1&explore=genres&ref_=adv_prv'
    driver.get(url)

    movie_cnt = int(''.join(re.findall('\d', driver.find_element(By.XPATH, '//*[@id="sidebar"]/div[3]/table/tbody/tr[1]/td[1]').text)))
    if movie_cnt < min_movie_cnt:
        min_movie_cnt = movie_cnt

MOVIE_CNT_IN_PAGE = 50
df_description = pd.DataFrame()
for category in categories:
    refined_descriptions = []

    cur_movie_idx = 1
    while cur_movie_idx <= min_movie_cnt:
        url = (f'https://www.imdb.com/search/title/?title_type=movie&genres={category.lower()}&start={cur_movie_idx}'
               f'&explore=genres&ref_=adv_prv')
        driver.get(url)

        for div_idx in range(MOVIE_CNT_IN_PAGE):
            try:
                description = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[3]/div/div[{div_idx}]/div[3]/p[2]').text
            except NoSuchElementException:
                continue
            refined_description = re.compile('[^a-z|A-Z]').sub(' ', description)
            refined_descriptions.append(refined_description)

        cur_movie_idx += MOVIE_CNT_IN_PAGE

    df_section_description = pd.DataFrame(refined_descriptions, columns=['description'])
    df_section_description['category'] = category
    df_description = pd.concat([df_description, df_section_description], axis='rows', ignore_index=True)
    df_section_description.to_csv(f'./crawling_data/temp_{category}_movie_description.csv', index=False)
df_description.to_csv('./crawling_data/all_movie_descriptions.csv', index=False)
