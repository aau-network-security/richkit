import os.path
import unittest
from richkit.retrieve.symantec import fetch_from_internet
from richkit.retrieve.symantec import fetch_categories
from richkit.retrieve.symantec import load_categories
from richkit.retrieve.symantec import categories_url
from richkit.retrieve.util import URLVoid
from richkit.retrieve import dns


class RetrieveTestCase(unittest.TestCase):
    test_urls = {
        "google.co.uk": {
            "domain_registration": "1999-02-14",
            "blacklist_status": "0/36",
            "ASN": "AS15169 Google LLC",
            "server_location": " (US) United States",
            "detection_rate": 0,
            "ip_address": "172.217.19.227",
            "a_record": ['172.217.19.195', '172.217.17.67'],
            "ptr_record": [
                'ams16s30-in-f67.1e100.net.',
                'ams16s31-in-f3.1e100.net.',
                'ams16s30-in-f3.1e100.net.'
            ]
        },
        "facebook.com": {
            "domain_registration": "1997-03-29",
            "blacklist_status": "0/36",
            "ASN": "AS32934 Facebook, Inc.",
            "server_location": " (US) United States",
            "detection_rate": 0,
            "ip_address": "157.240.21.35",
            "a_record": ['31.13.72.36'],
            "ptr_record": ['edge-star-mini-shv-01-arn2.facebook.com.']
        },
    }

    def test_fetch_categories(self, file_path='categories_list.txt'):
        # make sure that categories url is accessible and fetched correctly
        categories = fetch_categories(categories_url, file_path)
        assert categories != {}
        os.remove(file_path)

    def test_load_categories(self, categories_file_path='categories_list.txt'):
        if os.path.isfile(categories_file_path):
            assert load_categories(categories_file_path) != {}
        else:
            assert load_categories(categories_file_path) == {}
        if os.path.isfile(categories_file_path):
            os.remove(categories_file_path)

    def test_fetch_from_internet(
            self,
            categories_file_path='categories_list.txt',
            categorized_url_path='categorized_urls.txt'
    ):
        domain_categories = {
            "Search Engines/Portals": [
                "www.bing.com",
                "www.google.com",
                "www.yandex.com"
            ],
            "Social Networking": [
                "www.facebook.com",
                "www.twitter.com"
            ]
        }
        for category, url_list in domain_categories.items():
            for url in url_list:
                assert fetch_from_internet(url, categories_file_path, categorized_url_path) == category
        if os.path.isfile(categories_file_path):
            os.remove(categories_file_path)
        os.remove(categorized_url_path)

    def test_domain_registration_date(self):
        for k, v in self.test_urls.items():
            instance = URLVoid(k)
            assert instance.domain_registration_date()[:-15] == v["domain_registration"]

    def test_get_detection_rate(self):
        for k, v in self.test_urls.items():
            instance = URLVoid(k)
            assert instance.get_detection_rate() == v["detection_rate"]

    def test_get_server_location(self):
        for k, v in self.test_urls.items():
            instance = URLVoid(k)
            assert instance.get_server_location() == v["server_location"]

    def test_get_asn(self):
        for k, v in self.test_urls.items():
            instance = URLVoid(k)
            assert instance.get_asn() == v["ASN"]

    def test_blacklist_status(self):
        for k, v in self.test_urls.items():
            instance = URLVoid(k)
            assert instance.blacklist_status() == v["blacklist_status"]

    @unittest.skip("A Record change every time")
    def test_a_record(self):
        for k, v in self.test_urls.items():
            instance = dns.get_a_record(k)
            assert instance[0] in v["a_record"]

    @unittest.skip("PTR Record change every time")
    def test_ptr_record(self):
        for k, v in self.test_urls.items():
            instance = dns.get_ptr_record(v["a_record"][0])
            print(instance)
            assert instance[0] in v["ptr_record"]


if __name__ == '__main__':
    unittest.main()
