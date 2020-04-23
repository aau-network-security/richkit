from dns import resolver
from dns import reversename
import logging

logger = logging.getLogger(__name__)


def get_a_record(domain):
    """
    Return the A record list of a given domain
    :param domain: domain (string)
    :return: IP Addresses (list)
    """
    try:
        a_record = []
        result = resolver.query(domain, 'A')
        for ip in result:
            a_record.append(ip.to_text())
        return a_record
    except Exception as ex:
        logger.error(ex)
        return None


def get_ptr_record(ip_address):
    """
    Return the PTR record of a given IP Address
    :param ip_address: IP Address (string)
    :return: domains list
    """
    try:
        ptr_record = []
        addr = reversename.from_address(ip_address)
        result = resolver.query(addr, 'PTR')
        for ip in result:
            ptr_record.append(ip.to_text())
        return ptr_record
    except Exception as ex:
        logger.error(ex)
        return None
