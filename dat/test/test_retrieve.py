import os.path
import unittest
from dat.retrieve.symantec import fetch_from_internet
from dat.retrieve.symantec import fetch_categories
from dat.retrieve.symantec import load_categories
from dat.retrieve.symantec import categories_url

class DatTestCase(unittest.TestCase):

    def test_fetch_categories(self, categories_file_path='../retrieve/data/categories_list.txt'):
        ## make sure that categories url is accessible and fetched correctly
        categories=fetch_categories(categories_url,categories_file_path)
        assert categories != {}
        os.remove(categories_file_path)

    def test_load_categories(self, categories_file_path='../retrieve/data/categories_list.txt'):
        if os.path.isfile(categories_file_path):
             assert load_categories(categories_file_path) != {}
        else:
            assert load_categories(categories_file_path) == {}
        if os.path.isfile(categories_file_path):
            os.remove(categories_file_path)

    def test_fetch_from_internet(self,categories_file_path='../retrieve/data/categories_list.txt', categorized_url_path='../retrieve/data/categorized_urls.txt'):
        domain_categories = {"Search Engines/Portals":["www.bing.com","www.google.com","www.yandex.com"],
                             "Social Networking":["www.facebook.com","www.twitter.com"]}
        for category, url_list in domain_categories.items():
            for url in url_list:
              assert fetch_from_internet(url,categories_file_path,categorized_url_path)==category
        if os.path.isfile(categories_file_path):
            os.remove(categories_file_path)
        os.remove(categorized_url_path)


if __name__ == '__main__':
    unittest.main()
