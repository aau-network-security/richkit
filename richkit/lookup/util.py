import requests
import os
import subprocess
import time
from datetime import datetime, timedelta
import logging
from pathlib import Path
import maxminddb

"""
Lookups in the MaxMind GeoLite2 databases.

A license key is required as per [#GeoLite2_CCPA_GDPR]_:

#. Sign up for a MaxMind account (no purchase required): https://www.maxmind.com/en/geolite2/signup
#. Set your password and create a license key: https://www.maxmind.com/en/accounts/current/license-key
#. Setup your download mechanism by using our GeoIP Update program or creating a direct download script: https://dev.maxmind.com/geoip/geoipupdate/#Direct_Downloads

.. rubric:: Footnotes

.. [#GeoLite2_CCPA_GDPR] https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/
"""

logger = logging.getLogger(__name__)
directory = os.getcwd().split("richkit")
maxmind_directory = directory[0] + "/richkit/richkit/lookup/data"
Path(maxmind_directory).mkdir(parents=True, exist_ok=True)


class MaxMindDB:
    """
    This class provides functions to download, extract and get data from MaxMind DBs
    """

    # Dict to lookup const's, structured like this:
    # name given by MaxMind, name of the extracted DB, directory of the downloaded file from MaxMind
    helpers = {
        "asn": ['GeoLite2-ASN_', 'GeoLite2-ASN.mmdb', str(Path(maxmind_directory, "asn.tar.gz"))],
        "cc": ['GeoLite2-Country_', 'GeoLite2-Country.mmdb', str(Path(maxmind_directory, "cc.tar.gz"))]
    }

    def __init__(self, url, query):
        self.MASTERURL = url
        self.query = query
        self.path_db = maxmind_directory
        if MaxMindDB.get_db_path(self) is None:
            MaxMindDB.get_db(self)
        #  weeks = 1 because the database is updated once a week.
        #  if it is downloaded more than one week ago, it will be removed and updated

        if self.get_age() > timedelta(weeks=1):
            os.remove(self.get_db_path())
            MaxMindDB.get_db(self)

    def get_db(self):
        """
        Download the MaxMind database in zip format from the MaxMind website

        """
        logger.debug('Downloading the '+self.helpers[self.query][2]+' DB ... ')
        try:
            response = requests.get(self.MASTERURL, stream=True)
        except Exception as e:
            logger.error('Reraising Exception raised by requests.get ({})'.format(e))
            raise e

        if response.status_code == 200:
            with open(self.helpers[self.query][2], 'wb') as file:
                file.write(response.content)
        else:
            msg = (
                'Error while downloading the ASN DB '
                '(Status Code={}): {}'
            ).format(
                response.status_code,
                response.text,
            )
            logger.error(msg)
            raise Exception(msg)
        self.unpack()

    def unpack(self):
        """
        Extract MaxMind DB
        """
        if os.path.exists(self.helpers[self.query][2]):
            subprocess.Popen(['tar', '-xzf', self.helpers[self.query][2]], cwd=maxmind_directory)
            time.sleep(2)
        else:
            msg = 'Error extract DB on get_db '
            logger.error(msg)
            raise Exception(msg)

    def get_db_path(self):
        """
        Return the ASN Database path if exists

        """
        filtered_dir = [x for x in os.listdir(
            self.path_db) if x.startswith(self.helpers[self.query][0])]
        sorted_dir = sorted(filtered_dir, reverse=True)
        if sorted_dir:
            return str(Path(
                maxmind_directory,
                sorted_dir[0],
                self.helpers[self.query][1],
            ))
        else:
            return None

    def open_db(self):
        country_code_db_path = self.get_db_path()
        reader = maxminddb.open_database(country_code_db_path)
        return reader

    def get_data(self, ip_address):
        reader = self.open_db()
        return reader.get(ip_address)

    def get_age(self):
        reader = self.open_db()
        delta = datetime.now() - datetime.fromtimestamp(
            reader.metadata().build_epoch
        )
        return delta
