import unittest
from dat import analyse


class TestAnalyse2(unittest.TestCase):
    def setUp(self):
        self.domain = {
            'www.google.co.uk': {
                'num_tokens': 4,
                'len2ld': 12,
                'len_domain': 13,
                'domain_tld': "co.uk",
                'domain_sld': "google.co.uk",
                'second_label': "google",
                'language': "en",
                'nld': "www.google.co.uk",
                'n_label': "www",
                'entropy': 2.8553885422075336,
                'num_words_2ld': 0,
                'vowels': 5,
                'ratio_vowels': 0.4166666666666667,
                'num_of_consonants_2ld': 5,
                'ratio_consonants_2ld': 0.4166666666666667,
                'num_of_special_2ld': 0,
                'ratio_special_2ld': 0.0,
                'num_numeric_2ld': 0,
                'radio_numeric_2ld': 0.0,
            },
            'www.intranet.es.aau.dk': {
                'num_tokens': 5,
                'len2ld': 6,
                'len_domain': 18,
                'domain_tld': "dk",
                'domain_sld': 'aau.dk',
                'second_label': "aau",
                'language': "en",
                'nld': "es.aau.dk",
                'n_label': "es",
                'entropy': 2.2516291673878226,
                'num_words_2ld': 0,
                'vowels': 3,
                'ratio_vowels': 0.5,
                'num_of_consonants_2ld': 2,
                'ratio_consonants_2ld': 0.3333333333333333,
                'num_of_special_2ld': 0,
                'ratio_special_2ld': 0.0,
                'num_numeric_2ld': 0,
                'radio_numeric_2ld': 0.0,
            }
        }

    def test_tld(self):
        for k, v in self.domain.items():
            domain_tld = analyse.tld(k)
            assert domain_tld == v['domain_tld']

    def test_sld(self):
        for k, v in self.domain.items():
            domain_sld = analyse.sld(k)
            assert domain_sld == v['domain_sld']

    def test_sl_label(self):
        for k, v in self.domain.items():
            domain_sld = analyse.sl_label(k)
            assert domain_sld == v['second_label']

    def test_nld(self):
        for k, v in self.domain.items():
            nld3 = analyse.nld(k, 3)
            assert nld3 == v['nld']

    def test_n_label(self):
        for k, v in self.domain.items():
            n_label3 = analyse.n_label(k, 3)
            assert n_label3 == v['n_label']

    def test_depth(self):
        for k, v in self.domain.items():
            domain_depth = analyse.depth(k)
            assert domain_depth == str(v['num_tokens'])

    def test_length(self):
        for k, v in self.domain.items():
            domain_length = analyse.length(k)
            assert domain_length == str(v['len_domain'])

    def test_language(self):
        for k, v in self.domain.items():
            domain_language = analyse.language(k)
            assert domain_language == v['language']

    def test_entropy(self):
        for k, v in self.domain.items():
            domain_entropy = analyse.entropy(k)
            assert domain_entropy == str(v['entropy'])

    def test_ratio_vowels(self):
        for k, v in self.domain.items():
            domain_ratio_vowels = analyse.ratio_vowels(k)
            assert domain_ratio_vowels == str(v['ratio_vowels'])

    def test_number_vowels(self):
        for k, v in self.domain.items():
            domain_number_vowels = analyse.number_vowels(k)
            assert domain_number_vowels == str(v['vowels'])

    def test_ratio_consonants(self):
        for k, v in self.domain.items():
            domain_ratio_consonants = analyse.ratio_consonants(k)
            assert domain_ratio_consonants == str(v['ratio_consonants_2ld'])

    def test_number_consonants(self):
        for k, v in self.domain.items():
            domain_number_consonants = analyse.number_consonants(k)
            assert domain_number_consonants == str(v['num_of_consonants_2ld'])

    def test_ratio_numerics(self):
        for k, v in self.domain.items():
            domain_ratio_numerics = analyse.ratio_numerics(k)
            assert domain_ratio_numerics == str(v['radio_numeric_2ld'])

    def test_number_numerics(self):
        for k, v in self.domain.items():
            domain_number_numerics = analyse.number_numerics(k)
            assert domain_number_numerics == str(v['num_numeric_2ld'])

    def test_ratio_specials(self):
        for k, v in self.domain.items():
            domain_ratio_specials = analyse.ratio_specials(k)
            assert domain_ratio_specials == str(v['ratio_special_2ld'])

    def test_number_specials(self):
        for k, v in self.domain.items():
            domain_number_specials = analyse.number_specials(k)
            assert domain_number_specials == str(v['num_of_special_2ld'])

    def test_number_words(self):
        for k, v in self.domain.items():
            domain_number_words = analyse.number_words(k)
            assert domain_number_words == str(v['num_words_2ld'])

    @unittest.skip("Skipping alexa test, tested locally")
    def test_get_grams_alexa_2ld(self):
        alexa_grams = analyse.n_grams_alexa(self.domain)
        assert alexa_grams == ''

    @unittest.skip("Skipping dict test since no data folder")
    def test_get_grams_dict_2ld(self):
        grams_dict_2ld = analyse.n_grams_dict(self.domain)
        assert grams_dict_2ld == '25.77346214958408'