"""Analysis and computations on domain names.

This module provides functions that can be applied to a domain
name. Similarly to `dat.lookup`, and in contrast to `dat.retrieve`,
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


# aka tld
def tld(domain):
    """Returns the Effective Top-Level Domain (eTLD) (aka Public Suffix).

    The eTLD is extracted from the domain,

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


def t2ld(domain):
    """Returns the Effective Second-Level Domain (2LD) (aka Apex Domain).

    The 2LD, aka the Apex Domain, is extracted from the domain, using
    the `list of public suffixes <https://publicsuffix.org/list/>`_
    maintained by Mozilla

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


def t2label(domain):
    """Returns the Effective 2-level label.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


def nld(domain, n):
    """Returns the Effective N'th-Level Domain (eNLD).

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


def nlabel(domain, n):
    """Returns the Effective N'th-level label.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()



# aka num_tokens
def depth(domain):
    """Returns the effective depth of the domain,

    The depth is the number of labels in the domain.

    .. example:: `google.co.uk` is "effectively a 2LD. `google` is one
    label. The public suffix of `co.uk` is considered one label
    effectively. With effectively two labels, the effective depth is
    two.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka len
def length(domain):
    """Retuns the sum of count of characters for all labels.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


def language(domain):
    """Returns the best gues for the language of the domain.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka entropy2ld (approximately)
def entropy(s):
    """Returns the entropy of characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka ratio_vowels_2ld (approximately)
def ratio_vowels(s):
    """Returns the ratio vowels to all characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka num_vowels_2ld (approximately)
def number_vowels(s):
    """Returns the number vowels to all characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka ratio_consonants_2ld (approximately)
def ratio_consonants(s):
    """Returns the ratio consonants to all characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka num_consonants_2ld (approximately)
def number_consonants(s):
    """Returns the number consonants to all characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka ratio_numeric_2ld (approximately)
def ratio_numerics(s):
    """Returns the ratio numeric characters to all characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka num_numeric_2ld (approximately)
def number_numerics(s):
    """Returns the number numeric characters to all characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka ratio_special_2ld (approximately)
def ratio_specials(s):
    """Returns the ratio special characters to all characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka num_special_2ld (approximately)
def number_specials(s):
    """Returns the number special characters to all characters in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka num_word_2ld (approximately)
def number_words(s):
    """Returns the number of English word found in s.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka grams_alexa2ld
def n_grams_alexa(s):
    """Returns similarity to distribution of N-grams in Alexa Top 1M.

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()


# aka grams_dict2ld
def n_grams_alexa(s):
    """Returns similarity to distribution of N-grams in English dictionary

    .. todo:: Implement this.
    .. todo:: Test this.

    """
    raise NotImplementedError()
