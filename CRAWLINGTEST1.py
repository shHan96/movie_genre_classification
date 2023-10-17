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

def get_movie(url):
    # 웹 페이지 열기
    driver.get(url)

    # '소개' 텍스트를 찾아 해당 div의 인덱스를 결정
    for i in range(2, 6):  # div[2]와 div[3] 사이를 검사
        test_xpath = f'//*[@id="content"]/div[2]/ul/li[1]/div[{i}]/strong'
        try:
            element = driver.find_element(By.XPATH, test_xpath)
            if element.text == '소개':
                div_index = i
                break
        except:
            continue
    else:
        print(f'Error on {url}: Unable to determine the div index')
        return None, None

    # 올바른 description_xpath를 선택
    description_xpath = f'//*[@id="content"]/div[2]/ul/li[1]/div[{div_index}]/p'

    # XPath로 요소의 텍스트 추출
    title_xpath = '//*[@id="content"]/div[2]/div/div[1]/div[1]/strong'

    # 영화 제목과 소개글 추출
    try:
        title = driver.find_element(By.XPATH, title_xpath).text
        description = driver.find_element(By.XPATH, description_xpath).text
    except Exception as e:
        print(f'Error: {e}')
    else:
        # 결과 출력
        return title, description

# 웹 페이지 열기
url = 'https://serieson.naver.com/v3/movie/products/action?sortType=UPDATE_DESC&price=all'
driver.get(url)

# XPath로 요소의 href 속성 값 가져오기
xpath = '//*[@id="content"]/div[1]/ul/li[1]/a'
try:
    element = driver.find_element(By.XPATH, xpath)
    href_value = element.get_attribute('href')
    print(f'href value: {href_value}')
    print(get_movie(href_value))
except Exception as e:
    print(f'Error: {e}')

# 드라이버 종료
driver.quit()
