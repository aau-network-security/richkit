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
		try:
			soup = BeautifulSoup(text, "lxml").find("table", class_="table table-custom table-striped")
			all_tr = soup.find_all("tr")
			value = {tr.find_all("td")[0].text:
						 tr.find_all("td")[1].text.replace("\xa0", "")
					 for tr in all_tr}
		except ModuleNotFoundError as me:
			print("Opps ! Error : %s",me)
		return value

	def get_last_analysis_date(self):
		try:
			result = self.value["Last Analysis"][:-9]
		except KeyError as ke:
			print(f'Error while retrieving value; {ke} ')
		return result

	def domain_registration_date(self):
		try:
			result = self.value["Domain Registration"]
		except KeyError as ke:
			print(f' DRD: Error while retrieving value; {ke} ')
		return result

	def blacklist_status (self):
		try:
			result = self.value["Blacklist Status"]
		except KeyError as ke:
			print(f' Blacklist status: Error while retrieving value; {ke} ')
		return result


	def get_asn(self):
		try:
			result = self.value["ASN"]
		except KeyError as ke:
			print(f' ASN: Error while retrieving value; {ke} ')
		return result


	def get_server_location(self):
		try:
			result = self.value["Server Location"]
		except KeyError as ke:
			print(f' Server Location : Error while retrieving value; {ke} ')
		return result

	def get_ip_address(self):
		try:
			result = self.value["IP Address"]
		except KeyError as ke:
			print(f' IP Address: Error while retrieving value; {ke} ')
		return result

	def get_detection_rate(self):
		try:
			parts = self.blacklist_status().split("/")
			result = int(parts[0]) / int(parts[1]) * 100
		except IndexError as ie:
			print(f'Detection rate : Error while retrieving value; {ie} ')
		return result
