import pydig

def get_a_record(domain):
    """
    Return the A record list of a given domain

    :param domain: domain (string)
    :return: IP Addresses (list)
    """
    return pydig.query(domain, 'A')

def get_ptr_record(ip_adress):
    """
    Return the PTR record of a given IP Address

    :param ip_adress: IP Address (string)
    :return: domains (list)
    """

    helper_list = ip_adress.split('.')
    reversed_list = reverse(helper_list)
    query_string = '.'.join(reversed_list) + '.in-addr.arpa.'
    return pydig.query(query_string, 'PTR')

# Reversing a list using reversed()
def reverse(lst):
    return [ele for ele in reversed(lst)]