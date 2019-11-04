import math
from collections import Counter

import langid
import numpy as np
from dat.analyse.segment import segment
from sklearn.feature_extraction.text import CountVectorizer
from dat.analyse.util import WordMatcher
from dat.analyse.util import load_alexa
from dat.analyse.util import load_words
from dat.analyse.util import TldMatcher


def entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count/lns * math.log(count/lns, 2) for count in list(p.values()))

def get_tld(domain):
	"""
	:param domain:
	:return:
	"""
	tldmatch = TldMatcher()
	try:
		tld = tldmatch.gettld(domain)
	except:
		tld = domain.split(".")[-1]
	return tld

def get_sld(domain):
	tldmatch = TldMatcher()
	try:
		sld = tldmatch.get_2ld(domain)
	except:
		sld = domain.split(".")[-2]
	return sld

def get_domain_name_features(domain):
	"""
	Returns domain name features within dictionary
	includes num_tokens, len2ld, len_domain

	:param: domain
	:return: dict

	"""
	domain_array = domain.split('.')
	num_tokens = len(domain_array)
	len2ld  = len(get_sld(domain))
	len_domain = sum([len(el) for el in domain_array])
	domain_name_features = {
		"num_tokens": str(num_tokens),
		"len2ld"    : str(len2ld),
		"len_domain": str(len_domain)
	}
	return domain_name_features


def get_language(domain):
	"""
	:param: domain
	"""
	try:
		language = langid.classify(" ".join(segment(get_tld(domain))))[0]
	except IndexError:
		language = ""
	except ValueError:
		language = ""
	return str(language)



def get_entropy_2ld(domain):
	"""
	:param domain:
	:return: entropy of second level domain
	"""
	return str(entropy(get_sld(domain)))



def get_grams_alexa_2ld(domain, analyzer='char', ngram_range=(3, 5)):
	"""
	:param : domain, analyzer, ngram_range
	:return: grams of second level domain
	"""
	alexa_slds = load_alexa()
	alexa_vc = CountVectorizer(analyzer=analyzer,
							   ngram_range=ngram_range,
							   min_df=1e-4,
							   max_df=1.0)
	counts_matrix = alexa_vc.fit_transform(alexa_slds)
	alexa_counts = np.log10(counts_matrix.sum(axis=0).getA1())
	grams_alexa2ld = ngram_count(get_sld(domain), alexa_counts, alexa_vc)
	return str(grams_alexa2ld)


def get_grams_dict_2ld(domain):
	"""

	:param domain:
	:return: grams_dict_2ld as string
	"""
	words = load_words()
	dict_vc = CountVectorizer(analyzer='char',
							  ngram_range=(3, 5),
							  min_df=1e-5,
							  max_df=1.0)
	counts_matrix = dict_vc.fit_transform(words)
	dict_counts = np.log10(counts_matrix.sum(axis=0).getA1())
	grams_dict2ld = ngram_count(get_sld(domain), dict_counts, dict_vc)
	return str(grams_dict2ld)


def get_num_words_2ld(domain):
	"""

	:param domain:
	:return: num of words in 2ld from WordMatcher Object
	"""
	word_matcher = WordMatcher()
	return str(word_matcher.get_num_of_words(get_tld(domain)))


def get_num_of_vowels_2ld(domain):
	"""

	:param domain:
	:return: number of counts:  vowels in 2ld
	"""
	sld=get_sld(domain)
	vowels = list("aeiouy")
	return str(sum([sld.count(c) for c in vowels]))


def get_ratio_vowels_2ld(domain):
	"""

	:param domain:
	:return: ratio of vowels in scope of 2ld
	"""
	return str(float(get_num_of_vowels_2ld(domain)) / float(len(get_sld(domain))))


def get_num_of_consonants_2ld(domain):
	"""

	:param domain:
	:return: number of consonants in scope of 2ld
	"""
	consonants = list("bcdfghjklmnpqrstvwxz")

	return str(sum([get_sld(domain).count(c) for c in consonants]))


def get_ratio_consonants_2ld(domain):
	"""
	:param domain:
	:return:  ratio of consonants
	"""
	return str(float(get_num_of_consonants_2ld(domain)) / float(len(get_sld(domain))))


def get_num_of_special_2ld(domain, special=list("~`!@#$%^&*()_={}[]:>;',</?*-+")):
	"""

	:param domain:
	:param special: special character list, default is "~`!@#$%^&*()_={}[]:>;',</?*-+"
	:return: total special character in 2ld.
	"""
	return str(sum([get_sld(domain).count(c) for c in special]))


def get_ratio_special_2ld(domain):
	"""

	:param domain:
	:return: ratio of special characters in 2ld
	"""
	return str(float(get_num_of_special_2ld(domain)) / float(len(get_sld(domain))))


def ngram_count(domain, counts, counts_vc):
	"""
	:param domain:
	:param counts:
	:param counts_vc: count vectorizer from sklearn
	:return: calculates ngram_count from given count vectorizer and counts
	"""
	match = counts * counts_vc.transform([domain]).T
	return str(match[0])
