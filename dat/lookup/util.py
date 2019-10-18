import urllib.error, urllib.parse, urllib.request
import os, subprocess
import time, calendar, shutil
import tempfile

class TempFile:
    tempfile = tempfile.TemporaryDirectory()
    def __init__(self):
        self.tempfile=tempfile
    def get_temporary_folder(self):
        return self.tempfile.gettempdir()

temp_directory = TempFile.tempfile

class MaxMind_CC_DB(object):
    """
    This class provides functions to download, extract and get the path of the
    Country database provided by MaxMind

    """
    MASTERURL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"
    MASTERFILE = temp_directory.name + "country.tar.gz"

    @classmethod
    def get_db(cls):
        """
        Download the Country database in zip format from the MaxMind website, then extract it

        """
        print('Downloading the Country DB ...')
        result = urllib.request.urlretrieve(cls.MASTERURL, cls.MASTERFILE)
        if os.path.exists(result[0]):
            subprocess.Popen(['tar', '-xzf', cls.MASTERFILE], cwd=temp_directory.name)
            time.sleep(2)
        else:
            print('Error exctract DB.')

    def __init__(self):

        self.path_db = temp_directory.name
        self.three_weeks = 1814400  # seconds of 3 weeks  1814400

        # check if the database already exists
        if MaxMind_CC_DB.get_db_path(self) is None:
            MaxMind_CC_DB.get_db()

        # check if the database is updated
        if (int(calendar.timegm(time.gmtime())) - int(os.path.getctime(MaxMind_CC_DB.get_db_path(self)))) > self.three_weeks:
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
            return temp_directory.name + "/" + sorted_dir[0] + "/GeoLite2-Country.mmdb"
        else:
            return None

class MaxMind_ASN_DB():
    """
    This class provides functions to download, extract and get the path of the
    Autonomous System Number database provided by MaxMind

    """

    MASTERURL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz"
    MASTERFILE = temp_directory.name + "asn.tar.gz"

    @classmethod
    def get_db(cls):
        """
        Download the Country database in zip format from the MaxMind website, then extract it

        """
        print('Downloading the ASN DB ...')
        result = urllib.request.urlretrieve(cls.MASTERURL, cls.MASTERFILE)
        if os.path.exists(result[0]):
            subprocess.Popen(['tar', '-xzf', cls.MASTERFILE], cwd=temp_directory.name)
            time.sleep(2)
        else:
            print('Error exctract DB.')

    def __init__(self):

        self.path_db = temp_directory.name
        self.three_weeks = 1814400  # seconds of 3 weeks  1814400

        # check if the database already exists
        if MaxMind_ASN_DB.get_db_path(self) is None:
            MaxMind_ASN_DB.get_db()

        # check if the database is updated
        if (int(calendar.timegm(time.gmtime())) - int(os.path.getctime(MaxMind_ASN_DB.get_db_path(self)))) > self.three_weeks:
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
            return temp_directory.name + "/" + sorted_dir[0] + "/GeoLite2-ASN.mmdb"
        else:
            return None
