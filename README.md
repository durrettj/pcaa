# pcaa
Python CAA and Certificate Check

Usage: ./pcaa.py hostname domainname port

This script checks for the existence of a CAA record for a domain and, if one exists, checks the certificate on the host and port specified. This script works on all tls speaking services and suports SNI. It has been tested on smtps, https, sip-tls, imaps and some others.
