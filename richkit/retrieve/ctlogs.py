from richkit.retrieve.util import DomainCertificates


def ctlogs(domain):

    try:
        test = DomainCertificates(domain)
        test.get_cert_features()
        return test.get_san_features()
    except Exception as e:
        print(e)
