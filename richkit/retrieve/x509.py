from richkit.analyse import tld, sld, sl_label, depth, length
import statistics
import requests
import logging

logger = logging.getLogger(__name__)


class X509:

    crtSH_url = "https://crt.sh/{}"

    def __init__(self, cert_id):
        self.cert_id = cert_id
        self.algorithm = None
        self.policy_list = None
        self.certificates_features = None
        self.get_certificate_features()

    def get_certificate_info(self, cert_id):
        try:
            r = requests.get(self.crtSH_url.format("?id=" + cert_id))
            if "<BR><BR>Certificate not found </BODY>" in r.text:
                raise Exception("Certificate not found")
            if "<BR><BR>Invalid value:" in r.text:
                raise Exception("Certificate not found")
            return r.text
        except Exception as e:
            logger.error('Error while retrieving certificate %s: %s', cert_id, e)
            return None

    def get_certificate_features(self):
        text = self.get_certificate_info(str(self.cert_id))
        text_list = text.split('<BR>')

        SAN_list = []           # Used to store the  SANs
        policy_list = []        # Used to store the policies in order to get the Validation Level

        algo_index = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Signature&nbsp;Algorithm:'
        san_index = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DNS:'
        policy_index = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Policy:&nbsp;'
        for row in text_list:
            # Get Signature Algorithm
            if algo_index in row:
                self.algorithm = row[len(algo_index) + 6:]

            # Get SANs
            if san_index in row:
                SAN_list.append(row[len(san_index):])

            if policy_index in row:
                policy_list.append(row[len(policy_index):])

        # Calculating the LCS
        apex = [sld(san) for san in SAN_list]
        lcs_num = 0
        for i in apex:
            for j in apex:
                current_lcs = lcs(i, j)
                if current_lcs > lcs_num:
                    lcs_num = current_lcs

        self.policy_list = policy_list
        self.certificates_features = dict({
            'san_list': SAN_list,
            'DomainCount': len(SAN_list),
            'UniqueApexCount': unique_apex(SAN_list),
            'UniqueSLDCount': unique_sld(SAN_list),
            'ShortestSAN': int(min([length(row) for row in SAN_list])),
            'LongestSAN': int(max([length(row) for row in SAN_list])),
            'SANsMean': statistics.mean([len(row) for row in SAN_list]),
            'MinSublabels': min([int(depth(row)) - 2 for row in SAN_list]),
            'MaxSublabels': max([int(depth(row)) - 2 for row in SAN_list]),
            'MeanSublabels': statistics.mean([int(depth(row)) for row in SAN_list]),
            'UniqueTLDsCount': unique_tld(SAN_list),
            'UniqueTLDsDomainCount': unique_tld(SAN_list) / len(SAN_list),
            'ApexLCS': None,        # Don't need to implement
            'LenApexLCS': lcs_num,
            'LenApexLCSnorm': lcs_num / int(max([length(row) for row in SAN_list]))
        })


def unique_apex(sans):
    """
    Number of unique apex/root domains covered by the certificate
    :param sans: List of Subject Alternative Name
    """
    apex = [sld(san) for san in sans]
    return len(set(apex))


def unique_tld(sans):
    """
    Number of unique apex/root domains covered by the certificate
    :param sans: List of Subject Alternative Name
    """
    get_tlds = [tld(san) for san in sans]
    return len(set(get_tlds))


def unique_sld(sans):
    """
    Number of unique apex/root domains covered by the certificate
    :param sans: List of Subject Alternative Name
    """
    get_sld = [sl_label(san) for san in sans]
    return len(set(get_sld))


def lcs(x, y):
    """
    The longest common substring (LCS)
    :param x: First string
    :param y: Second string
    """
    # find the length of the strings
    m = len(x)
    n = len(y)

    L = [[None] * (n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif x[i - 1] == y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    return L[m][n]
