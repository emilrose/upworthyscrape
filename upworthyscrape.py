import json
import datetime
import csv
import os.path
import pickle

import requests
from bs4 import BeautifulSoup
import scrapehelper

def get_features(url, category, csvwriter):
    try:
        # Grab data out of the URL
        header_dict, article_content = get_content_for_url(url)
        pub_year = header_dict['nuggetYear']
        pub_month_day = header_dict['nuggetDate']
        pub_date = convert_date(pub_year, pub_month_day)
        day_of_week = datetime.date.isoweekday(pub_date)

        # Use the data for features: every variable after this comment is a feature to be written to the CSV
        date_published = (datetime.date.today() - pub_date).days
        # We don't use data from articles that are less than a week old
        if date_published < 7:
            return

        num_tokens_title = len(header_dict['title'].split())
        num_tokens_body = num_words_in_body(article_content)

        num_hrefs, num_self_hrefs = num_links(article_content)
        num_videos = num_videos_in_article(article_content)
        num_imgs, num_gifs = num_images_gifs(article_content)

        is_promoted = int(header_dict['isPromoted'])  # Cast the booleans to int
        is_sponsored = int(header_dict['isSponsored'])

        (day_is_monday, day_is_tuesday, day_is_wednesday, day_is_thursday, day_is_friday, day_is_saturday,
            day_is_sunday) = set_day(day_of_week)
        is_weekend = day_is_weekend(day_of_week)

        (is_democracy, is_diversity, is_economics, is_environment, is_health, is_humanity,
            is_justice, is_science) = set_category(category)

        num_likes_shares = calc_num_likes_shares(url)

        feature_list = [url, date_published, num_tokens_title, num_tokens_body, num_hrefs, num_self_hrefs,
                        num_videos, num_imgs, num_gifs, is_promoted, is_sponsored, day_is_monday,
                        day_is_tuesday, day_is_wednesday, day_is_thursday, day_is_friday, day_is_saturday,
                        day_is_sunday, is_weekend, is_democracy, is_diversity, is_economics, is_environment,
                        is_health, is_humanity, is_justice, is_science, num_likes_shares]

        csvwriter.writerow(feature_list)
    except Exception as e:
        print(e)


def get_content_for_url(url):
    page = requests.get(url)
    page_html = BeautifulSoup(page.text)

    main_html = page_html.find('div', {'id': 'nuggetPage'}).extract()

    header_dict = json.loads(page_html.find('div', {'class': 'row nugget-header'}).div['data-react-props'])
    article_content = main_html.find('div', {'id': 'nuggetBody'}).extract()

    return header_dict, article_content


def convert_date(year, month_day):
    year = int(year)
    l = month_day.split()
    month = convert_month(l[0])
    day = int(l[1])
    return datetime.date(year, month, day)


# We use the Facebook API to obtain likes and shares
def calc_num_likes_shares(url):
    url_without_https = url[:4] + url[5:]  # Must change the url to http://... from https://... for FB API
    likes_shares_xml = requests.get("https://api.facebook.com/method/fql.query?query=select%20total_count,like_count,"
                                    "comment_count,share_count,click_count%20from%20link_stat%"
                                    "20where%20url=%27{0}%27&format=xml".format(url_without_https))
    soup = BeautifulSoup(likes_shares_xml.text)
    likes_shares = int(soup.find('total_count').contents[0])
    return likes_shares


def num_images_gifs(article_content):
    article_images_gifs = article_content.find_all('img')
    num_gifs = num_images = 0
    for item in article_images_gifs:
        if "gif" in str(item):
            num_gifs += 1
        else:
            num_images += 1
    return num_images, num_gifs


def num_videos_in_article(article_content):
    iframe_tags = article_content.find_all('iframe')
    return len(iframe_tags)


def num_links(article_content):
    links = 0
    links_to_upworthy = 0
    a_tags = article_content.find_all('a')
    for tag in a_tags:
        if tag.has_attr('href'):
            links += 1
            if "upworthy" in str(tag):
                links_to_upworthy += 1
    return links, links_to_upworthy


def num_words_in_body(article_content):
    return len(article_content.get_text().split())


def convert_month(month):
    if month == "January":
        return 1
    elif month == "February":
        return 2
    elif month == "March":
        return 3
    elif month == "April":
        return 4
    elif month == "May":
        return 5
    elif month == "June":
        return 6
    elif month == "July":
        return 7
    elif month == "August":
        return 8
    elif month == "September":
        return 9
    elif month == "October":
        return 10
    elif month == "November":
        return 11
    else:
        return 12


def set_category(category):
    if category == "Democracy":
        return (1, 0, 0, 0, 0, 0, 0, 0)
    elif category == "Diversity and Equality":
        return (0, 1, 0, 0, 0, 0, 0, 0)
    elif category == "Economics":
        return (0, 0, 1, 0, 0, 0, 0, 0)
    elif category == "Environment":
        return (0, 0, 0, 1, 0, 0, 0, 0)
    elif category == "Health":
        return (0, 0, 0, 0, 1, 0, 0, 0)
    elif category == "Humanity and Culture":
        return (0, 0, 0, 0, 0, 1, 0, 0)
    elif category == "Justice":
        return (0, 0, 0, 0, 0, 0, 1, 0)
    else:
        return (0, 0, 0, 0, 0, 0, 0, 1)


def set_day(day_of_week):
    if day_of_week == 1:
        return (1, 0, 0, 0, 0, 0, 0)
    elif day_of_week == 2:
        return (0, 1, 0, 0, 0, 0, 0)
    elif day_of_week == 3:
        return (0, 0, 1, 0, 0, 0, 0)
    elif day_of_week == 4:
        return (0, 0, 0, 1, 0, 0, 0)
    elif day_of_week == 5:
        return (0, 0, 0, 0, 1, 0, 0)
    elif day_of_week == 6:
        return (0, 0, 0, 0, 0, 1, 0)
    else:
        return (0, 0, 0, 0, 0, 0, 1)


def day_is_weekend(day_of_week):
    if day_of_week <= 5:
        return 0
    else:
        return 1


if __name__ == '__main__':
    if not os.path.exists('category_url_list.txt'):
        scrapehelper.create_category_url_list()

    with open('category_url_list.txt', 'rb') as urls_file, open('features.csv', 'w') as csvdata:
        category_url_list = pickle.loads(urls_file.read())
        csvwriter = csv.writer(csvdata, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        feature_names = ['url', 'date_published', 'num_tokens_title', 'num_tokens_body', 'num_hrefs', 'num_self_hrefs',
                         'num_videos', 'num_imgs', 'num_gifs', 'is_promoted', 'is_sponsored', 'day_is_monday',
                         'day_is_tuesday', 'day_is_wednesday', 'day_is_thursday', 'day_is_friday', 'day_is_saturday',
                         'day_is_sunday', 'is_weekend', 'is_democracy', 'is_diversity', 'is_economics',
                         'is_environment', 'is_health', 'is_humanity', 'is_justice', 'is_science', 'num_likes_shares']
        csvwriter.writerow(feature_names)
        for category, url in category_url_list:
            get_features(url, category, csvwriter)
