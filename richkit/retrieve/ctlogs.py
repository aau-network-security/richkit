from richkit.retrieve.cert_sh import DomainCertificates
from richkit.retrieve.x509 import X509


def get_logs(domain):
    """
    Get a list of certificates with all the features
    :param domain: Input domain
    """
    try:
        certs = DomainCertificates(domain)
        return certs.get_all()
    except Exception as e:
        print(e)


def get_certificates(domain):
    """
    Get just the list of certificates of the domain
    :param domain: Input domain
    """
    try:
        certs = DomainCertificates(domain)
        return certs.get_cert_features()
    except Exception as e:
        print(e)


def get_certificates_features(cert_id):
    """
    Get the certificate features by certificate ID
    :param cert_id: crt.sh certificate ID
    """
    try:
        cert = X509(cert_id)
        return cert.certificates_features
    except Exception as e:
        print(e)
