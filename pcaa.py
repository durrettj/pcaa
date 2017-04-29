#!/usr/bin/python
 import sys
 import dns.resolver
 from sys import argv, stdout
 from socket import socket
 from OpenSSL.SSL import TLSv1_METHOD, Context, Connection
 
 
 if len(argv) <= 1:
     print 'Error: Specify a hostname!\n'
     print 'Usage: ./pcaa.py hostname domainname port\n'
     print 'Note: Pay attention to the spaces.'
     exit()
 
 
 domain = argv[2]
 host = argv[1] + '.' + argv[2]
 port = argv[3]
 
 print '\nChecking DNS for CAA records . . .\n'
 answers = dns.resolver.query(domain, 'CAA')
 print 'The following records were found:\n'
 for rdata in answers:
     print domain, 'in CAA', rdata.flags, rdata.value
 print '\nNow checking certificate . . . \n'
 print 'Using server name:', host, 'on port', port, 'for SNI ...'
 client = socket()
 stdout.flush()
 client.connect(('{0}'.format(host), int(port)))
 print 'Connected to', client.getpeername(), '\n'
 
 client_ssl = Connection(Context(TLSv1_METHOD), client)
 client_ssl.set_connect_state()
 client_ssl.set_tlsext_host_name(host)
 client_ssl.do_handshake()
 issuer = client_ssl.get_peer_certificate().get_issuer()
 issr = str(issuer)
 issr = issr.strip('<>')
 issr = issr.replace('X509Name object', 'Certificate Information: ')
 issr = issr.replace('C=', 'Country: ')
 issr = issr.replace('O=', 'Organization: ')
 issr = issr.replace('CN=', 'Common Name: ')
 issr = issr.split('/')
 for issr in issr:
     print issr
 print '\n'
 client_ssl.close()
 exit()
