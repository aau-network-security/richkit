"""Confidentiality-aware look-ups for data on domain names.

This modules provides the ability to look up domain names in local
resources, i.e. the domain name cannot be sent of to third
parties. The module might fetch resources, such as lists or
databasese, but this must be done in a way that keeps the domain name
confidential. Contrast this with `dat.retrieve`."""
