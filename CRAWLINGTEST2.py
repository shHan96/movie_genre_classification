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


def save_urls_to_file(start, end, urls):
    filename = f"melo{start}to{end}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\\n')
    return filename


def merge_files(filenames):
    with open('all_movie_urls.txt', 'w', encoding='utf-8') as outfile:
        for fname in filenames:
            with open(fname, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())


def get_all_movies(url):
    # driver.get(url)
    # movie_count = 0
    # movie_urls = []
    # files_created = []
    #
    # # Extend the movie list
    # while movie_count < 3000:
    #     try:
    #         load_more_button = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/button')
    #         load_more_button.click()
    #         time.sleep(1)
    #         movie_count += 30
    #     except NoSuchElementException:
    #         break
    #
    # # Collect all movie URLs without navigating away and save in batches of 100
    # for i in range(1, movie_count + 1):
    #     movie_xpath = f'//*[@id="content"]/div[1]/ul/li[{i}]/a'
    #     try:
    #         movie_element = driver.find_element(By.XPATH, movie_xpath)
    #         movie_urls.append(movie_element.get_attribute('href'))
    #
    #         # Save to file every 100 URLs
    #         if i % 100 == 0:
    #             start = i - 99
    #             end = i
    #             file_created = save_urls_to_file(start, end, movie_urls)
    #             files_created.append(file_created)
    #             movie_urls.clear()
    #     except Exception as e:
    #         print(f"Error collecting URL for movie {i}: {e}")
    #
    # # Save any remaining URLs to file
    # if movie_urls:
    #     start = (i // 100) * 100 + 1
    #     end = i
    #     file_created = save_urls_to_file(start, end, movie_urls)
    #     files_created.append(file_created)

    # Merge all files into one
    #merge_files(files_created)

    driver.quit()


url = 'https://serieson.naver.com/v3/movie/products/melo?sortType=UPDATE_DESC&price=all'
get_all_movies(url)