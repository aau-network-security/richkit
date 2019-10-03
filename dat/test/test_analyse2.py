import unittest
from dat import analyse

class TestAnalyse2(unittest.TestCase):
    def setUp(self):
        self.domain = 'www.intranet.es.aau.dk'

    def test_tld(self):
        domain_tld = analyse.tld(self.domain)
        assert domain_tld == 'dk'
    
    def test_sld(self):
        domain_sld = analyse.sld(self.domain)
        assert domain_sld == 'aau.dk'
    
    def test_sl_label(self):
        domain_sld = analyse.sl_label(self.domain)
        assert domain_sld == 'aau'

    def test_nld(self):
        nld4 = analyse.nld(self.domain, 4)
        assert nld4 == 'intranet.es.aau.dk'

    def n_label(self):
        n_label4 = analyse.n_label(self.domain, 4)
        assert n_label4 == 'intranet'

    def test_depth(self):
        domain_depth = analyse.depth(self.domain)
        assert domain_depth == '5'

    def test_length(self):
        domain_length = analyse.length(self.domain)
        assert domain_length == '18'
    
    def test_language(self):
        domain_language = analyse.language(self.domain)
        assert domain_language == 'en'

    def test_entropy(self):
        domain_entropy = analyse.entropy(self.domain)
        assert domain_entropy == '2.2516291673878226'

    def test_ratio_vowels(self):
        domain_ratio_vowels = analyse.ratio_vowels(self.domain)
        assert domain_ratio_vowels == '0.5'

    def test_number_vowels(self):
        domain_number_vowels = analyse.number_vowels(self.domain)
        assert domain_number_vowels == '3'

    def test_ratio_consonants(self):
        domain_ratio_consonants = analyse.ratio_consonants(self.domain)
        assert domain_ratio_consonants == '0.3333333333333333'

    def test_number_consonants(self):
        domain_number_consonants = analyse.number_consonants(self.domain)
        assert domain_number_consonants == '2'

    def test_ratio_numerics(self):
        domain_ratio_numerics = analyse.ratio_numerics(self.domain)
        assert domain_ratio_numerics == '0.0'

    def test_number_numerics(self):
        domain_number_numerics = analyse.number_numerics(self.domain)
        assert domain_number_numerics == '0'

    def test_ratio_specials(self):
        domain_ratio_specials = analyse.ratio_specials(self.domain)
        assert domain_ratio_specials == '0.0'

    def test_number_specials(self):
        domain_number_specials = analyse.number_specials(self.domain)
        assert domain_number_specials == '0'

    def test_number_words(self):
        domain_number_words = analyse.number_words(self.domain)
        assert domain_number_words == '0'

    @unittest.skip("Skipping alexa test, tested locally")
    def test_get_grams_alexa_2ld(self):
        alexa_grams = analyse.n_grams_alexa(self.domain)
        assert alexa_grams == ''

    @unittest.skip("Skipping dict test since no data folder")
    def test_get_grams_dict_2ld(self):
        grams_dict_2ld  = analyse.n_grams_dict(self.domain)
        assert grams_dict_2ld == '25.77346214958408'