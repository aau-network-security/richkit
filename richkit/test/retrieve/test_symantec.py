from richkit.retrieve.symantec import read_categorized_file
from richkit.retrieve.symantec import fetch_from_internet
from richkit.retrieve.symantec import fetch_categories
from richkit.retrieve.symantec import load_categories
from richkit.retrieve.symantec import categories_url

import unittest

from pathlib import Path
import os.path


DATA_FOLDER = Path('richkit/retrieve/data')
CAT_URLS_FILE = DATA_FOLDER / 'categorized_urls.txt'


class SymantecTestCase(unittest.TestCase):

    def setUp(self):
        self.assertTrue(DATA_FOLDER.is_dir())

    @classmethod
    def tearDownClass(cls):
        try:
            CAT_URLS_FILE.unlink()
        except FileNotFoundError:
            pass

    def test_read_categorized_file(self):

        # Read with missing file
        try:
            CAT_URLS_FILE.unlink()
        except FileNotFoundError:
            pass
        self.assertIsInstance(read_categorized_file(), dict)

        # Read with empty file
        CAT_URLS_FILE.unlink()
        CAT_URLS_FILE.touch()
        d = read_categorized_file()
        self.assertIsInstance(d, dict)
        self.assertEqual(len(d), 0)

        # Read something already in file
        CAT_URLS_FILE.unlink()
        with open(CAT_URLS_FILE, 'w') as fd:
            fd.writelines([
                'www.example.com,Example'
            ])
        d = read_categorized_file()
        self.assertIsInstance(d, dict)
        self.assertEqual(len(d), 1)
        self.assertEqual(d['www.example.com'], 'Example')

    def test_fetch_categories(self, file_path='categories_list.txt'):
        # make sure that categories url is accessible and fetched correctly
        categories = fetch_categories(categories_url, file_path)
        assert categories != {}
        os.remove(file_path)

    def test_load_categories(self, categories_file_path='categories_list.txt'):
        if os.path.isfile(categories_file_path):
            assert load_categories(categories_file_path) != {}
        else:
            assert load_categories(categories_file_path) == {}
        if os.path.isfile(categories_file_path):
            os.remove(categories_file_path)

    def test_fetch_from_internet(
            self,
            categories_file_path='categories_list.txt',
            categorized_url_path='categorized_urls.txt'
    ):
        domain_categories = {
            "Search Engines/Portals": [
                "www.bing.com",
                "www.google.com",
                "www.yandex.com"
            ],
            "Social Networking": [
                "www.facebook.com",
                "www.twitter.com"
            ]
        }
        for category, url_list in domain_categories.items():
            for url in url_list:
                assert fetch_from_internet(
                    url, categories_file_path, categorized_url_path
                ) == category
        if os.path.isfile(categories_file_path):
            os.remove(categories_file_path)
        os.remove(categorized_url_path)


if __name__ == '__main__':
    unittest.main()
