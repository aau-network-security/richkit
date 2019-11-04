import pydig

def get_a_record(domain):
    """
    Return the A record list of a given domain

    :param domain: domain (string)
    :return: IP Addresses (list)
    """
    return pydig.query(domain, 'A')