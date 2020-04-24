import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import json
from urllib.parse import parse_qs
import socket
import threading
import requests
import os
import richkit.retrieve.ctlogs as ct
from richkit.retrieve.cert_sh import DomainCertificates
from richkit.retrieve.x509 import X509


class MockServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if re.search("/api", self.path):
            arguments_url = self.path.split('?', 1)[1]
            arguments = parse_qs(arguments_url)
            key = arguments.get('q')[0]

            path = os.getcwd()
            with open(path+"/crtsh_response.txt", "r") as crt:
                crt_response = crt.read()
                crt_response = crt_response.replace("\n", "")

            crt_rr = crt_response.split("------------")
            response_content = "<BR><BR>Certificate not found </BODY>"
            if key == "example.com":
                response_content = crt_rr[0]
            if key == "987119772":
                response_content = crt_rr[1]
            if key == "984858191":
                response_content = crt_rr[2]
            if key == "24560621":
                response_content = crt_rr[3]

            self.send_response(requests.codes.ok)

            self.send_header('Content-Type', 'text/html; charset=UTF-8')
            self.end_headers()

            # Put the dummy VT response here (maybe change the header ro json) --> application/json; charset=utf-8
            self.wfile.write(response_content.encode('utf-8'))
            return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockServer)
    mock_server_thread = threading.Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()


class TestCTLogs(unittest.TestCase):

    def setUp(self):
        self.port = get_free_port()
        start_mock_server(self.port)
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

    def test_mock_server(self):
        r = requests.get("http://localhost:{}/api/?q={}".format(self.port, "test.com"))
        self.assertEqual(r.text, "<BR><BR>Certificate not found </BODY>")

    def test_init_domain(self):
        obj = DomainCertificates("example.com")
        self.assertIsNotNone(obj)

    def test_init_certificate(self):
        obj = X509("12345678")
        self.assertIsNotNone(obj)

    def test_certificate_error(self):
        X509.crtSH_url = "http://localhost:" + str(self.port) + "/api/?q={}"
        with self.assertRaises(Exception):
            X509("this_id_does_not_exist.com")

    def test_get_all_certificate(self):

        for k, v in self.domains.items():
            DomainCertificates.crtSH_url = "http://localhost:{}/api/?q={}".format(self.port, k)
            certs = ct.get_logs(k)
            if certs is None:
                self.skipTest("Server not available")

            for cert in certs:
                for vx in v["certs"]:
                    if str(cert["ID"]) == str(vx["ID"]):
                        assert cert["Algorithm"] == vx["Algorithm"]
                        assert cert["SANFeatures"]["DomainCount"] == vx["SANFeatures"]["DomainCount"]

    def test_get_certificate_features(self):

        for k, v in self.domains.items():
            for cert in v["certs"]:
                X509.crtSH_url = "http://localhost:{}/api/?q={}".format(self.port, cert["ID"])
                cert_features = ct.get_certificates_features(cert["ID"])
                if not cert_features:
                    continue
                assert cert_features.get('DomainCount') == cert["SANFeatures"]["DomainCount"]
