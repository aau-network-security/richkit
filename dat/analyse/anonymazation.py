from ipaddress import ip_address
import hashlib

def anon_ip(ip, key):
    """
    Function that anonymazes the private IP Address, both IPv4 and IPv6

    :param ip: IP Address
    :param key: Encryption Key
    :return: Either the IP Address or the Hashed IP Address with the Key
    """
    if ip_address(ip).is_private:
        hash = hashlib.sha256()
        hash.update(key.encode())
        hash.update(ip.encode())
        return "sha256:" + hash.hexdigest()
    else:
        return ip
