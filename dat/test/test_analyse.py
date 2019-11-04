import unittest
from dat.analyse.analyse import get_domain_name_features
from dat.analyse.analyse import get_num_words_2ld
from dat.analyse.analyse import get_grams_alexa_2ld
from dat.analyse.analyse import get_grams_dict_2ld
from dat.analyse.analyse import get_language
from dat.analyse.analyse import get_tld
from dat.analyse.analyse import get_num_of_special_2ld
from dat.analyse.analyse import get_num_of_consonants_2ld
from dat.analyse.analyse import get_num_of_vowels_2ld
from dat.analyse.analyse import get_entropy_2ld
from dat.analyse.analyse import get_ratio_vowels_2ld
from dat.analyse.analyse import get_ratio_special_2ld
from dat.analyse.analyse import get_ratio_consonants_2ld

class TestAnalyse(unittest.TestCase):
	def setUp(self):
		self.domain='www.google.co.uk'

	def test_get_domain_name_features(self):
		domain_features  = get_domain_name_features(self.domain)
		if (domain_features['num_tokens'] == '4') and \
				(domain_features['len2ld']== '6') and \
				(domain_features['len_domain']=='13'):
			self.assertEqual(True,True)
		else:
			self.assertEqual(True,False)


	def test_get_tld(self):
		domain_tld = get_tld(self.domain)
		assert domain_tld == "uk"


	def test_get_language(self):
		language = get_language(self.domain)
		assert language == 'en'

	def test_get_entropy_2ld(self):
		entropy = get_entropy_2ld(self.domain)
		assert entropy == '1.9182958340544893'

	@unittest.skip("Skipping alexa test, tested locally")
	def test_get_grams_alexa_2ld(self):
		alexa_grams = get_grams_alexa_2ld(self.domain)
		assert alexa_grams == '25.685477827705515'

	@unittest.skip("Skipping dict test since no data folder  ")
	def test_get_grams_dict_2ld(self):
		grams_dict_2ld  = get_grams_dict_2ld(self.domain)
		assert grams_dict_2ld == '25.77346214958408'

	def test_get_num_words_2ld(self):
		num_words_2ld = get_num_words_2ld(self.domain)
		assert  num_words_2ld =='0'

	def test_get_num_of_vowels_2ld(self):
		vowels = get_num_of_vowels_2ld(self.domain)
		assert  vowels == '3'
	def test_get_ratio_vowels_2ld(self):
		ratio_vowels  = get_ratio_vowels_2ld(self.domain)
		assert ratio_vowels == '0.5'
	def test_get_num_of_consonants_2ld(self):
		assert get_num_of_consonants_2ld(self.domain) == '3'
	def test_get_ratio_consonants_2ld(self):
		assert get_ratio_consonants_2ld(self.domain) == '0.5'

	def test_get_num_of_special_2ld(self):
		assert get_num_of_special_2ld(self.domain) == '0'

	def test_get_ratio_special_2ld(self):
		assert get_ratio_special_2ld(self.domain) == '0.0'
