import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle

BASE_URL = "https://www.upworthy.com/"
TIMES_TO_PAGE_DOWN = 0

# "URL_END" means the part after "BASE_URL", e.g. 'democracy' for https://www.upworthy.com/democracy
URL_END_TO_CATEGORY_NAME = {
    'democracy': 'Democracy',
    'diversity-and-equality': 'Diversity and Equality',
    'economics': 'Economics',
    'environment': 'Environment',
    'health': 'Health',
    'humanity-and-culture': 'Humanity and Culture',
    'justice': 'Justice',
    'science-and-technology': 'Science and Technology',
}


def get_category_urls(url_end, category):
    driver = webdriver.Firefox()

    # Load the category's pagerl
    print("Loading urls for category: " + url_end)
    driver.get("https://www.upworthy.com/" + url_end)
    time.sleep(5)

    # Click load more
    driver.find_element_by_xpath("//a[@class='load-more']").click()
    time.sleep(2)

    # Page down many times to load more articles
    elem = driver.find_element_by_tag_name("body")
    times_to_page_down = TIMES_TO_PAGE_DOWN
    while times_to_page_down:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        times_to_page_down -= 1

    # Grab all the URLS of articles that are relevant to the current category
    # Upworthy shows some articles from other categories in each category; we don't include those
    # Category information is not actually shown on article pages themselves, so we must note the category here
    print("Grabbing URLS")
    url_elements = driver.find_elements_by_xpath("//*[@href][./../../div[1]/text()='{0}']".format(category))
    category_url_list = [] # list of category-url tuples
    for element in url_elements:
        url = element.get_attribute("href")
        url_minus_end = url[:-3]  # Cut out the "?c=" at the end of URLs
        category_url_list.append((category, url_minus_end))

    driver.close()
    return category_url_list

def create_category_url_list():
    category_url_list = []
    for url_end, category in URL_END_TO_CATEGORY_NAME.items():
        category_url_list.append(get_category_urls(url_end, category))
    category_url_list = [item for sublist in category_url_list for item in sublist] # flatten list
    with open('category_url_list.txt', 'wb') as handle:
        pickle.dump(category_url_list, handle)


