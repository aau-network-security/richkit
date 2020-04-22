import os
from pathlib import Path
from richkit.lookup import util
from richkit import lookup
import unittest


def rm_recursive(pth):
    pth = Path(pth)
    # Recurse
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_recursive(child)
    # Handle current pth
    if pth.is_file():
        pth.unlink()
    else:
        pth.rmdir()


class LookupTestCase(unittest.TestCase):

    def tearDown(self):
        for el in Path(util.maxmind_directory).glob('*'):
            rm_recursive(el)

    def test_country(self):
        country = lookup.country("8.8.8.8")
        self.assertEqual(country, 'US')

    def test_asn(self):
        asn = lookup.asn("8.8.8.8")
        self.assertEqual(asn, 'AS15169')

    def test_registered_country(self):
        registered_country = lookup.registered_country("8.8.8.8")
        self.assertEqual(registered_country, 'US')

    def test_maxmindb_licence_key(self):
        test_license_key = os.environ["TEST_LICENSE_KEY"] = "LICENSEKEY"
        license_key = lookup.maxmindb_licence_key("TEST_LICENSE_KEY")
        non_existing_license_key = lookup.maxmindb_licence_key("NON-EXISTING")
        self.assertTrue(license_key, test_license_key)
        self.assertIs(non_existing_license_key, 'NOLICENSEKEYFOUND')
