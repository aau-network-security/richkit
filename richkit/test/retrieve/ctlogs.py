import unittest
import richkit.retrieve.ctlogs as ct


class TestAnalyse(unittest.TestCase):

    def setUp(self):
        self.certificate_ids = {
            'example.com': {
                '987119772': {
                    "Issuer": "C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA",
                    "Algorithm": "sha256WithRSAEncryption",
                    "ValidationL": [
                        "2.16.840.1.114412.1.1",
                        "2.23.140.1.2.2"
                    ],
                    "NotBefore": "2018-11-28T00:00:00",
                    "NotAfter": "2020-12-02T12:00:00",
                    "Validity": 735,
                    "SANFeatures": {
                        "DomainCount": 8,
                        "UniqueApexCount": 4,
                        "UniqueSLDCount": 1,
                        "ShortestSAN": 10,
                        "LongestSAN": 13,
                        "SANsMean": 13,
                        "MinSublabels": 0,
                        "MaxSublabels": 1,
                        "MeanSublabels": 2.5,
                        "UniqueTLDsCount": 4,
                        "UniqueTLDsDomainCount": 0.5,
                        "ApexLCS": "None",
                        "LenApexLCS": "None",
                        "LenApexLCSnorm": "None"
                    }
                }
            }
        }

    def test_get_certificate(self):
        for k, v in self.certificate_ids.items():
            r = ct.ctlogs(k)
            assert r[0]["Algorithm"] == v["987119772"]["Algorithm"]
