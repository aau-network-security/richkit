from richkit.retrieve.symantec import read_categorized_file

import unittest


class SymantecTestCase(unittest.TestCase):

    def test_read_categorized_file(self):
        self.assertIsInstance(read_categorized_file(), dict)
