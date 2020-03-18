from bs4 import BeautifulSoup
import logging
import re
import requests

logger = logging.getLogger(__name__)

# RFC 6793 specifies 32 bit integer. The convention, of unknown origin,
# is to prefix "AS" to the decimal form integer. \d{1,10} is a rough
# approximation of 4,294,967,295
ASN_REGEX = re.compile('AS\\d{1,10}')


class URLVoid(object):

    def __init__(self, domain):
        self.domain = domain
        self.value = self.urlvoid_parser()

    def urlvoid_parser(self):
        """
        Parses URLVOID table with beatifulsoup
        :return: dictionary which contains urlvoid response
        """
        url = "https://www.urlvoid.com/scan/" + self.domain
        res = requests.get(url)
        text = res.text
        try:
            soup = BeautifulSoup(
                text, "lxml"
            ).find(
                "table",
                class_="table table-custom table-striped"
            )
            all_tr = soup.find_all("tr")
            value = {tr.find_all("td")[0].text:
                     tr.find_all("td")[1].text.replace("\xa0", "")
                     for tr in all_tr}
        except ModuleNotFoundError as me:
            logger.error("Opps ! Error : %s", me)
        return value

    def get_last_analysis_date(self):
        """

        :return: Last analysis time of given domain on URLVOID
        """
        try:
            result = self.value["Last Analysis"][:-9]
        except KeyError as ke:
            logger.error('Error while retrieving value', ke)
        return result

    def domain_registration_date(self):
        """

        :return: Registration time of domain
        """
        try:
            result = self.value["Domain Registration"]
        except KeyError as ke:
            logger.error(' DRD: Error while retrieving value; %s ', ke)
        return result

    def blacklist_status(self):
        """

        :return: Blacklist status among 36 services or more which are enable
        in URLVOID itself.
        """
        try:
            result = self.value["Blacklist Status"]
        except KeyError as ke:
            logger.error(
                ' Blacklist status: Error while retrieving value; %s ', ke)
        return result

    def get_asn(self):
        """

        :return: ASN Number
        """
        try:
            result = self.value["ASN"]
        except KeyError as ke:
            logger.error('ASN: Error while retrieving value; %s ', ke)
        m = ASN_REGEX.search(result)
        if m is None:
            logger.error(
                "Failed to parse ASN for {} from \"{}\"".format(
                    self.domain,
                    result,
                )
            )
            return None
        else:
            return m.group()

    def get_server_location(self):
        """

        :return: Server location of domain which exists on URLVOID
        """
        try:
            result = self.value["Server Location"]
        except KeyError as ke:
            logger.error(
                ' Server Location : Error while retrieving value; %s ', ke)
        return result

    def get_ip_address(self):
        """

        :return: IP address of given domain via URLVOID service
        """
        try:
            result = self.value["IP Address"]
        except KeyError as ke:
            logger.error(' IP Address: Error while retrieving value; %s ', ke)
        return result

    def get_detection_rate(self):
        """

        :return: Returns detection rate in percentage.
        """
        try:
            parts = self.blacklist_status().split("/")
            result = int(parts[0]) / int(parts[1]) * 100
        except IndexError as ie:
            logger.error(
                'Detection rate : Error while retrieving value; %s ', ie)
        return result
