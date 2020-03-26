import unittest
import richkit.retrieve.ctlogs as ct
from richkit.retrieve.ctlogs_util import DomainCertificates, CertificateFeatures


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
        obj2 = CertificateFeatures("12345678")
        self.assertIsNotNone(obj2)

    def test_get_all_certificate(self):

        with self.assertRaises(Exception):
            DomainCertificates("this_domain_does_not_exist.com")

        for k, v in self.certificate_ids.items():
            certs = ct.get_ctlogs(k)
            for cert in certs:
                if cert["ID"] in v:
                    assert cert["Algorithm"] == v[str(cert["ID"])]["Algorithm"]
                    assert cert["SANFeatures"]["DomainCount"] == v[str(cert["ID"])]["SANFeatures"]["DomainCount"]

    def test_get_certificate_features(self):

        with self.assertRaises(Exception):
            CertificateFeatures("this_id_does_not_exist.com")

        for k, v in self.certificate_ids.items():
            for k2, v2 in v.items():
                cert_features = ct.get_certificates_features(k2)
                assert cert_features.get('DomainCount') == v2["SANFeatures"]["DomainCount"]