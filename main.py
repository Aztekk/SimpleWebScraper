import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import string
import os
import re

"""
This simple parcer saves all articles from page https://www.nature.com/nature/articles with chosen type
and places them to different folders, according to pagination
"""

# Translate rules for filename
space_to_line = str.maketrans(' ', '_')
remove_punctuation = str.maketrans('', '', string.punctuation)

# Input rules
pages = int(input('Enter number of pages: '))
type_articles = input('Enter type of articles: ')

for page in range(1, pages + 1):
    # Creates folder for articles and moves there
    os.mkdir('Page_{n}'.format(n=page))
    os.chdir('Page_{n}'.format(n=page))

    url = 'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={}'.format(page)
    response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    parsed_url = urlparse(response.url)

    base_url = parsed_url.scheme + '://' + parsed_url.netloc

    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')

    # Processes each article, extracts the content to specific folder
    for article in articles:
        article_type = article.find('span', {'data-test': 'article.type'}).find('span').text
        if article_type == type_articles:
            description = article.find('a', {"data-track-action": "view article"}).text.strip()
            file_name = description.translate(remove_punctuation).translate(space_to_line) + '.txt'

            link_url = parsed_url.scheme + '://' + parsed_url.netloc + \
                article.find('a', {"data-track-action": "view article"})['href']

            link_response = requests.get(link_url)
            link_soup = BeautifulSoup(link_response.content, 'html.parser')
            article_body = link_soup.find('div', {'class': re.compile("body")})
            article_body_text = article_body.text

            file = open(file_name, 'wb')
            file.write(article_body_text.encode('utf-8'))
            file.close()
    os.chdir('..')
print('Saved all articles.')
