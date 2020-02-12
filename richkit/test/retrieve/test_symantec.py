from richkit.retrieve.symantec import read_categorized_file

import unittest

from pathlib import Path

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
