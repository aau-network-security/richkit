import requests
import os, subprocess
import time, calendar, shutil
import tempfile
import logging

logger = logging.getLogger(__name__)
temp_directory = tempfile.mkdtemp()

class MaxMind_CC_DB(object):

    """
    This class provides functions to download, extract and get the path of the
    Country database provided by MaxMind

    """
    MASTERURL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"
    MASTERFILE = temp_directory + "/country.tar.gz"




    @classmethod
    def get_db(cls):
        """
        Download the Country database in zip format from the MaxMind website, then extract it

        """
        logger.info("Downloading MaxMind_CC_DB... ")
        response = requests.get(cls.MASTERURL, stream=True)
        if response.status_code == 200:
            with open(cls.MASTERFILE, 'wb') as file:
                file.write(response.content)
        else:
            logger.error('Error while downloading the Country DB ...')

        if os.path.exists(cls.MASTERFILE):
            subprocess.Popen(['tar', '-xzf', cls.MASTERFILE], cwd=temp_directory)
            time.sleep(2)
        else:
            logger.error('Error exctract DB.')


    def __init__(self):

        self.path_db = temp_directory
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
            return temp_directory + "/" + sorted_dir[0] + "/GeoLite2-Country.mmdb"
        else:
            return None


class MaxMind_ASN_DB():
    """
    This class provides functions to download, extract and get the path of the
    Autonomous System Number database provided by MaxMind

    """

    MASTERURL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz"
    MASTERFILE = temp_directory + "/asn.tar.gz"

    @classmethod
    def get_db(cls):
        """
        Download the Country database in zip format from the MaxMind website, then extract it

        """
        logger.info('Downloading the ASN DB ... ')
        response = requests.get(cls.MASTERURL, stream=True)
        if response.status_code == 200:
            with open(cls.MASTERFILE, 'wb') as file:
                file.write(response.content)
        else:
            logger.error('Error while downloading the ASN DB ....')

        if os.path.exists(cls.MASTERFILE):
            subprocess.Popen(['tar', '-xzf', cls.MASTERFILE], cwd=temp_directory)
            time.sleep(2)
        else:
            logger.error('Error extract DB on get_db ')


    def __init__(self):


        self.path_db = temp_directory
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
            return temp_directory + "/" + sorted_dir[0] + "/GeoLite2-ASN.mmdb"
        else:
            return None
