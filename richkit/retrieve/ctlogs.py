from richkit.retrieve.ctlogs_util import DomainCertificates, CertificateFeatures


def get_ctlogs(domain):
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
        cert = CertificateFeatures(cert_id)
        return cert.certificates_features
    except Exception as e:
        print(e)
