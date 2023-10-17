import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv

# Setup
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# Uncomment the line below if you want to run in headless mode
# options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

def login_if_needed(username, password):
    return
    try:
        id_field = driver.find_element(By.XPATH, '//*[@id="id"]')
        pw_field = driver.find_element(By.XPATH, '//*[@id="pw"]')
        # If found, enter login details
        id_field.send_keys(username)
        pw_field.send_keys(password)
        time.sleep(0.1)
        login_button = driver.find_element(By.XPATH, '//*[@id="log.login"]')
        login_button.click()
        time.sleep(2)
    except Exception as e:
        pass

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
        description = driver.find_element(By.XPATH, description_xpath).text.replace("\n", " ")
    except Exception as e:
        print(f'Error: {e}')
        return None, None
    return title, description

def save_to_csv():
    with open('all_movie_urls.txt', 'r', encoding='utf-8') as file:
        urls = file.read().split("\\n")
    with open('movies_melo_data.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter="`")
        writer.writerow(['Title', 'Description'])
        for idx, url in enumerate(urls):
            #if idx >= 50:
            #    break
            title, description = get_movie(url.strip())
            if title and description:
                writer.writerow([title, description])
    driver.quit()

save_to_csv()
