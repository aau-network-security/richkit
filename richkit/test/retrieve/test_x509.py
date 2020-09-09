import unittest
from richkit.retrieve.x509 import unique_apex, unique_sld, unique_tld, get_lcs_apex


class Test_x509(unittest.TestCase):

    def setUp(self):
        self.sans = ['*.google.com', 'mail.google.com',
                     'example.com', 'test.example.dk', 'test_domain.co.uk']

    def test_unique_apex(self):
        assert unique_apex(self.sans) == 4

    def test_unique_tld(self):
        assert unique_tld(self.sans) == 3

    def test_unique_sld(self):
        assert unique_sld(self.sans) == 3

    def test_lcs(self):
        assert get_lcs_apex(self.sans) == 11
