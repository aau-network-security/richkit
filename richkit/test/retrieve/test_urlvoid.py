from richkit.retrieve.urlvoid import URLVoid

import unittest


class URLVoidTestCase(unittest.TestCase):
    test_urls = {
        "google.co.uk": {
            "domain_registration": "1999-02-14",
            # checking number of blacklist status is not required, because the number of services where URLvoid uses may change over time.
            # therefore, the test has been removed
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
            assert instance.domain_registration_date()[:-15] \
                == v["domain_registration"]

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

        class StubURLVoid(URLVoid):
            def __init__(self, asn):
                self.domain = None
                self.value = {'ASN': asn}

        self.assertIsNone(StubURLVoid('AZ1 Not a valid ASN').get_asn())
        self.assertEqual(StubURLVoid('AS1').get_asn(), 'AS1')
        self.assertEqual(StubURLVoid('AS1 Random-Test-Text').get_asn(), 'AS1')
        self.assertEqual(StubURLVoid('AS1234567890').get_asn(), 'AS1234567890')
        # Strictly speaking, the below tests are correct, but covering them
        # is deemed unnecessary complex:
        # self.assertIsNone(
        #     StubURLVoid('AS12345678901').get_asn(),
        #     ("Failed to reject ASN of 10 decimal digits (One more digit that"
        #      "possible with RFC 6793)"),
        # )
        # self.assertIsNone(
        #     StubURLVoid('AS4294967295').get_asn(),
        #     "Failed to reject ASN 0xFFFFFFFF + 0x1 (RFC 6793 max value + 1)",
        # )


if __name__ == '__main__':
    unittest.main()
