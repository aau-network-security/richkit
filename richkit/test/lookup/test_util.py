from richkit.lookup import util
from richkit.lookup.util import MaxMind_CC_DB
from richkit.lookup.util import MaxMind_ASN_DB
ORIG_CC_MASTERURL = MaxMind_CC_DB.MASTERURL
ORIG_ASN_MASTERURL = MaxMind_ASN_DB.MASTERURL

import unittest

from pathlib import Path
from requests.exceptions import ConnectionError

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


class stub_MaxMind_CC_DB(MaxMind_CC_DB):
    """Stub with minimal __init__, to not hit error there."""
    def __init__(self):
        self.path_db = util.maxmind_directory


class MaxMind_CC_DBTestCase(unittest.TestCase):


    def setUp(self):
        MaxMind_CC_DB.MASTERURL = ORIG_CC_MASTERURL

        for el in Path(util.maxmind_directory).glob('*'):
            rm_recursive(el)


    def test_init(self):
        obj = MaxMind_CC_DB()
        self.assertIsNotNone(obj)


    def test_get_db_path(self):
        s = stub_MaxMind_CC_DB()

        # No db present
        p = s.get_db_path()

        self.assertIsNone(p)

        # Single db present
        folder = Path(s.path_db, 'GeoLite2-Country_DUMMYFOLDER_1970')
        folder.mkdir()
        db_file = Path(folder, 'GeoLite2-Country.mmdb')
        db_file.touch()
        p = MaxMind_CC_DB.get_db_path(s)

        self.assertEqual(p, str(db_file))

        # Two dbs present
        folder = Path(s.path_db, 'GeoLite2-Country_DUMMYFOLDER_2040')
        folder.mkdir()
        db_file = Path(folder, 'GeoLite2-Country.mmdb')
        db_file.touch()
        p = MaxMind_CC_DB.get_db_path(s)

        self.assertEqual(p, str(db_file))


    def test_get_db(self):

        # When DNS fails:
        MaxMind_CC_DB.MASTERURL = (
            "https://this_domain_does_not_exist.local"
            "/download/geoip/database/GeoLite2-Country.tar.gz"
        )

        with self.assertRaises(ConnectionError):
            #TODO: Can the error logs from this be supressed from here?
            MaxMind_CC_DB.get_db()

        # When URL is bad
        MaxMind_CC_DB.MASTERURL = ORIG_CC_MASTERURL
        MaxMind_CC_DB.MASTERURL = MaxMind_CC_DB.MASTERURL.replace(
            '?', "THIS_URL_IS_WRONG")

        with self.assertRaises(Exception):
            #TODO: Can the error logs from this be supressed from here?
            MaxMind_CC_DB.get_db()

        # When all is fine:
        MaxMind_CC_DB.MASTERURL = ORIG_CC_MASTERURL
        # Fetch it
        s = stub_MaxMind_CC_DB()
        s.get_db()
        # Check if file is present
        p = s.get_db_path()
        self.assertIsNotNone(p, "get_db did not a path to the db")
        self.assertTrue(Path(p).exists())


class stub_MaxMind_ASN_DB(MaxMind_ASN_DB):
    """Stub with minimal __init__, to not hit error there."""
    def __init__(self):
        self.path_db = util.maxmind_directory


class MaxMind_ASN_DBTestCase(unittest.TestCase):


    def setUp(self):
        MaxMind_ASN_DB.MASTERURL = ORIG_ASN_MASTERURL

        for el in Path(util.maxmind_directory).glob('*'):
            rm_recursive(el)


    def test_init(self):
        obj = MaxMind_ASN_DB()
        self.assertIsNotNone(obj)


    def test_get_db_path(self):
        s = stub_MaxMind_ASN_DB()

        # No db present
        p = s.get_db_path()

        self.assertIsNone(p)

        # Single db present
        folder = Path(s.path_db, 'GeoLite2-ASN_DUMMYFOLDER_1970')
        folder.mkdir()
        db_file = Path(folder, 'GeoLite2-ASN.mmdb')
        db_file.touch()
        p = MaxMind_ASN_DB.get_db_path(s)

        self.assertEqual(p, str(db_file))

        # Two dbs present
        folder = Path(s.path_db, 'GeoLite2-ASN_DUMMYFOLDER_2040')
        folder.mkdir()
        db_file = Path(folder, 'GeoLite2-ASN.mmdb')
        db_file.touch()
        p = MaxMind_ASN_DB.get_db_path(s)

        self.assertEqual(p, str(db_file))


    def test_get_db(self):

        # When DNS fails:
        MaxMind_ASN_DB.MASTERURL = (
            "https://this_domain_does_not_exist.local"
            "/download/geoip/database/GeoLite2-ASN.tar.gz"
        )

        with self.assertRaises(ConnectionError):
            #TODO: Can the error logs from this be supressed from here?
            MaxMind_ASN_DB.get_db()

        # When URL is bad
        MaxMind_ASN_DB.MASTERURL = ORIG_ASN_MASTERURL
        MaxMind_ASN_DB.MASTERURL = MaxMind_ASN_DB.MASTERURL.replace(
            '?', "THIS_URL_IS_WRONG")

        with self.assertRaises(Exception):
            #TODO: Can the error logs from this be supressed from here?
            MaxMind_ASN_DB.get_db()

        # When all is fine:
        MaxMind_ASN_DB.MASTERURL = ORIG_ASN_MASTERURL
        # Fetch it
        s = stub_MaxMind_ASN_DB()
        s.get_db()
        # Check if file is present
        p = s.get_db_path()
        self.assertIsNotNone(p, "get_db did not a path to the db")
        self.assertTrue(Path(p).exists())
