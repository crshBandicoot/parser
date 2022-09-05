from requests import get
from bs4 import BeautifulSoup
import json
import unicodedata
import re


def slugify(value, allow_unicode=False): #title to valid filename
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def jsonify(url, filter):

    page = BeautifulSoup(get(url).text, 'lxml')
    title = page.find(id='firstHeading').get_text()
    body = page.find(id='bodyContent').find('p').find_next_sibling('p').get_text()
    filtered = True

    for el in filter:
        if el.lower() not in title.lower() and el.lower() not in body.lower():
            filtered = False
            break
    
    if filtered:
        with open(slugify(title) + '.json', 'w') as json_file:
            json.dump({'url': url, 'title': title, 'body': body[0:100]+'...'}, json_file, indent=4)
    

filter = ['rock band', 'Lemmy']
url = 'https://en.wikipedia.org/wiki/Mot%C3%B6rhead'

jsonify(url, filter)


