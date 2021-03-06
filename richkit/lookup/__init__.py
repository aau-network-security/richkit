"""Confidentiality-aware look-ups for data on domain names.

This modules provides the ability to look up domain names in local
resources, i.e. the domain name cannot be sent of to third
parties. The module might fetch resources, such as lists or
databasese, but this must be done in a way that keeps the domain name
confidential. Contrast this with `richkit.retrieve`."""

from richkit.lookup import geo


def country(ip_address):
    """
    Return the country code of a given IP Address

    :param ip_address: IP Address (string)
    """
    return geo.get_country(ip_address)


def asn(ip_address):
    """
    Return the Autonomous System Number of a given IP Address

    :param ip_address: IP Address (string)
    """
    return geo.get_asn(ip_address)


def registered_country(ip_address):
    """
    Return the registered country code of a given IP Address

    :param ip_address: IP Address (string)
    """
    return geo.get_registered_country(ip_address)


def maxmindb_licence_key(license_key):
    """
    Return license key for MaxMind DB
    Retrieve license key for usage of MaxMindDb

    If it is not present print warning
    """

    return geo.get_license_key(license_key)
