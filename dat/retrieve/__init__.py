"""Retrieval of data on domain names.

This module provides the ability to retrieve data on domain names of
any sort. It comes without the "confidentiality contract" of
`dat.lookup`.

Ideas for additiaon sources:

 * urlvoid.com (all of the 36 services checked?)
 * Virus total
 * WHOIS (suggestion: pywhois)
 * github.com/aau-network-security/kraaler
 * Services on top of HTTPS Certificate Transparency logs
 * https://www.lucidchart.com/documents/edit/e1fc4013-d4db-41d5-ba47-01ac9ae19fa0/0_0

"""

def symantec_site_review(dn):
    raise NotImplementedError()
