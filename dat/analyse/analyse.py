from tld import get_tld, get_fld
from collections import Counter
from util import load_alexa
from util import load_words
from util import WordMatcher
import sklearn
import numpy as np
import langid
import segment
import math


def get_tld(domain, fix_protocol=True):
    """
    Overwriting default get_tld function from tld library with parameter fix_protocol=True
    :param domain:
    :param fix_protocol:
    :return:
    """
    return get_tld(domain, fix_protocol)


def get_fld(domain, fix_protocol=True):
    """
    Overwriting default get_fld function from tld library with parameter fix_protocol=True
    :param domain:
    :param fix_protocol:
    :return:
    """
    return get_fld(domain, fix_protocol)


## domain name related features

def get_domain_name_features(domain):
    """
    Returns domain name features within dictionary
    includes num_tokens, len2ld, len_domain

    :param: domain
    :return: dict

    """
    domain_array = domain.split('.')
    num_tokens = len(domain_array)
    len2ld, len_domain = len(get_fld(domain)), sum[[len(el) for el in domain_array]]
    domain_name_features = {
        "num_tokens": str(num_tokens),
        "len2ld": str(len2ld),
        "len_domain": str(len_domain)
    }
    return domain_name_features


def get_language(domain):
    """


    :param: domain
    """
    try:
        language = langid.classify(" ".join(segment.segment(get_fld(domain))))[0]
    except IndexError:
        language = ""
    except ValueError:
        language = ""
    return str(language)


def get_entropy_2ld(domain):

    s = get_fld(domain)

    def entropy(s):
        p, lns = Counter(s), float(len(s))
        return -sum(count / lns * math.log(count / lns, 2) for count in p.values())

    return str(entropy(s))


def get_grams_alexa_2ld(domain, analyzer='char', ngram_range=(3, 5)):
    alexa_slds = load_alexa()
    alexa_vc = sklearn.feature_extraction.text.CountVectorizer(analyzer=analyzer,
                                                               ngram_range=ngram_range,
                                                               min_df=1e-4,
                                                               max_df=1.0)
    counts_matrix = alexa_vc.fit_transform(alexa_slds)
    alexa_counts = np.log10(counts_matrix.sum(axis=0).getA1())
    grams_alexa2ld = ngram_count(get_fld(domain), alexa_counts, alexa_vc)
    return str(grams_alexa2ld)


def get_grams_dict_2ld(domain):
    words = load_words()
    dict_vc = sklearn.feature_extraction.text.CountVectorizer(analyzer='char',
                                                              ngram_range=(3, 5),
                                                              min_df=1e-5,
                                                              max_df=1.0)
    counts_matrix = dict_vc.fit_transform(words)
    dict_counts = np.log10(counts_matrix.sum(axis=0).getA1())
    grams_dict2ld = ngram_count(get_fld(domain), dict_counts, dict_vc)
    return str(grams_dict2ld)


def get_num_words_2ld(domain):
    word_matcher = WordMatcher()
    return str(word_matcher.get_num_of_words(get_fld(domain)))


def get_num_of_vowels_2ld(domain):
    vowels = list("aeiouy")
    return sum([get_fld(domain).count(c) for c in vowels])


def get_ratio_vowels_2ld(domain):
    return float(get_num_of_vowels_2ld(domain)) / float(len(get_fld(domain)))


def get_num_of_consonants_2ld(domain):
    consonants = list("bcdfghjklmnpqrstvwxz")
    return sum([get_fld(domain).count(c) for c in consonants])


def get_ratio_consonants_2ld(domain):
    return float(get_num_of_consonants_2ld(domain)) / float(len(get_fld(domain)))


def get_num_of_special_2ld(domain, special=list("~`!@#$%^&*()_={}[]:>;',</?*-+")):
    return sum([get_fld(domain).count(c) for c in special])


def get_ratio_special_2ld(domain):
    return float(get_num_of_special_2ld(domain)) / float(len(get_fld(domain)))


def ngram_count(domain, counts, counts_vc):
    match = counts * counts_vc.transform([domain]).T
    return match[0]
