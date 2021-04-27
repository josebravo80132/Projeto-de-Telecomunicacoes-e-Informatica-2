import time
import socket
import sys
from threading import Thread

message_enviar = -1
ip_inicial = -1
ip_final = -1
tipo_teste = -1
d1 = -1



class Th(Thread):
	def __init__ (self, num, ip):
		Thread.__init__(self)
		self.num = num
		self.ip = ip
		self._return = None 

	def run(self):

		Tcp_port = 5005

		Buffer = 1024

		msg = "start "
		Msg_env1 = msg+ip_inicial+" "+ip_final
		
		s_inicial = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_inicial.connect((self.ip, Tcp_port))
		s_inicial.send(Msg_env1.encode())
		data_i = s_inicial.recv(Buffer)
		global d1
		d1 = data_i.decode()
		s_inicial.close()
		print(d1)
		self._return = d1

	def join(self):
		Thread.join(self)
		return self._return



def begin():
	return 'b'


def start():
	return 'e'


def tutorial():
	return 'c'


def sair():
	print("O servidor encerrrou sessao.")
	return 'd'

def m():

	print("o teste fez o espectavel")
	return 1

def lista_peers():
	return 'l'


def lista_testes():
	return 'b'



def com_udp(ip_inicial, ip_final):

	Tcp_ip_inicial = ip_inicial
	Tcp_ip_final = ip_final

	a = Th(1, ip_inicial)
	b = Th(2, ip_final)
	
	
	a.start()
	b.start()

	res = a.join()
	
	return res


def latencia():

	global ip_inicial
	global ip_final

	msg = "start "
 
	m = com_udp(ip_inicial, ip_final)

	return m

def Perda_pacotes():
	return 'b'


def Largura_banda():
	return 'b'

def Disponibilidade():
	return 'b'


def switch_serv(number):

	switcher = {
		'a':begin,
		'b':start,
		'c':tutorial,
		'd':sair,
		'e':lista_peers,
		'f':m,
		'g':m,
		'h':m,
		'i':m,
		'j':m,
		'k':lista_testes,
		'l':latencia,
		'm':Perda_pacotes,
		'n':Largura_banda,
		'o':Disponibilidade,
		'p':m
	}

	func = switcher.get(number)
	return func()


def server_program():
	# get the hostname
	host = sys.argv[1]
	port = 5000  # initiate port no above 1024

	server_socket = socket.socket()  # get instance
	# look closely. The bind() function takes tuple as argument
	server_socket.bind((host, port))  # bind host address and port together

	# configure how many client the server can listen simultaneously
	server_socket.listen(2)
	conn, address = server_socket.accept()  # accept new connection
	print("Connection from: " + str(address))
	while True:
		# receive data stream. it won't accept data packet greater than 1024 bytes
		data = conn.recv(1024).decode()
		if not data:
			# if data is not received break
			break

		else :

			global message_enviar

			if( len(data)>2):

				x=data.split(" ", 1)

				global ip_inicial
				global ip_final

				ip_inicial = x[0]
				ip_final = x[1]
				message_enviar = 'k'


			if( len(data)==1):
				x=data
				print(x)
				print("oalolaoal \n")
				message_enviar = switch_serv(x)
				print(message_enviar)

			print("from connected user: " + str(data))
			conn.send(str(message_enviar).encode())  # send data to the client

	conn.close()  # close the connection


if __name__ == '__main__':
	server_program()

