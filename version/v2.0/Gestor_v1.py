import socket


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
    # print("2 - Histórico de testes efetuados")
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
    if teste_selecionado == "1":
        optional = input("Intervalo de monitorização (s): ")
    elif teste_selecionado == "2":
        optional = input("Número de pacotes a enviar: ")
    elif teste_selecionado == "3":
        optional = "-"

    # ID | Teste | Peer A | Peer B | Opcional/IntervaloMonitorizaçao
    messageToServer = '0 '+teste_selecionado + \
        ' '+peerInicial+' '+peerFinal+' '+optional
    connect_to_server(messageToServer)


def connect_to_server(message):
    serverIP = input("Endereço IP do servidor: ")
    port = 5000

    print("Starting TCP connection with "+serverIP+" ...")
    socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_TCP.connect((serverIP, port))
    socket_TCP.send(message.encode())
    socket_TCP.close()


def waitServerResult():
    gestorIP = socket.gethostbyname(socket.gethostname())
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


def printMonitorizationResult(resultado):
    # ID TipoTeste Resultado (10.0.18.1),(10.0.2.1),(10.0.1.1),
    resultFields = resultado.split()
    expectedRoute = resultFields[3].split(",")
    print(expectedRoute)


    if resultFields[1] == "1":
        print("\n*** Resultado ***\n"+'Latencia entre : '+str(expectedRoute[0])+' -> '+str(expectedRoute[-1])+'\n Resultado: '+format(
        float(resultFields[2]), ".9f")+'s \n')

    elif resultFields[1] == "2":
        print("\n*** Resultado ***\n"+' Tipo de Teste: '+str(resultFields[1])+'\n Resultado: '+str(
        resultFields[2])+'\n Rota Expectável: '+str(resultFields[3])+'\n')
    
    elif resultFields[1] == "3":
        print("\n*** Resultado ***\n"+' Tipo de Teste: '+str(resultFields[1])+'\n Resultado: '+str(
        resultFields[2])+'\n Rota Expectável: '+str(resultFields[3])+'\n')

    elif resultFields[1] == "4":
        print("\n*** Resultado ***\n"+' Tipo de Teste: '+str(resultFields[1])+'\n Resultado: '+str(
        resultFields[2])+'\n Rota Expectável: '+str(resultFields[3])+'\n')
    

if __name__ == '__main__':
    while 1:
	    # getMainMenu()
        getMenuTestes()
        server_result = waitServerResult().decode()
        printMonitorizationResult(server_result)