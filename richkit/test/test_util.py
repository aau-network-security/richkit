from richkit.lookup import util
from richkit.lookup.util import MaxMindDB
import os
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


class stub_MaxMindDB(MaxMindDB):
    """Stub with minimal __init__, to not hit error there."""
    def __init__(self):
        self.path_db = util.maxmind_directory
        self.query = "cc"


class MaxMind_DBTestCase(unittest.TestCase):

    def setUp(self):
        MaxMindDB.MASTERURL = (
                "https://download.maxmind.com/app/geoip_download?"
                "edition_id=GeoLite2-Country&"
                "license_key={license_key}&"
                "suffix=tar.gz"
            ).format(
                license_key=os.environ['MAXMIND_LICENSE_KEY'],
            )

        for el in Path(util.maxmind_directory).glob('*'):
            rm_recursive(el)

    def test_init(self):
        obj = MaxMindDB(MaxMindDB.MASTERURL, "cc")
        self.assertIsNotNone(obj)

    def test_get_db_path(self):
        s = stub_MaxMindDB()

        # No db present
        p = s.get_db_path()
        self.assertIsNone(p)

        # Single db present
        folder = Path(s.path_db, 'GeoLite2-Country_DUMMYFOLDER_1970')
        folder.mkdir()
        db_file = Path(folder, 'GeoLite2-Country.mmdb')
        db_file.touch()
        p = MaxMindDB.get_db_path(s)

        self.assertEqual(p, str(db_file))

        # Two dbs present
        folder = Path(s.path_db, 'GeoLite2-Country_DUMMYFOLDER_2040')
        folder.mkdir()
        db_file = Path(folder, 'GeoLite2-Country.mmdb')
        db_file.touch()
        p = MaxMindDB.get_db_path(s)

        self.assertEqual(p, str(db_file))

    def test_get_db(self):

        # When DNS fails:
        MaxMindDB.MASTERURL = (
            "https://this_domain_does_not_exist.local"
            "/download/geoip/database/GeoLite2-Country.tar.gz"
        )

        with self.assertRaises(ConnectionError):
            #TODO: Can the error logs from this be supressed from here?
            MaxMindDB(MaxMindDB.MASTERURL, "cc").get_db()

        # When URL is bad
        MaxMindDB.MASTERURL = MaxMindDB.MASTERURL.replace(
            '?', "THIS_URL_IS_WRONG")

        with self.assertRaises(Exception):
            #TODO: Can the error logs from this be supressed from here?
            MaxMindDB.get_db()

    def test_is_outdated(self):
        obj = MaxMindDB(MaxMindDB.MASTERURL, "cc")
        assert obj.is_outdated() == False


