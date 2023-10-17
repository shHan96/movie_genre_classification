from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

# Setup
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# Uncomment the line below if you want to run in headless mode
# options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)


def get_movie(url):
    driver.get(url)
    for i in range(2, 6):
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

    description_xpath = f'//*[@id="content"]/div[2]/ul/li[1]/div[{div_index}]/p'
    title_xpath = '//*[@id="content"]/div[2]/div/div[1]/div[1]/strong'
    try:
        title = driver.find_element(By.XPATH, title_xpath).text
        description = driver.find_element(By.XPATH, description_xpath).text
    except Exception as e:
        print(f'Error: {e}')
        return None, None

    return title, description


def get_all_movies(url):
    driver.get(url)
    movie_count = 0
    movie_urls = []

    # Extend the movie list
    while movie_count < 3000:
        try:
            # Click on the "Load More" button
            load_more_button = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/button')
            load_more_button.click()
            time.sleep(1)
            movie_count += 30  # Each click loads 30 more movies
        except NoSuchElementException:
            break

    # Collect all movie URLs without navigating away
    for i in range(1, movie_count + 1):
        movie_xpath = f'//*[@id="content"]/div[1]/ul/li[{i}]/a'
        print(i, end=' ')
        try:
            movie_element = driver.find_element(By.XPATH, movie_xpath)
            movie_urls.append(movie_element.get_attribute('href'))
        except Exception as e:
            print(f"Error collecting URL for movie {i}: {e}")

    # Fetch details for each movie using the collected URLs
    for movie_url in movie_urls:
        title, description = get_movie(movie_url)
        if title and description:
            print(f"Title: {title}")
            print(f"Description: {description}")
            print("=" * 50)

    driver.quit()


url = 'https://serieson.naver.com/v3/movie/products/action?sortType=UPDATE_DESC&price=all'
get_all_movies(url)