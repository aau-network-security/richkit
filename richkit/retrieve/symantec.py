"""Symantec Web Service

This is generated to get categories of given urls, normally it fetches
category from symantec web service then saves it to local file which
is called `categorized_urls` under `richkit/retrieve/data/`


How to use:

    >>> # Import necesseary functions and make a call as demonstrated given below
    >>> from richkit.retrieve.symantec import fetch_from_internet
    >>> from richkit.retrieve.symantec import LocalCategoryDB
    >>>
    >>> urls = ["www.aau.dk","www.github.com","www.google.com"]
    >>>
    >>> local_db = LocalCategoryDB()
    >>> for url in urls:
    ...     url_category=local_db.get_category(url)
    ...     if url_category=='':
    ...         url_category=fetch_from_internet(url)
    ...     print(url_category)
    Education
    Technology/Internet
    Search Engines/Portals

"""
import ast
import json
import os
from json import dumps
import re
from pathlib import Path
import logging
import requests
from xml.etree.ElementTree import fromstring
from requests.exceptions import HTTPError
from requests.exceptions import InvalidURL
logger = logging.getLogger(__name__)

"""
Configuration
Get one here: http://www1.k9webprotection.com/get-k9-web-protection-free
"""
categories_url = "https://gitlab.com/snippets/1740321/raw"
data_path = Path(os.path.dirname(__file__), 'data')
categories_file_path = data_path / "categories_list.txt"
categorized_urls_file = data_path / "categorized_urls.txt"

k9License = 'Replace_by_your_own_license'


class LocalCategoryDB():
    def __init__(self):

        self.url_to_category = read_categorized_file()

    def get_category(self, url):
        if url in self.url_to_category:
            return self.url_to_category[url]
        else:
            return ''


def fetch_categories(categories_url=categories_url, local_categories_path=categories_file_path):
    """Fetch categories and create local cache """
    if not categories_url:
        return None
    try:
        resp = requests.get(categories_url)
        data = resp.json()
        d = dict([('%02x' % c['num'], c['name']) for c in data])
    except HTTPError as e:
        logger.error('Cannot fetch categories, HTTP error: %s\n' % str(e.code))
    except InvalidURL as e:
        logger.error('Cannot fetch categories, URL error: %s\n' % str(e.reason))
    try:
        f = open(local_categories_path, 'w')
        f.write(dumps(d))
        f.close()
    except Exception as e:
        f.close()
        logger.error('Cannot save categories: %s\n' % e)
    return d


#
def load_categories(name):
    """Load categories from a cache file"""
    if not name:
        return None
    d = {}
    try:
        f = open(name, 'r')
        data = f.read()
        d = ast.literal_eval(data)
        f.close()
    except FileNotFoundError as e:
        return {}
    except OSError as er:
        f.close()
        os.exit(1)
    return d


def check_local_categories_file_exists(categories_file_path=categories_file_path):
    webCats = load_categories(categories_file_path)
    if webCats == {}:
        webCats = fetch_categories(categories_url, categories_file_path)
    return webCats


def _chunks(s):
    # Original: https://github.com/allfro/sploitego/blob/master/src/sploitego/webtools/bluecoat.py
    return [s[i:i + 2] for i in range(0, len(s), 2)]


# if there is no info related with link  then call for api and append it to categorized_url.txt
def write_to_local_file(text, categorized_urls_file=categorized_urls_file):
    with open(categorized_urls_file, 'a') as file:
        file.write(text + "\n")


def fetch_from_internet(url, categories_file_path=categories_file_path, categorized_urls_file=categorized_urls_file):
    result = ''
    hostname = url
    port = '80'
    webservice_endpoint = 'http://sp.cwfservice.net/1/R/%s/K9-00006/0/GET/HTTP/%s/%s///' % (k9License, hostname, port)
    r = requests.get(webservice_endpoint)
    if r.status_code == 200:
        e = fromstring(r.text)
        domc = e.find('DomC')
        dirc = e.find('DirC')
        if domc is not None:
            cats = _chunks(domc.text)
            result = [check_local_categories_file_exists().get(c.lower(), 'Unknown')
                      for c in cats][0]
            write_to_local_file(url + "," + re.sub('\n', '', result), categorized_urls_file)
        elif dirc is not None:
            cats = _chunks(dirc.text)
            logger.debug(
                '%s,%s\n' % (hostname, [check_local_categories_file_exists(categories_file_path).get(c.lower(), 'Unknown') for c in cats][0]))
            result = [check_local_categories_file_exists(
                categories_file_path).get(c.lower(), 'Unknown') for c in cats][0]
            write_to_local_file(url + "," + re.sub('\n', '', result), categorized_urls_file)
        else:
            logger.error('Cannot get category for %s\n' % hostname)

    return re.sub('\n', '', result)


def read_categorized_file():
    url_to_category = dict()
    if not os.path.exists(categorized_urls_file):
        open(categorized_urls_file, 'w').close()
    else:
        with open(categorized_urls_file, "r") as ins:
            for line in ins:
                pair = line.replace('\n', '').split(',')
                url_to_category[pair[0]] = pair[1]

    return url_to_category


def check_for_local(url):
    domains = dict()
    for i in read_categorized_file():
        line = i.split(',')

        if len(line) == 2:
            if line[1] in domains:
                # append tyhhe new number to the existing array at this slot
                if line[0] not in domains[line[1]]:
                    domains[line[1]].append(line[0])
            else:
                # create a new array in this slot
                domains[line[1]] = [line[0]]
    url_belong_to = []
    result = ''
    for index, key in enumerate(domains):
        if url in domains[key]:
            result = key
    return result


def get_index(category):
    for k, v in check_local_categories_file_exists().items():
        if (v == category):
            return k
