import whois
import logging

logger = logging.getLogger(__name__)


def get_whois_info(domain):
    """Retrive a WHOIS information for a domain name

    :param domain: Domain name
    :type domain: str
    :return: WHOIS information of given domain name
    :rtype: dict (Actually a subclass of whois.parser.WhoisEntry, which
    itself is a subclass of `dict`)

    """
    result = whois.whois(domain)

    return result
