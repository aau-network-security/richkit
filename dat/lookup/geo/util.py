import ssl
import urllib.error
import urllib.parse
import urllib.request
import os
import subprocess
import time


class MaxMind_CC_DB(object):

    MASTERURL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"
    MASTERFILE = os.getcwd()+"/dat/lookup/maxmind_db/country.tar.gz"
    MASTERDB = os.getcwd()+"/dat/lookup/maxmind_db"

    @classmethod
    def get_db(cls):

        print('Downloading the Country DB ...')
        result = urllib.request.urlretrieve(cls.MASTERURL, cls.MASTERFILE)
        if(os.path.exists(result[0])):
            subprocess.Popen(['tar', '-xzf', cls.MASTERFILE], cwd=cls.MASTERDB)
            time.sleep(2)
        else:
            print('Error exctract DB.')

    

    def __init__(self):

        if MaxMind_CC_DB.get_db_path(self) is None:
            MaxMind_CC_DB.get_db()

    def get_db_path(self, path_db = os.getcwd()+"/dat/lookup/maxmind_db"):

        filtered_dir = [ x for x in os.listdir(path_db) if x.startswith('GeoLite2-Country_')]
        sorted_dir = sorted(filtered_dir,reverse=True)
        print(sorted_dir)
        if sorted_dir:
            return os.getcwd()+"/dat/lookup/maxmind_db/"+sorted_dir[0]+"/GeoLite2-Country.mmdb"
        else: 
            return None

MaxMind_CC_DB = MaxMind_CC_DB()

class MaxMind_ASN_DB():

    MASTERURL = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz"
    MASTERFILE = "maxmind_db/asn.tar.gz"
    MASTERDB = os.getcwd()+"/dat/lookup/maxmind_db"

    @classmethod
    def get_db(cls):

        print('Downloading the ASN DB ...')
        result = urllib.request.urlretrieve(cls.MASTERURL, cls.MASTERFILE)
        if(os.path.exists(result[0])):
            subprocess.Popen(['tar', '-xzf', cls.MASTERFILE], cwd=cls.MASTERDB)
            time.sleep(2)
        else:
            print('Error exctract DB.')

    

    def __init__(self):

        MaxMind_CC_DB.get_db()

    def get_db_path(self, path_db = os.getcwd()+"/dat/lookup/maxmind_db"):

        filtered_dir = [ x for x in os.listdir(path_db) if x.startswith('GeoLite2-Country_')]
        sorted_dir = sorted(filtered_dir,reverse=True)
        return os.getcwd()+"/dat/lookup/maxmind_db/"+sorted_dir[0]+"/GeoLite2-Country.mmdb"


