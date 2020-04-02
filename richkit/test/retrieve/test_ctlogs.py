import unittest
import richkit.retrieve.ctlogs as ct
from richkit.retrieve.cert_sh import DomainCertificates
from richkit.retrieve.x509 import X509


class TestCTLogs(unittest.TestCase):

    def setUp(self):
        self.domains = {
            'example.com': {
                'certs': [
                    {
                        "ID": "987119772",
                        "Algorithm": "sha256WithRSAEncryption",
                        "SANFeatures": {
                            "DomainCount": 8,
                        }
                    },
                    {
                        "ID": "984858191",
                        "Algorithm": "sha256WithRSAEncryption",
                        "SANFeatures": {
                            "DomainCount": 8,
                        }
                    },
                    {
                        "ID": "24560621",
                        "Algorithm": "sha256WithRSAEncryption",
                        "SANFeatures": {
                            "DomainCount": 4,
                        }
                    },
                ]
            }
        }

    def test_init(self):
        obj = DomainCertificates("example.com")
        self.assertIsNotNone(obj)
        obj2 = X509("12345678")
        self.assertIsNotNone(obj2)

    def test_get_all_certificate(self):

        with self.assertRaises(Exception):
            DomainCertificates("this_domain_does_not_exist.com")

        for k, v in self.domains.items():
            certs = ct.get_logs(k)
            for cert in certs:
                for vx in v["certs"]:
                    if str(cert["ID"]) == str(vx["ID"]):
                        assert cert["Algorithm"] == vx["Algorithm"]
                        assert cert["SANFeatures"]["DomainCount"] == vx["SANFeatures"]["DomainCount"]

    def test_get_certificate_features(self):

        with self.assertRaises(Exception):
            X509("this_id_does_not_exist.com")

        for k, v in self.domains.items():
            for cert in v["certs"]:
                cert_features = ct.get_certificates_features(cert["ID"])
                assert cert_features.get('DomainCount') == cert["SANFeatures"]["DomainCount"]
