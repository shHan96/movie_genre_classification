from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# Chrome driver 설정
options = webdriver.ChromeOptions()
# 필요한 경우, options에 추가 설정을 추가할 수 있습니다. 예: headless 모드 등
# options.add_argument('--headless')

driver = webdriver.Chrome(service=service, options=options)

# 웹 페이지 열기
url = 'https://serieson.naver.com/v2/movie/581381'
#url = 'https://serieson.naver.com/v2/movie/594366'
driver.get(url)

# XPath로 요소의 텍스트 추출
title_xpath = '//*[@id="content"]/div[2]/div/div[1]/div[1]/strong'
#title_xpath = '//*[@id="content"]/div[2]/div/div[1]/div[1]/strong'
description_xpath = '//*[@id="content"]/div[2]/ul/li[1]/div[3]/p'
#description_xpath = '//*[@id="content"]/div[2]/ul/li[1]/div[2]/p'

# 영화 제목과 소개글 추출
try:
    title = driver.find_element(By.XPATH, title_xpath).text
    description = driver.find_element(By.XPATH, description_xpath).text
except Exception as e:
    print(f'Error: {e}')
else:
    # 결과 출력
    print(f'Title: {title}')
    print(f'Description: {description}')

# 드라이버 종료
driver.quit()
