import sys
#sys.path.extend(['/home/gian/Desktop/git-repos/domain-analysis-toolkit'])
from dat import lookup
import unittest

class LookupTestCase(unittest.TestCase):

    def test_country(self):
        country = lookup.country("8.8.8.8")
        assert country == 'US'

    def test_asn(self):
        asn = lookup.asn("8.8.8.")
        assert asn == 'AS15169'
