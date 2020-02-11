from richkit.retrieve.urlvoid import URLVoid

import unittest

class URLVoidTestCase(unittest.TestCase):
    test_urls = {
        "google.co.uk": {
            "domain_registration": "1999-02-14",
            "blacklist_status": "0/36",
            "ASN": "AS15169",
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
            "ASN": "AS32934",
            "server_location": " (US) United States",
            "detection_rate": 0,
            "ip_address": "157.240.21.35",
            "a_record": ['31.13.72.36'],
            "ptr_record": ['edge-star-mini-shv-01-arn2.facebook.com.']
        },
    }

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


if __name__ == '__main__':
    unittest.main()
    
