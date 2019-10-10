import requests
from bs4 import BeautifulSoup,NavigableString
import lxml

class URLVoid(object):

	def __init__(self,domain):
		self.domain = domain
		self.value = self.urlvoid_parser()

	def urlvoid_parser(self):
		url = "https://www.urlvoid.com/scan/" + self.domain
		res = requests.get(url)
		text = res.text
		soup = BeautifulSoup(text, "lxml").find("table", class_="table table-custom table-striped")
		all_tr = soup.find_all("tr")
		value = {tr.find_all("td")[0].text:
					 tr.find_all("td")[1].text.replace("\xa0", "")
				 for tr in all_tr}

		return value

	def get_last_analysis_date(self):
		return self.urlvoid_parser()["Last Analysis"][:-9]

	def domain_registration_date(self):
		return self.value["Domain Registration"]

	def blacklist_status (self):
		return self.value["Blacklist Status"]

	def get_asn(self):
		return self.value["ASN"]

	def get_server_location(self):
		return self.value["Server Location"]

	def get_detection_rate(self):
		parts= self.blacklist_status().split("/")
		return int(parts[0])/int(parts[1])*100

