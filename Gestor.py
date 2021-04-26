import socket


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


def connect_to_server(selectedTest, peerA, peerB, timeout):
    HOST = '10.0.0.10'
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # ID | TipoTeste | PeerA | PeerB | Opcional
        command = '0 '+selectedTest+' '+peerA+' '+peerB+' '+timeout
        s.send(command.encode())
        data = s.recv(1024).decode()

    print('Received', repr(data))


if __name__ == '__main__':
    selected_operation = getUI()    # Monitorizar ou Histórico de testes realizados
    requestMonitorization()