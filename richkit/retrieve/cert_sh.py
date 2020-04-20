import requests
import json
import logging
from richkit.retrieve.x509 import X509
from datetime import datetime

logger = logging.getLogger(__name__)


class DomainCertificates:
    """
    This class provides the functions to get certificates of a given domain.
    The website used to get them is crt.sh
    """

    # Website used to retrieve the certificates belonging a domain
    crtSH_url = "https://crt.sh/{}"

    def __init__(self, domain):
        """
        Get the certificate features from the given domain
        :param domain: domain to analyze
        """
        self.domain = domain
        self.certificates = None
        self.certificates_features = None
        self.get_certificates(self.domain)

    def get_certificates(self, domain):
        """
        Make a request and get the response content of the given domain
        :param domain: the choosen domain
        """
        try:
            r = requests.get(self.crtSH_url.format("?q=" + domain + "&output=json"))
            if r.status_code != 200:
                return
            content = r.content.decode('utf-8')
            if len(r.text) == 2:        # It's 2 when the domain is not found
                raise Exception("Domain not found")
            self.certificates = json.loads(content)
        except Exception as e:
            logger.error('Error while retrieving certificates: %s', e)
            raise e

    def get_all(self):
        """
        Get the list of certificates for the given domain and the certificate features for each of them
        """
        certs_features = []
        for cert in self.certificates:
            # filter out all the rows containing @ because they are email
            # example: https://crt.sh/?id=34083306
            cf = X509(cert.get('id'))
            not_before = cert.get('not_before')
            not_after = cert.get('not_after')
            not_before_obj = datetime.strptime(not_before, "%Y-%m-%dT%H:%M:%S")
            not_after_obj = datetime.strptime(not_after, "%Y-%m-%dT%H:%M:%S")
            validity = (not_after_obj.date() - not_before_obj.date()).days
            features = dict({
                'ID': cert.get('id'),
                'Issuer': cert.get('issuer_name'),
                'Algorithm': cf.algorithm,
                'ValidationL': cf.policy_list,
                'NotBefore': not_before,
                'NotAfter': not_after,
                'Validity': validity,       # days
                'SANFeatures': cf.certificates_features
            })
            certs_features.append(features)
        self.certificates_features = certs_features
        return certs_features

    def get_certificates_list(self):
        """
        Get the list of certificates for the given domain
        """
        certs_features = []
        for cert in self.certificates:
            # filter out all the rows containing @ because they are email
            # example: https://crt.sh/?id=34083306
            not_before = cert.get('not_before')
            not_after = cert.get('not_after')
            not_before_obj = datetime.strptime(not_before, "%Y-%m-%dT%H:%M:%S")
            not_after_obj = datetime.strptime(not_after, "%Y-%m-%dT%H:%M:%S")
            validity = (not_after_obj.date() - not_before_obj.date()).days
            features = dict({
                'ID': cert.get('id'),
                'Issuer': cert.get('issuer_name'),
                'NotBefore': not_before,
                'NotAfter': not_after,
                'Validity': validity,       # days
            })
            certs_features.append(features)
        self.certificates_features = certs_features
        return certs_features
