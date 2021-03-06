#!/usr/bin/env python

import socket
import time
import sys

milliseconds_inicial = -1
milliseconds_final = -1


Tcp_ip_do_peer_self = sys.argv[1]
Tcp_port_self = 5005

BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((Tcp_ip_do_peer_self, Tcp_port_self))
s.listen(3)


conn, addr = s.accept()
print('Connection address:', addr)


while 1:
	s.settimeout(60)
	try:
		data = conn.recv(BUFFER_SIZE)
	except:
		print('TCP Timeout')
		conn.send(b'd')
	if not data: break
	else:

		busca_ip = data.decode()
		x = busca_ip.split(" ",2)

		if(x[1] == Tcp_ip_do_peer_self):

			ip_inicial = x[1]
			ip_final = x[2]
			i=0

			while(i<10):
				UDP_IP = ip_final
				UDP_PORT = 5010

				MESSAGE = b"Hello, World!"
				print("UDP target IP: %s" % UDP_IP)
				print("UDP target port: %s" % UDP_PORT)
				print("message: %s" % MESSAGE)

				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

				milliseconds_inicial_1 = float(round(time.time() * 10000000))

				print("comecou\n")
				print(milliseconds_inicial_1)
				print("\n 2222comecou 22222222222222\n")

				sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
				sock.close()
				i+=1

			UDP_IP = ip_inicial
			UDP_PORT = 5015

			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.bind((UDP_IP, UDP_PORT))
			sock.settimeout(5)

			try :
				data, addr = sock.recvfrom(1024) # buffer size is 1024 bytel
				milliseconds_final = float(round(time.time() * 10000000))
			except:
				print('timeout')
				conn.send(b'd')
			print("comecou\n")
			print(milliseconds_inicial_1)
			print("\n Recebeu \n")
			print("received message: %s" % data)

			mensagem = float(milliseconds_final) - float(milliseconds_inicial_1)
			print("REsultado finaL: "+ str(mensagem))
			conn.send(str(mensagem).encode())
			sock.close()


		else:
			ip_inicial = x[1]
			ip_final = x[2]

			UDP_IP = ip_final
			UDP_PORT = 5010

			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			sock.bind((UDP_IP, UDP_PORT))
			sock.settimeout(5)

			try:
				data, addr = sock.recvfrom(1024) # buffer size is 1024 byte
				print("received message: %s" % data)
			except:
				print('timeout')
				conn.send(b'd')
			sock.close()

			t=0
			while(t<15):
				UDP_IP = ip_inicial
				UDP_PORT = 5015
				MESSAGE = b"comunicacao de volta "
				print("UDP target IP: %s" % UDP_IP)
				print("UDP target port: %s" % UDP_PORT)
				print("message: %s" % MESSAGE)

				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
				sock.close()
				t+=1

	# 	if(milliseconds_inicial == -1):
	# 		msg_ip_final = (float(milliseconds_final))
	# 	else:
	# 		msg_ip_final = (float(milliseconds_inicial))

	# print("received data:", data)
	# conn.send(str(msg_ip_final).encode())  # echo
conn.close()