import socket

SERVER_AUTH = 42069

def getUI():

	global selected

	print("*** Bem-vindo ***")
	print("0 - Sair")
	print("1 - Monitorização de rede ")
	print("2 - Histórico de testes efetuados")

	selected = input("Selecione uma opção: ")
	return selected


def requestMonitorization():

	global teste_selecionado

	print(" *** Monitorização do estado da rede ***")
	print("1 - Latencia.")
	print("2 - Perda de Pacotes.")
	print("3 - Largura de Banda.")
	print("4 - Disponibilidade.")
	teste_selecionado = input("Selecione o teste a efetuar: ")
	timeout = input("Intervalo de monitorização (s): ")

	print(" *** Peers *** ")
	print("* 192.168.1.0 *")
	print("* 192.168.1.0 *")
	print("* 192.168.1.0 *")
	print("* 192.168.1.0 *")
	print("* 192.168.1.0 *")
	print(" ************* ")

	peerInicial = input("Endereço do Peer inicial: ")
	peerFinal = input("Endereço do Peer destino: ")

	connect_to_server(teste_selecionado, timeout, peerInicial, peerFinal)


#def connect_to_server(selectedTest, peerA, peerB, timeout):
def connect_to_server():
	HOST = '10.0.0.10'
	PORT = 5000
	available_peers = []
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		#Hello m0essage to server
		command = str(0)+str(SERVER_AUTH)
		print(command)
		s.send(command.encode('utf-8'))
		data = s.recv(1024)
		print(data)
		if data[0] == "0":
			i = 1
			peer_id = 0
			print(data[1:5])
			
			while(data[i:i+3] != None):
				peer = data[i:i+4]        
				available_peers.append(peer)
				i+4

			print("Available peers received:")
			option = "a"
			for peer in available_peers:
				print(option+") "+peer)
				option += 1


			# ID | TipoTeste | PeerA | PeerB | Opcional
			#command = '1'+selectedTest+peerA+peerB+timeout


if __name__ == '__main__':
	connect_to_server()
	