import maxminddb
from dat.lookup.geo.util import MaxMind_CC_DB
from dat.lookup.geo.util import MaxMind_ASN_DB

def get_country(ip_address):
    """
    Return the country code of a given IP address

    :param ip_address: IP Address (string)

    """
    try:
        country_code_db = MaxMind_CC_DB()
        country_code_db_path = country_code_db.get_db_path()
        reader = maxminddb.open_database(country_code_db_path)
        result =  reader.get(ip_address)
        country_code = str(result['country']['iso_code'])
    except:
        country_code = ""
    return country_code

def get_registered_country(ip_address):
    """
    Return the registered country code of a given IP address

    :param ip_address: IP Address (string)

    """
    try:
        country_code_db = MaxMind_CC_DB()
        country_code_db_path = country_code_db.get_db_path()
        reader = maxminddb.open_database(country_code_db_path)
        result =  reader.get(ip_address)
        country_code = str(result['registered_country']['iso_code'])
    except:
        country_code = ""
    return country_code

def get_asn(ip_address):
    """
    Return the ASN of a given IP address

    :param ip_address: IP Address (string)

    """
    try:
        asn_db = MaxMind_ASN_DB()
        asn_db_path = asn_db.get_db_path()
        reader = maxminddb.open_database(asn_db_path)
        result = reader.get(ip_address)
        asn = "AS" + str(result['autonomous_system_number'])
    except:
        asn = ""
    return asn