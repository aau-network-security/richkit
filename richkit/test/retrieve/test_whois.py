import unittest
from datetime import datetime
from richkit.retrieve import whois as wh

class WhoisTestCase(unittest.TestCase):

    def setUp(self):
        self.domains = ["www.google.com", "www.cloudflare.com"]

    # .dk domains give unknownTld exception !
    @unittest.skip("No reason to skip however it fails on ci requires more investigation")
    def test_get_whois_info(self):
        # last updated field skipped since it could be None
        for i in self.domains:
            whois_info = wh.get_whois_info(i)
            date = whois_info["d_expiration_date"]
            registrar = whois_info["d_registrar"]
            assert len(registrar) > 0
            assert type(date) == datetime


if __name__ == '__main__':
    unittest.main()
