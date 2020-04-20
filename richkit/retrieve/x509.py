from richkit.analyse import tld, sld, sl_label, depth, length
import statistics
import requests
import logging

logger = logging.getLogger(__name__)


class X509:
    """
    This class provides functions to extract certificate features from crt.sh
    The only needed parameter is the crt.sh ID of the certificate, it's possible to
    get it just making a request on crt.sh by listing all the certificates for a specific domain
    """

    # Website used to retrieve the certificates belonging a domain
    crtSH_url = "https://crt.sh/{}"

    def __init__(self, cert_id):
        """
        Get the Subject Alternative Name features from the given certificate
        :param cert_id: unique ID given by crt.sh per certificate
        """
        self.cert_id = cert_id
        self.algorithm = None
        self.policy_list = None
        self.certificates_features = None
        self.get_certificate_features()

    def get_certificate_info(self, cert_id):
        """
        Make a request and get the response content of the given ID
        :param cert_id: crt.sh ID of the certificate
        :return: response as text
        """
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
        """
        Parse the response content to get the certificate features
        """
        text = self.get_certificate_info(str(self.cert_id))
        text_list = text.split('<BR>')

        sans = SANList()           # Used to store the  SANs
        policy_list = []        # Used to store the policies in order to get the Validation Level

        algo_index = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Signature&nbsp;Algorithm:'
        san_index = \
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DNS:'

        san_index_email = \
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;email:'

        policy_index = \
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' \
            '&nbsp;&nbsp;&nbsp;&nbsp;Policy:&nbsp;'
        for row in text_list:
            # Get Signature Algorithm
            if algo_index in row:
                self.algorithm = row[len(algo_index) + 6:]

            # Get SANs
            if san_index in row:
                sans.append(row[len(san_index):])
            if san_index_email in row:
                sans.append(row[len(san_index_email):])

            if policy_index in row:
                policy_list.append(row[len(policy_index):])

        # Calculating the LCS
        apex = [sld(san) for san in sans.get_sans()]
        lcs_num = get_lcs_apex(apex)

        self.policy_list = policy_list
        self.certificates_features = dict({
            'san_list': sans.get_sans(),
            'DomainCount': len(sans.get_sans()),
            'UniqueApexCount': unique_apex(sans.get_sans()),
            'UniqueSLDCount': unique_sld(sans.get_sans()),
            'ShortestSAN': sans.min(),
            'LongestSAN': sans.max(),
            'SANsMean': sans.mean(),
            'MinSubLabels': sans.min_labels(),
            'MaxSubLabels': sans.max_labels(),
            'MeanSubLabels': sans.mean_labels(),
            'UniqueTLDsCount': unique_tld(sans.get_sans()),
            'UniqueTLDsDomainCount': sans.uniqueTLDsDomainCount(),
            'ApexLCS': None,        # Don't need to implement
            'LenApexLCS': lcs_num,
            'LenApexLCSNorm': sans.lenApexLCSNorm(lcs_num),
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
    Number of unique TLDs covered by the certificate
    :param sans: List of Subject Alternative Name
    """
    get_tlds = [tld(san) for san in sans]
    return len(set(get_tlds))


def unique_sld(sans):
    """
    Number of unique effective 2-level label domains covered by the certificate
    :param sans: List of Subject Alternative Name
    """
    get_sld = [sl_label(san) for san in sans]
    return len(set(get_sld))


def get_lcs_apex(apex):
    """
    The longest common substring of an array
    :param apex: apex array
    :return: The longest common substring
    """
    lcs_num = 0
    for i in apex:
        current_sans_list = apex[:]
        current_sans_list.remove(i)
        for j in current_sans_list:
            current_lcs = lcs(i, j)
            if current_lcs > lcs_num:
                lcs_num = current_lcs
    return lcs_num


def lcs(x, y):
    """
    The longest common substring (LCS)
    :param x: First string
    :param y: Second string
    :return LCS
    """
    m = len(x)
    n = len(y)

    h = [[None] * (n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                h[i][j] = 0
            elif x[i - 1] == y[j - 1]:
                h[i][j] = h[i - 1][j - 1] + 1
            else:
                h[i][j] = max(h[i - 1][j], h[i][j - 1])
    return h[m][n]


class SANList:
    """
    This class provides tje functions to extract features from the SAN list
    """

    def __init__(self):
        self.sans = []

    def append(self, san):
        self.sans.append(san)

    def get_sans(self):
        return self.sans

    def min(self):
        if not self.sans:
            return 0
        return int(min([length(row) for row in self.sans]))

    def max(self):
        if not self.sans:
            return 0
        return int(max([length(row) for row in self.sans]))

    def mean(self):
        if not self.sans:
            return 0
        return statistics.mean([len(row) for row in self.sans])

    def min_labels(self):
        if not self.sans:
            return 0
        return min([int(depth(row)) - 2 for row in self.sans])

    def max_labels(self):
        if not self.sans:
            return 0
        return max([int(depth(row)) - 2 for row in self.sans])

    def mean_labels(self):
        if not self.sans:
            return 0
        return statistics.mean([int(depth(row)) for row in self.sans])

    def uniqueTLDsDomainCount(self):
        if not self.sans:
            return 0
        return unique_tld(self.sans) / len(self.sans)

    def lenApexLCSNorm(self, lcs):
        if not self.sans:
            return 0
        return lcs / len(self.sans)
