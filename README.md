# richkit

The Domain Analysis Toolkit (dat) is a python3 package that provides
tools taking a domain name as input, and returns addtional information
on that domain. It can be an analysis of the domain itself, looked up
from data-bases, retrieved from other services, or some combination
thereof.

The purpose of dat is to provide a reusable library of domain
name-related analysis, lookups, and retrieval functions, that are
shared within the Network Security research group at Aalborg
University, and also availble to the public for reuse and modification.

# Requirements

Todo: Describe requirements. We do py3. Anything else?

# Installation

Todo: installation procedure

# Usage

Todo: a usage example

# Features

Todo: Describe the data model of FQDN > APEX Domain > Public Suffix > TLD

Todo: Describe how the module is structured.

# Features Function for analyse examples

Below the functions for analyses with the respective outputs. This is the input domain `www.support.gooogle.co.uk`, s equal to the domain as well and n = `4`
```
- tld(domain) -> 'co.uk'
- sld(domain) -> 'google.co.uk'
- sl_label(domain) -> 'google'
- nld(domain, n) -> 'www.support.gooogle.co.uk'
- n_label(domain, n) -> 'www'
- depth(domain) -> '5'
- length(domain) -> '20'
- language(domain) -> 'en'
- entropy(s) -> '2.8553885422075336'
- ratio_vowels(s) -> '0.4166666666666667'
- number_vowels(s) -> '5'
- ratio_consonants(s) -> '0.4166666666666667'
- number_consonants(s) -> '5'
- ratio_numerics(s) -> '0.0'
- number_numerics(s) -> '0'
- ratio_specials(s) -> '0.0'
- number_specials(s) -> '0'
- number_words(s) -> '0'
- n_grams_alexa(domain) -> ''
- n_grams_dict(domain) -> ''
```
