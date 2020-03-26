"""Retrieval of data on domain names.

This module provides the ability to retrieve data on domain names of
any sort. It comes without the "confidentiality contract" of
`richkit.lookup`.

"""
from richkit.retrieve import symantec
from richkit.retrieve import dns

def symantec_category(domain):
    """
    Returns the category from Symantec's BlueCoat service.
    :param domain:
    :return:
    """
    return symantec.fetch_from_internet(domain)


def dns_a(domain):
    """
    Return the A Records of a given domain
    :param domain: domain (string)
    :return: IP Addresses (list)
    """
    return dns.get_a_record(domain)


def dns_ptr(ip_address):
    """
    Return the PTR record of a given IP address
    :param ip_address: IP Address (string)
    :return: domains (list)
    """
    return dns.get_ptr_record(ip_address)

