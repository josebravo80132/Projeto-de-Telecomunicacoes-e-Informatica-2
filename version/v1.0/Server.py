import socket

serverIP = '10.0.0.10' #socket.gethostbyname(socket.gethostname())
gestorIP = '10.0.0.20'

def waitGestorRequest():
    port = 5000

    print("*** Server ***\n Waiting on port "+str(port)+" ...")
    socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_TCP.bind((serverIP, port))
    socket_TCP.listen(1)
    connection, address = socket_TCP.accept()
    print("Connected from "+str(address))
    #gestorIP = address[0]
    while True:
        gestorRequest = connection.recv(1024)
        if not gestorRequest:
            break
        return gestorRequest 

def activatePeers(request):
    #|ID| TESTE | IP_Inicial | IP_Final | Opcional |
    requestFields = request.split()
    typeID = requestFields[0]
    teste = requestFields[1]
    peerA_IP = requestFields[2]
    peerB_IP = requestFields[3]
    optional = requestFields[4]

    #|ID| TESTE | IP_Final | Opcional |
    message = typeID+' '+teste+' '+peerB_IP+' '+optional
    print("Starting TCP connection with "+peerA_IP+" ...")
    port = 5000

    socket_peerA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_peerA.connect((peerA_IP, port))
    socket_peerA.send(message.encode())
    socket_peerA.close()

    print("Starting TCP connection with "+peerB_IP+" ...")
    port = 5000

    socket_peerB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_peerB.connect((peerB_IP, port))
    socket_peerB.send(message.encode())
    socket_peerB.close()

def waitPeerResult():
    port = 5000

    print("*** Server ***\n (TCP) Waiting Peer result on port "+str(port)+" ...")
    socket_result = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_result.bind((serverIP, port))
    socket_result.listen(1)
    connection, address = socket_result.accept()
    print("Connected from "+str(address))
    while True:
        peerResult = connection.recv(1024)
        if not peerResult:
            break
        return peerResult 

def sendResult_Gestor(resultado):
    port = 5005

    print("(TCP) Connecting to Gestor "+str(gestorIP)+" ...")
    socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_TCP.connect((gestorIP, port))
    socket_TCP.send(resultado)
    socket_TCP.close()


if __name__ == '__main__':
    gestorRequest = waitGestorRequest().decode()
    print("Gestor Request: "+str(gestorRequest))
    activatePeers(gestorRequest)
    monitorizationResult = waitPeerResult()
    print("Monitorization Result: "+str(monitorizationResult))
    sendResult_Gestor(monitorizationResult)
