from richkit.retrieve import dns

import unittest


class DNSTestCase(unittest.TestCase):
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
