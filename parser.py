from turtle import st
from requests import get
from bs4 import BeautifulSoup
import json
import unicodedata
import re

def slugify(value, allow_unicode=False):  # title to valid filename
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def jsonify(url, filter):

    json_array = []

    page = BeautifulSoup(get(url).text, 'lxml')
    products = page.find(id='tab_newreleases_content', class_='tab_content').find_all('a', class_='tab_item')

    for product in products:
        game_page = BeautifulSoup(get(product['href']).text, 'lxml')
        title = game_page.find(id='appHubAppName').get_text()
        body = game_page.find(class_='game_description_snippet').get_text(separator=' ', strip=True)
        filtered = True

        for el in filter:
            if el.lower() not in title.lower() and el.lower() not in body.lower():
                filtered = False
                break

        if filtered:
            splitted = body.split()

            if len(splitted) > 100:
                body = ''
                for i in range(100):
                    body += splitted[i] + ' '
                body = body.rstrip() + '...'
            
            json_array.append({'url': product['href'], 'title': title, 'body': body})

    with open(slugify(url) + '.json', 'w+') as json_file:
        json_file.write(json.dumps(json_array, indent=4))
    

    


filter = []
url = 'https://store.steampowered.com/explore/new/'

jsonify(url, filter)
