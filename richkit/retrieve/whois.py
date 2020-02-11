import whois
import logging

logger = logging.getLogger(__name__)


def get_whois_info(domain):
    """

    :return: returns whois information of given domain name.
    """
    d = whois.query(domain)
    result = {
            "d_name": d.name,
            "d_expiration_date": d.expiration_date,
            "d_last_updated": d.last_updated,
            "d_registrar": d.registrar
    }
    return result
