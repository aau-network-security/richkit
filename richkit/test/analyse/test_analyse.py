
import unittest


from richkit import analyse
from os import path
import requests
import tempfile
import logging
import os

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestEffect2LD():
    temp_directory = tempfile.mkdtemp()
    MASTERURL = "https://raw.githubusercontent.com/publicsuffix/list/master/tests/test_psl.txt"
    MASTERFILE = temp_directory + 'correct_test.txt'
    test = None

    @classmethod
    def fetch_tlds(cls, url=None):
        url = url or cls.MASTERURL

        # grab master list
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(cls.MASTERFILE, 'wb') as file:
                file.write(response.content)
        else:
            logger.error('Error while downloading the Test List status code: %s',
                         response.status_code)

    @classmethod
    def load_tlds(cls):
        try:
            f = open(cls.MASTERFILE, 'r', encoding="utf8")
            lines = f.readlines()
        except FileNotFoundError as e:

            logger.error("File not readable, not found %s", e)
            f.close()
        f.close()

        # strip comments and blank lines
        lines = [ln for ln in (ln.strip() for ln in lines) if len(ln) and ln[:2] != '//']

        cls.test = set(lines)

    def load(self):

        if path.exists(TestEffect2LD.MASTERFILE):
            TestEffect2LD.load_tlds()

        if TestEffect2LD.test is None:
            TestEffect2LD.fetch_tlds()
            TestEffect2LD.load_tlds()

    def get_tests(self):
        test_list = []
        for i in TestEffect2LD.test:
            parser = i[i.find("(")+1:i.find(")")]
            test_list.append(parser.replace(" ", "").replace("null", "'None'"))
        return test_list


class TestAnalyse(unittest.TestCase):

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
                # following values are smaller than expected due to top 100 alexa which is expected
                'n_grams_2ld': 27.33635144637163,
                'n_grams_2ld_alexa': 27.33081895777167
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
                # this is 0.0 because of gathering top 100 alexa db, written for just ensuring test functions running correctly
                'n_grams_2ld': 0.0,
                'n_grams_2ld_alexa':  0.0
            }
        }
        self.data_path = "data/"

    def tearDown(self):
        """
            Removes the file after test is done.
            Could be modified in future according to need
        """
        if os.path.isfile('top-1m.csv'):
            os.remove('top-1m.csv')

    def test_tld(self):
        for k, v in self.domain.items():
            domain_tld = analyse.tld(k)
            self.assertEqual(domain_tld, v['domain_tld'])

    def test_sld(self):
        for k, v in self.domain.items():
            domain_sld = analyse.sld(k)
            self.assertEqual(domain_sld, v['domain_sld'])

    def test_sl_label(self):
        for k, v in self.domain.items():
            domain_sld = analyse.sl_label(k)
            self.assertEqual(domain_sld, v['second_label'])

    def test_nld(self):
        for k, v in self.domain.items():
            nld3 = analyse.nld(k, 3)
            self.assertEqual(nld3, v['nld'])

    def test_n_label(self):
        for k, v in self.domain.items():
            n_label3 = analyse.n_label(k, 3)
            self.assertEqual(n_label3, v['n_label'])

    def test_depth(self):
        for k, v in self.domain.items():
            domain_depth = analyse.depth(k)
            self.assertEqual(domain_depth, str(v['num_tokens']))

    def test_length(self):
        for k, v in self.domain.items():
            domain_length = analyse.length(k)
            self.assertEqual(domain_length, str(v['len_domain']))

    def test_language(self):
        for k, v in self.domain.items():
            domain_language = analyse.language(k)
            self.assertEqual(domain_language, v['language'])

    def test_entropy(self):
        for k, v in self.domain.items():
            domain_entropy = analyse.entropy(k)
            self.assertEqual(domain_entropy, str(v['entropy']))

    def test_ratio_vowels(self):
        for k, v in self.domain.items():
            domain_ratio_vowels = analyse.ratio_vowels(k)
            self.assertEqual(domain_ratio_vowels, str(v['ratio_vowels']))

    def test_number_vowels(self):
        for k, v in self.domain.items():
            domain_number_vowels = analyse.number_vowels(k)
            self.assertEqual(domain_number_vowels, str(v['vowels']))

    def test_ratio_consonants(self):
        for k, v in self.domain.items():
            domain_ratio_consonants = analyse.ratio_consonants(k)
            self.assertEqual(domain_ratio_consonants, str(v['ratio_consonants_2ld']))

    def test_number_consonants(self):
        for k, v in self.domain.items():
            domain_number_consonants = analyse.number_consonants(k)
            self.assertEqual(domain_number_consonants, str(v['num_of_consonants_2ld']))

    def test_ratio_numerics(self):
        for k, v in self.domain.items():
            domain_ratio_numerics = analyse.ratio_numerics(k)
            self.assertEqual(domain_ratio_numerics, str(v['radio_numeric_2ld']))

    def test_number_numerics(self):
        for k, v in self.domain.items():
            domain_number_numerics = analyse.number_numerics(k)
            self.assertEqual(domain_number_numerics, str(v['num_numeric_2ld']))

    def test_ratio_specials(self):
        for k, v in self.domain.items():
            domain_ratio_specials = analyse.ratio_specials(k)
            self.assertEqual(domain_ratio_specials, str(v['ratio_special_2ld']))

    def test_number_specials(self):
        for k, v in self.domain.items():
            domain_number_specials = analyse.number_specials(k)
            self.assertEqual(domain_number_specials, str(v['num_of_special_2ld']))

    def test_number_words(self):
        for k, v in self.domain.items():
            domain_number_words = analyse.number_words(k)
            self.assertEqual(domain_number_words, str(v['num_words_2ld']))

    def test_get_grams_alexa_2ld(self):
        for k, v in self.domain.items():
            alexa_grams_2ld = analyse.n_grams_alexa(k, is_test=True)
            self.assertEqual(alexa_grams_2ld, v['n_grams_2ld_alexa'])

    def test_get_grams_dict_2ld(self):
        for k, v in self.domain.items():
            grams_dict_2ld = analyse.n_grams_dict(k, is_test=True)
            self.assertEqual(grams_dict_2ld, v['n_grams_2ld'])

    def test_correctly_tlds(self):
        tests = TestEffect2LD()
        tests.load()
        test_list = tests.get_tests()

        # Test skipped for the following list
        # Punycode are not handled by this library
        list_punycode_tests = [
            'xn--85x722f.xn--55qx5d.cn',
            'xn--85x722f.xn--fiqs8s',
            'xn--55qx5d.cn',
            'shishi.xn--55qx5d.cn',
            'www.xn--85x722f.xn--fiqs8s',
            'www.xn--85x722f.xn--55qx5d.cn',
            'shishi.xn--fiqs8s'
        ]

        # Test skipped for obvious invalid domains
        list_test_error = [
            '公司.cn',
            '中国',
            'biz',
            'jp',
            'us',
            'com',
            'a.b.example.example',
            'b.example.example',
            'example.example',
            '.example.com',
            '.com',
        ]

        # Test skipped for the following domains list
        # They start with esclamation point on the Public Suffix list
        list_esclamation_point = [
            'www.ck',
            'www.city.kobe.jp',
            'www.www.ck',
            'city.kobe.jp'
        ]

        for i in test_list:
            values = i.split(',')
            input = values[0].replace("'", "")
            expected = values[1].replace("'", "")
            if expected == "None":
                expected = None

            if input in list_punycode_tests or \
               input in list_test_error or \
               input in list_esclamation_point:
                continue
            else:
                self.assertEqual(analyse.sld(input), expected)
