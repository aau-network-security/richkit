from richkit.retrieve.symantec import read_categorized_file
from richkit.retrieve.symantec import fetch_from_internet
from richkit.retrieve.symantec import fetch_categories
from richkit.retrieve.symantec import load_categories
from richkit.retrieve.symantec import categories_url
from pathlib import Path
import unittest
import os


CAT_URLS_FILE = 'categorized_urls.txt'
CATEGORIES_FILE_PATH = 'categories_list.txt'


class SymantecTestCase(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        """
        Removes created resources during test phase
        """
        for file in Path('.').glob('*.txt'):
            file.unlink()

    def test_read_categorized_file(self):
        cat_urls_file_path = Path(CAT_URLS_FILE)
        # Read with missing file
        try:
            cat_urls_file_path.unlink()
        except FileNotFoundError:
            pass
        self.assertIsInstance(read_categorized_file(), dict)

        # Read with empty file
        cat_urls_file_path.touch()

        d = read_categorized_file(CAT_URLS_FILE)
        self.assertIsInstance(d, dict)
        self.assertEqual(len(d), 0)

        # Read something already in file
        with open(CAT_URLS_FILE, 'w') as fd:
            fd.writelines([
                'www.example.com,Example'
            ])
        d = read_categorized_file(CAT_URLS_FILE)
        self.assertIsInstance(d, dict)
        self.assertEqual(len(d), 1)
        self.assertEqual(d['www.example.com'], 'Example')

    def test_fetch_categories(self):
        # make sure that categories url is accessible and fetched correctly
        categories = fetch_categories(categories_url, CATEGORIES_FILE_PATH)
        assert categories != {}

    def test_load_categories(self):
        if os.path.isfile(CATEGORIES_FILE_PATH):
            assert load_categories(CATEGORIES_FILE_PATH) != {}
        else:
            assert load_categories(CATEGORIES_FILE_PATH) == {}

    def test_fetch_from_internet(
            self,
            categories_file_path=CATEGORIES_FILE_PATH,
            categorized_url_path=CAT_URLS_FILE
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
        # unlinking CAT_URLS_FILE here, otherwise the len of dict
        # at line 29 (within test_read_categorized_file) will be different
        # it may cause failing that's why unlinking the file here is required.
        os.unlink(CAT_URLS_FILE)


if __name__ == '__main__':
    unittest.main()
