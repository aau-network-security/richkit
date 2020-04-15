import unittest
from datetime import datetime
from richkit.retrieve import whois


class WhoisTestCase(unittest.TestCase):

    # .dk domains give unknownTld exception !
    @unittest.skip("No reason to skip however it fails on ci requires more investigation")
    def test_get_whois_info(self):
        # last updated field skipped since it could be None

        d = "www.google.com"
        w = whois.get_whois_info(d)
        self.assertTrue(len(w['registrar']) > 0)
        # .com uses "thin" WHOIS, so we get expiry from both registry
        # and registrar;
        self.assertTrue(len(w['expiration_date']) == 2)
        self.assertIsInstance(w['expiration_date'][0], datetime)
        self.assertIsInstance(w['expiration_date'][1], datetime)

        d = "www.cloudflare.com"
        w = whois.get_whois_info(d)
        self.assertTrue('registrar' in w)
        self.assertTrue(len(w['registrar']) > 0)
        self.assertTrue('expiration_date' in w)
        # .com uses "thin" WHOIS, so we get expiry from both registry
        # and registrar, but they are equal here, so only one is returned;
        self.assertIsInstance(w['expiration_date'], datetime)


if __name__ == '__main__':
    unittest.main()
