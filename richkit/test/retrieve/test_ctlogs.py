import unittest
import richkit.retrieve.ctlogs as ct
from richkit.retrieve.util import DomainCertificates


class TestCTlogs(unittest.TestCase):

    def setUp(self):
        self.certificate_ids = {
            'example.com': {
                '987119772': {
                    "Algorithm": "sha256WithRSAEncryption",
                    "SANFeatures": {
                        "DomainCount": 8,
                    }
                }
            }
        }

    def test_init(self):
        obj = DomainCertificates("example.com")
        self.assertIsNotNone(obj)

    def test_get_certificate(self):

        with self.assertRaises(Exception):
            DomainCertificates("this_domain_does_not_exist.com")

        for k, v in self.certificate_ids.items():
            certs = ct.ctlogs(k)
            for cert in certs:
                print(cert["ID"])
                if cert["ID"] in v:
                    assert cert["Algorithm"] == v[str(cert["ID"])]["Algorithm"]
                    assert cert["SANFeatures"]["DomainCount"] == v[str(cert["ID"])]["SANFeatures"]["DomainCount"]
