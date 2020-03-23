from richkit.retrieve.util import DomainCertificates


def ctlogs():

    try:
        test = DomainCertificates("example.com")
        test.get_cert_features()
        test.get_san_features()
    except Exception as e:
        print(e)


ctlogs()
