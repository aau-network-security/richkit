"""Retrieval of data on domain names.

This module provides the ability to retrieve data on domain names of
any sort. It comes without the "confidentiality contract" of
`richkit.lookup`.

"""
from richkit.retrieve import symantec

def symantec_category(domain):
    """
    Returns the category from Symantec's BlueCoat service.
    :param domain:
    :return:
    """
    return symantec.fetch_from_internet(domain)
