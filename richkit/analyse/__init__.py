"""Analysis and computations on domain names.

This module provides functions that can be applied to a domain
name. Similarly to `richkit.lookup`, and in contrast to `richkit.retrieve`,
this is done without disclosing the domain name to third parties and
breaching confidentiality.

.. note:: For this entire module, we adopt the notion of effective
Top-Level Domains (eTLD), effective Second-Level Domain (e2LD), etc.
"Effective" refers to the practice where the public sufffic is
considered the effective TLD, and counted as one label. The `list of
public suffixes <https://publicsuffix.org/list/>`_, maintained by
Mozilla, is used as the definitive truth on what public suffixes
exists.

"""

from richkit.analyse import analyse

# aka tld
def tld(domain):
    """
    Returns the Effective Top-Level Domain (eTLD) (aka Public Suffix).

    The eTLD is extracted from the domain,

    :param domain: Domain (string)

    """
    return analyse.get_tld(domain)


def sld(domain):
    """
    Returns the Effective Second-Level Domain (2LD) (aka Apex Domain).

    The 2LD, aka the Apex Domain, is extracted from the domain, using
    the `list of public suffixes <https://publicsuffix.org/list/>`_
    maintained by Mozilla

    :param domain: Domain (string)

    """
    return analyse.get_sld(domain)


def sl_label(domain):
    """
    Returns the Effective 2-level label.

    :param domain: Domain (string)

    """
    return analyse.get_2l_label(domain)


def nld(domain, n):
    """
    Returns the Effective N'th-Level Domain (eNLD).

    :param domain: Domain (string)
    :param n: N'th-Level (int)

    """
    return analyse.get_nld(domain, n)


def n_label(domain, n):
    """
    Returns the Effective N'th-level label.

    :param domain: Domain (string)
    :param n: N'th-Level (int)

    """
    return analyse.get_n_label(domain, n)


def depth(domain):
    """
    Returns the effective depth of the domain,

    The depth is the number of labels in the domain.

    .. example:: `google.co.uk` is "effectively a 2LD. `google` is one
    label. The public suffix of `co.uk` is considered one label
    effectively. With effectively two labels, the effective depth is
    two.

    :param domain: Domain (string)

    """
    domain_name_features = analyse.get_domain_name_features(domain)
    return domain_name_features.get("num_tokens", "")


def length(domain):
    """
    Returns the sum of count of characters for all labels.

    :param domain: Domain (string)

    """
    domain_name_features = analyse.get_domain_name_features(domain)
    return domain_name_features.get("len_domain", "")


def language(domain):
    """
    Returns the best gues for the language of the domain.

    :param domain: Domain (string)

    """
    return analyse.get_language(domain)


def entropy(s):
    """
    Returns the entropy of characters in s.

    :param s: Domain (string)

    """
    return analyse.get_entropy_2ld(s)


def ratio_vowels(s):
    """
    Returns the ratio vowels to all characters in s.

    :param s: Domain (string)

    """
    return analyse.get_ratio_vowels_2ld(s)


def number_vowels(s):
    """
    Returns the number vowels to all characters in s.

    :param s: Domain (string)

    """
    return analyse.get_num_of_vowels_2ld(s)


def ratio_consonants(s):
    """
    Returns the ratio consonants to all characters in s.

    :param s: Domain (string)

    """
    return analyse.get_ratio_consonants_2ld(s)


def number_consonants(s):
    """
    Returns the number consonants to all characters in s.

    :param s: Domain (string)

    """
    return analyse.get_num_of_consonants_2ld(s)


def ratio_numerics(s):
    """
    Returns the ratio numeric characters to all characters in s.

    :param s: Domain (string)

    """
    return analyse.get_radio_numeric_2ld(s)


def number_numerics(s):
    """
    Returns the number numeric characters to all characters in s.

    :param s: Domain (string)

    """
    return analyse.get_num_numeric_2ld(s)


def ratio_specials(s):
    """
    Returns the ratio special characters to all characters in s.
    The default special character list is "~`!@#$%^&*()_={}[]:>;',</?*-+"

    :param s: Domain (string)

    """
    return analyse.get_ratio_special_2ld(s)


def number_specials(s):
    """
    Returns the number special characters to all characters in s.
    The default special character list is "~`!@#$%^&*()_={}[]:>;',</?*-+".

    :param s: Domain (string)

    """
    return analyse.get_num_of_special_2ld(s)


def number_words(s):
    """
    Returns the number of English word found in s.

    :param s: Domain (string)

    """
    return analyse.get_num_words_2ld(s)


def n_grams_alexa(domain):
    """
    Returns similarity to distribution of N-grams in Alexa Top 1M.

    :param domain: Domain (string)

    """
    return analyse.get_grams_alexa_2ld(domain)


def n_grams_dict(domain):
    """
    Returns similarity to distribution of N-grams in English dictionary

    :param domain: Domain (string)

    """
    return analyse.get_grams_dict_2ld(domain)
