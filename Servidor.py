import socket

def wait_gestor():
    #Comunicação gestor-servidor
    HOST = '10.0.0.10'
    PORT = 5000       

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for new connections...")
        connection, address = s.accept()    # Bloqueia e espera conexão do gestor
        with connection:
            print('Connected by', address)
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                connection.sendall(data)
                return data

def activatePeers(comandoRecebido):
    cmds = comandoRecebido.decode().split()
    #requestID = comandoRecebido[0]
    requestedTest = cmds[1]
    peerA_IP = cmds[2]
    peerB_IP = cmds[3]
    timeout = cmds[4]

    PORT = 5000
    startMSG = '0 '+requestedTest+' '+peerB_IP
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((peerB_IP, PORT))
        # ID | tipoTeste | peerDestino | Opcional
        sock.send(startMSG.encode())
        print("Activating "+peerB_IP+'...')
        sock.close()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as initialSocket:
        initialSocket.connect((peerA_IP, PORT))
        # ID | tipoTeste | peerDestino | Opcional
        initialSocket.send(startMSG.encode())
        print("Ativating "+peerA_IP+'...')

    return timeout

def waitPeersResponse(timeout):
    HOST = '10.0.0.10'
    PORT = 5000       

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for peers response...")
        connection, address = s.accept()    # Bloqueia e espera conexão do peer
        with connection:
            print('Connected by', address)
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                return data    


if __name__ == '__main__':
	
    gestorCMD = wait_gestor() ## ID | TipoTeste | PeerA | PeerB | Opcional
    timeout = activatePeers(gestorCMD)
    waitPeersResponse(timeout)
        

    