import requests
import os, subprocess
import time, calendar, shutil
import logging
from pathlib import Path

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    level=logging.DEBUG)
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

class MaxMind_CC_DB(object):

    """
    This class provides functions to download, extract and get the path of the
    Country database provided by MaxMind

    """
    MASTERURL = ( # https://dev.maxmind.com/geoip/geoipupdate/#Direct_Downloads
        "https://download.maxmind.com/app/geoip_download?"
        "edition_id=GeoLite2-Country&"
        "license_key={license_key}&"
        "suffix=tar.gz"
    ).format(
        license_key=os.environ['MAXMIND_LICENSE_KEY'],
    )
    MASTERFILE = str(Path(maxmind_directory, "country.tar.gz"))

    @classmethod
    def get_db(cls):
        """
        Download the Country database in zip format from the MaxMind website, then extract it

        """
        logger.debug("Downloading MaxMind_CC_DB... ")
        try:
            response = requests.get(cls.MASTERURL, stream=True)
        except Exception as e:
            logger.error('Reraising Exception raised by requests.get ({})'.format(e))
            raise e

        if response.status_code == 200:
            with open(cls.MASTERFILE, 'wb') as file:
                file.write(response.content)
        else:
            msg = (
                'Error while downloading the Country DB '
                '(Status Code={}): {}'
            ).format(
                response.status_code,
                response.text,
            )
            logger.error(msg)
            raise Exception(msg)

        if os.path.exists(cls.MASTERFILE):
            subprocess.Popen(['tar', '-xzf', cls.MASTERFILE], cwd=maxmind_directory)
            time.sleep(2)
        else:
            logger.error('Error exctract DB.')


    def __init__(self):

        self.path_db = maxmind_directory
        self.three_weeks = 1814400  # seconds of 3 weeks  1814400

        # check if the database already exists
        if MaxMind_CC_DB.get_db_path(self) is None:
            MaxMind_CC_DB.get_db()

        # check if the database is updated
        if (int(calendar.timegm(time.gmtime())) - int(
                os.path.getctime(MaxMind_CC_DB.get_db_path(self)))) > self.three_weeks:
            shutil.rmtree(self.path_db)
            os.mkdir(self.path_db)
            MaxMind_CC_DB.get_db()

    def get_db_path(self):
        """
        Return the Country Database path if exists

        """
        filtered_dir = [x for x in os.listdir(self.path_db) if x.startswith('GeoLite2-Country_')]
        sorted_dir = sorted(filtered_dir, reverse=True)
        if sorted_dir:
            return str(Path(
                maxmind_directory,
                sorted_dir[0],
                "GeoLite2-Country.mmdb",
            ))
        else:
            return None


class MaxMind_ASN_DB():
    """
    This class provides functions to download, extract and get the path of the
    Autonomous System Number database provided by MaxMind

    """

    MASTERURL = ( # https://dev.maxmind.com/geoip/geoipupdate/#Direct_Downloads
        "https://download.maxmind.com/app/geoip_download?"
        "edition_id=GeoLite2-ASN&"
        "license_key={license_key}&"
        "suffix=tar.gz"
    ).format(
        license_key=os.environ['MAXMIND_LICENSE_KEY'],
    )
    MASTERFILE = str(Path(maxmind_directory, "asn.tar.gz"))

    @classmethod
    def get_db(cls):
        """
        Download the Country database in zip format from the MaxMind website, then extract it

        """
        logger.debug('Downloading the ASN DB ... ')
        try:
            response = requests.get(cls.MASTERURL, stream=True)
        except Exception as e:
            logger.error('Reraising Exception raised by requests.get ({})'.format(e))
            raise e

        if response.status_code == 200:
            with open(cls.MASTERFILE, 'wb') as file:
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

        if os.path.exists(cls.MASTERFILE):
            subprocess.Popen(['tar', '-xzf', cls.MASTERFILE], cwd=maxmind_directory)
            time.sleep(2)
        else:
            logger.error('Error extract DB on get_db ')


    def __init__(self):


        self.path_db = maxmind_directory
        self.three_weeks = 1814400  # seconds of 3 weeks  1814400
        # check if the database already exists
        if MaxMind_ASN_DB.get_db_path(self) is None:
            MaxMind_ASN_DB.get_db()

        # check if the database is updated
        if (int(calendar.timegm(time.gmtime())) - int(
                os.path.getctime(MaxMind_ASN_DB.get_db_path(self)))) > self.three_weeks:
            shutil.rmtree(self.path_db)
            os.mkdir(self.path_db)
            MaxMind_ASN_DB.get_db()

    def get_db_path(self):
        """
        Return the ASN Database path if exists

        """
        filtered_dir = [x for x in os.listdir(self.path_db) if x.startswith('GeoLite2-ASN_')]
        sorted_dir = sorted(filtered_dir, reverse=True)
        if sorted_dir:
            return str(Path(
                maxmind_directory,
                sorted_dir[0],
                "GeoLite2-ASN.mmdb",
            ))
        else:
            return None
