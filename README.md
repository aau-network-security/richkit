<div align="center">
<h1>Richkit </h1>
</div>
<p align="center"> 
<div align="center">
   <!-- todo github actions buiild status  -->
  <a href="https://img.shields.io/pypi/pyversions/richkit">
    <img src="https://img.shields.io/pypi/pyversions/richkit" alt="GitHub release">
  </a>
   <a href="https://github.com/aau-network-security/richkit/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/richkit" alt="licence">
  </a>
  <div align ="center">
  <a href="https://github.com/aau-network-security/richkit/issues">
  <img src=https://img.shields.io/github/issues/aau-network-security/richkit?style=flat-square alt="issues">
  
  </a>
  <a href="https://github.com/aau-network-security/richkit/network/members">
  <img src=https://img.shields.io/github/forks/aau-network-security/richkit >
  </a>
  <a href="https://github.com/aau-network-security/richkit/stargazers">
  <img src=https://img.shields.io/github/stars/aau-network-security/richkit></a>
  </div>

 </div>

Richkit is a python3 package that provides tools taking a domain name as input, and returns addtional information on that domain. It can be an analysis of the domain itself, looked up from data-bases, retrieved from other services, or some combination thereof.

The purpose of richkit is to provide a reusable library of domain name-related analysis, lookups, and retrieval functions, that are shared within the Network Security research group at Aalborg University, and also availble to the public for reuse and modification.


# Requirements

 - `Python >= 3.5` 

# Installation

In order to install richikit just type in the terminal `pip install richkit`


# Usage

The following codes can be used to retrieve the TLD and the URL category, respectively.

- Retriving effective top level domain of a given url: 
  
      ```python3
      from richkit.analyse import tld

      urls = ["www.aau.dk","www.github.com","www.google.com"]

      for url in urls:
         print(tld(url))
      ```
- Retriving category of a given url : 

   ```python3
   from richkit.retrieve.symantec import fetch_from_internet
   from richkit.retrieve.symantec import LocalCategoryDB

   urls = ["www.aau.dk","www.github.com","www.google.com"]

   local_db = LocalCategoryDB()
   for url in urls:
      url_category=local_db.get_category(url)
      if url_category=='':
         url_category=fetch_from_internet(url)
      print(url_category)
   ```

# Modules

Richkit define a set of functions categorized by the following modules:

- `richkit.analyse`: This module provides functions that can be applied to a domain  name. Similarly to `richkit.lookup`, and in contrast to `richkit.retrieve`, this is done without disclosing the domain name to third parties and breaching confidentiality.



- `richkit.lookup`: This modules provides the ability to look up domain names in local resources, i.e. the domain name cannot be sent of to third parties. The module might fetch resources, such as lists or databasese, but this must be done in a way that keeps the domain name confidential. Contrast this with `richkit.retrieve`.


- `richkit.retrieve`: This module provides the ability to retrieve data on domain names of any sort. It comes without the "confidentiality contract" of `richkit.lookup`.
