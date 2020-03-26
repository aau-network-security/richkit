from richkit.retrieve import dns

import unittest


class DNSTestCase(unittest.TestCase):
    # Since A record change every time, just checking whether we are retrieving a record or not
    def setUp(self):
        self.test_urls = ["www.google.co.uk", "www.cloudflare.com", "www.intranet.es.aau.dk"]
        self.test_ips = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]

    def test_a_record(self):
        for url in self.test_urls:
            instance = dns.get_a_record(url)
            assert instance[0] is not None

    # Since PTR record change every time, just checking whether we are retrieving a record or not
    def test_ptr_record(self):
        for url in self.test_ips:
            instance = dns.get_ptr_record(url)
            assert instance[0] is not None


if __name__ == '__main__':
    unittest.main()
