import socket
import sqlite3
import time


def switch(number):

	switcher = {
		0: quit(),
        1: getMenuTestes()
	}

	func = switcher.get(number)
	return func()

def getMainMenu():
    print("*** Gestor ***")
    print("1 - Monitorização de rede ")
    #print("2 - Histórico de testes efetuados")
    print("0 - Sair")
    sel = int(input("Selecione uma opção: "))
    switch(sel)

def getMenuTestes():
    
    print(" *** Peers *** ")
    print("* 192.168.1.0 *")
    print("* 192.168.1.0 *")
    print("* 192.168.1.0 *")
    print("* 192.168.1.0 *")
    print("* 192.168.1.0 *")
    print(" ************* ")

    print(" *** Monitorização do estado da rede ***")
    print("1 - Latencia.")
    print("2 - Perda de Pacotes.")
    print("3 - Largura de Banda.")
    print("4 - Disponibilidade.")

    teste_selecionado = input("Selecione o teste a efetuar: ")
    peerInicial = input("Endereço do Peer inicial: ")
    peerFinal = input("Endereço do Peer destino: ")
    if teste_selecionado == "2":
        optional = input("Número de pacotes a enviar: ")
    else:
        optional = input("Intervalo de monitorização (s): ")

    # ID | Teste | Peer A | Peer B | Opcional/IntervaloMonitorizaçao
    messageToServer = '0 '+teste_selecionado+' '+peerInicial+' '+peerFinal+' '+optional
    connect_to_server(messageToServer)

    return [peerInicial, peerFinal]
    

def connect_to_server(message):
    serverIP = input("Endereço IP do servidor: ")
    port = 5000

    print("Starting TCP connection with "+serverIP+" ...")
    socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_TCP.connect((serverIP, port))
    socket_TCP.send(message.encode())
    socket_TCP.close()

def waitServerResult():
    gestorIP = '10.0.0.20' #socket.gethostbyname(socket.gethostname())
    port = 5005
    print("Waiting on port "+str(port)+" ...")

    socket_gestor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_gestor.bind((gestorIP, port))
    socket_gestor.listen(1)
    connection, address = socket_gestor.accept()
    print("Connected from "+str(address))
    while True:
        result = connection.recv(1024)
        if not result:
            break
        return result 
	

if __name__ == '__main__':
    while 1:
	    #getMainMenu()
	    conn = sqlite3.connect("localhost")
	    print("Garantido acesso a base de dados\n")
	    print("1 - Menu de Monitorizacao")
	    print("2 - Aceder a base de dados")
	    opcao = input("Escolha a opcao: ")
	    if opcao == "1":
	    	aux = getMenuTestes()
	    	server_result = waitServerResult().decode()
	    	x = server_result.split()
	    	conn.execute("INSERT INTO TESTES (ID, PEER_I, PEER_F, RESULT) VALUES(?,?,?,?)", (x[1], aux[0], aux[1],  x[2]))
	    	conn.commit()
	    	print("Adicionado com sucesso a base de dados")
	    	print("\n Resultado: "+str(server_result))
	    if opcao == '2':
	   		cursor = conn.execute("SELECT SEQ, ID, PEER_I, PEER_F, RESULT, TIMESTAMP from TESTES")

	   		for row in cursor:
	   			print("SEQ = ", row[0])
	   			print("ID = ", row[1])
	   			print("PEER_I = ", row[2])
	   			print("PEER_F = ", row[3])
	   			print("RESULT = ", row[4])
	   			print("TIMESTAMP = ", row[5])

	   		print("Operacao Concluida!")