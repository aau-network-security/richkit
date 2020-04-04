import os

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

    def test_maxmindb_licence_key(self):
        test_license_key = os.environ["TEST_LICENSE_KEY"] = "LICENSEKEY"
        license_key = lookup.maxmindb_licence_key("TEST_LICENSE_KEY")
        non_existing_license_key = lookup.maxmindb_licence_key("NON-EXISTING")
        self.assertTrue(license_key, test_license_key)
        self.assertIs(non_existing_license_key, 'NOLICENSEKEYFOUND')
