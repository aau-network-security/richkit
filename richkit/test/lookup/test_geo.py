from richkit import lookup
import unittest


class LookupTestCase(unittest.TestCase):

    def test_country(self):
        country = lookup.country("8.8.8.8")
        assert country == 'US'

    def test_asn(self):
        asn = lookup.asn("8.8.8.8")
        assert asn == 'AS15169'

    def test_registered_country(self):
        registered_country = lookup.registered_country("8.8.8.8")
        assert registered_country == 'US'
