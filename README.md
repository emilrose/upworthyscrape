Scrapes the articles on the website upworthy.com for data, with the goal of using the input features to predict the sum of Facebook shares and likes. I wrote this for a machine learning project. 28 features are created by default, as described below.
 
It would be easy to gather more features, especially using the "article_content" variable found in get_features().

Tested in Python 2.7 and 3.4.

To run:
$ pip install -r ./requirements.txt
$ python upworthyscrape.py

This will generate a category and url list if one does not exist (i.e. no 'category_url_list.txt' file in the current directory) using scrape.py. It will then generate a CSV data file, 'features.csv'.

A copy of the dataset is included, containing articles published on September 20th or prior.
 
Note that "TIMES_TO_PAGE_DOWN" in scrapehelper can be modified to change the number of articles scraped.

Features:
0. url: URL of the article (non-predictive)
1. data_published: Number representing how many days have passed between the time the article was published and 09/26/2015
2. num_tokens_title: Number of words in the title
3. num_tokens_content: Number of words in the content
4. num_hrefs: Number of links
5. num_self_hrefs: Number of links to other articles published by Upworthy
6. num_videos: Number of videos
7. num_imgs: Number of images
8. num_gifs: Number of gifs
9. is_promoted: Is the article promoted content?
10. is_sponsored: Is the article sponsored content?
11. day_is_monday: Was the article published on a Monday?
12. day_is_tuesday: Was the article published on a Tuesday?
13. day_is_wednesday: Was the article published on a Wednesday?
14. day_is_thursday: Was the article published on a Thursday?
15. day_is_friday: Was the article published on a Friday?
16. day_is_saturday: Was the article published on a Saturday?
17. day_is_sunday: Was the article published on a Sunday?
18. is_weekend: Was the article published on the weekend?
19. is_democracy: Is the article in the Democracy category?
20. is_diversity: Is the article in the Diversity and Equality category?
21. is_economics: Is the article in the Economics category?
22. is_environment: Is the article in the Environment category?
23. is_health: Is the article in the Health category?
24. is_humanity: Is the article in the Humanity and Culture category?
25. is_justice: Is the article in the Justice category?
26. is_science: Is the article in the Science and Technology category?
27. num_likes_shares: Combined numbers of likes and shares (target)
