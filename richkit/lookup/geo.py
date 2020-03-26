from richkit.lookup.util import MaxMindDB
import os


def get_country(ip_address):
    """
    Return the country code of a given IP address

    :param ip_address: IP Address (string)

    """
    try:
        country_code_db = MaxMindDB((
            "https://download.maxmind.com/app/geoip_download?"
            "edition_id=GeoLite2-Country&"
            "license_key={license_key}&"
            "suffix=tar.gz"
        ).format(
            license_key=os.environ['MAXMIND_LICENSE_KEY'],
        ), "cc"
        )
        result = country_code_db.get_data(ip_address)
        country_code = str(result['country']['iso_code'])
    except:
        country_code = None
    return country_code


def get_registered_country(ip_address):
    """
    Return the registered country code of a given IP address

    :param ip_address: IP Address (string)

    """
    try:
        country_code_db = MaxMindDB((
            "https://download.maxmind.com/app/geoip_download?"
            "edition_id=GeoLite2-Country&"
            "license_key={license_key}&"
            "suffix=tar.gz"
        ).format(
            license_key=os.environ['MAXMIND_LICENSE_KEY'],
        ), "cc"
        )
        result = country_code_db.get_data(ip_address)
        country_code = str(result['registered_country']['iso_code'])
    except:
        country_code = None
    return country_code


def get_asn(ip_address):
    """
    Return the ASN of a given IP address

    :param ip_address: IP Address (string)

    """
    try:
        country_code_db = MaxMindDB((
            "https://download.maxmind.com/app/geoip_download?"
            "edition_id=GeoLite2-ASN&"
            "license_key={license_key}&"
            "suffix=tar.gz"
        ).format(
            license_key=os.environ['MAXMIND_LICENSE_KEY'],
        ), "asn"
        )
        result = country_code_db.get_data(ip_address)
        asn = str('AS' + str(result['autonomous_system_number']))
    except:
        asn = None
    return asn
