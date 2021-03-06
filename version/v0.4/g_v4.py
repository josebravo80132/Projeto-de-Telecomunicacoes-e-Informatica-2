
import socket
import time
import sys

ip_inicial = -1
ip_final = -1
option_3 = 'a'

def print_menu():

	global option_3

	print("Bem vindo.Selecione uma opcao do menu:")
	print("1) Start.")
	print("2) Tutorial.")
	print("3) Sair.")

	option_3 = input()

	return option_3


def begin():
	return print_menu()


def tutorial():

	print("Bem vindo ao tutorial.")
	print("Selecione a opcao 1 para iniciar.")
	print("Na lista de peers na primeira escolha acrescente um " " e digite o segundo peer.")
	print("Depois selecione o teste a efetuar. ")
	print("Espere pelo o resultado do teste. ")
	print("Pode recomecar selecionando novos peers e novos testes.")
	print("Ou pressione 3 para sair.")

	option_3 = input()
	option_3 = 1

	return option_3

def lista_peers():

	global ip_inicial
	global ip_final

	print("A lista dos peers.Selecione dois peers:\n")
	print("5) 192.168.1.0")
	print("6) 192.168.1.0")
	print("7) 192.168.1.0")
	print("8) 192.168.1.0")
	print("9) 192.168.1.0")

	ip_inicial = input()
	ip_final = input()

	msg_env = ip_inicial+ip_final
	return msg_env

def lista_testes():

	global option_3

	print("A lista de testes. Selecione uma opcao :\n")
	print("11) Latencia.")
	print("12) Perda de Pacotes.")
	print("13) Largura de Banda.")
	print("14) Disponibilidade.")

	option_3 = input(b'')

	return option_3


def sair():

	global option_3
	option_3 = "bye"
	return option_3


def switch(number):

	switcher = {
		'b': print_menu,
		'c': tutorial,
		'd': sair,
		'e': lista_peers,
		'k': lista_testes,
		't': lista_testes
	}

	func = switcher.get(number)
	return func()

def client_program():
	host = sys.argv[1] # as both code is running on same pc
	port = 5000  # socket server port number

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server

	message = str('a')  # take input

	while message.lower().strip() != 'bye':

		client_socket.send(message.encode())  # send message
		data = client_socket.recv(1024).decode()  # receive response

		print('Received from server: ' + data)  # show in terminal
		
		if(len(data) >= 3):
			z=float(data)
			print(z)
			print(" O Resultado foi : " + str(z))
			time.sleep(10)
			message = str('a')
		else:
			message = switch(data)  # again take input


	client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
