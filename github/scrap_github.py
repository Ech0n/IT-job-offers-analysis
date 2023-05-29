from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import re
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

def scrap(url):
    driver = webdriver.Chrome()

    driver.get(url)

    while(True):
        try:

            button = driver.find_element(By.CLASS_NAME, "ajax-pagination-btn")
            button.click()
            sleep(2)
        except NoSuchElementException:
            break
        
    topics_list = []

    titles = driver.find_elements(By.XPATH, "//p[contains(@class, 'f3 lh-condensed mb-0 mt-1 Link--primary')]")
    
    desc = driver.find_elements(By.XPATH, "//p[contains(@class, 'f5 color-fg-muted mb-0 mt-1')]")
    
    elems = driver.find_elements(By.XPATH, "//a[contains(@class, 'no-underline flex-grow-0')]")
    i = 0
    for elem in elems:
        href = elem.get_attribute('href')
        if href is not None:
            topic_element = {
                'title' : titles[i].text,
                'desc' : desc[i].text,
                'link' : href,
            }
            topics_list.append(topic_element)
            i += 1
            

            
    for topic in topics_list:
            driver.get(topic['link'])
            sleep(1)
            number_of_repos_s : str = driver.find_element(By.CLASS_NAME, 'h3').text
            number  = "".join(re.findall(r'\d+', number_of_repos_s))

            best_repo = driver.find_element(By.CLASS_NAME, 'wb-break-word').text
            stars = driver.find_element(By.ID, 'repo-stars-counter-star').text
            topic['total_num_of_repos'] = number
            topic['best_repo'] = best_repo
            topic['stars'] = stars
            print(topic)
            sleep(4)

    df = pd.DataFrame(topics_list)
    print(df)
    df.to_csv('github_data.csv')

def main():
    url = 'https://github.com/topics'
    scrap(url)


if __name__ == '__main__':
    main()