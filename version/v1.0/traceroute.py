import time
import socket
import sys
import os
import argparse




def traceroute_1(ip_destino):

	f = open("ip_texto","w+")
	
	s = str(ip_destino)
	f.write(s)
	f.close()

	program = '''
	


x = open("ip_texto","r")
y = x.read()

print(y)

frase = 'traceroute ' + y

print(frase)

z = os.popen(frase).read()

print(z)

'''
	exec(program)

#----------------->  <________________________

z = input()
traceroute_1(z)
