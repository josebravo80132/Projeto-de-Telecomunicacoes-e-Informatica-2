import socket
import time

local_ip = socket.gethostbyname(socket.gethostname())
UDP_PORT = 8000


def waitServerRequest():
    port = 5000

    print("*** Peer ("+local_ip +
          ") ***\n (TCP) Waiting Server request on port "+str(port)+" ...")
    socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_TCP.bind((local_ip, port))
    socket_TCP.listen(1)
    connection, address = socket_TCP.accept()
    print("Connected from "+str(address))
    while True:
        serverRequest = connection.recv(1024)
        if not serverRequest:
            break
        return serverRequest


def processRequest(request):
    # |ID| TESTE | PeerDestino | Opcional
    requestFields = request.split()
    id = requestFields[0]

    if id == "0":
        teste = requestFields[1]
        if teste == "1":  # Substituir por SWITCH c/ todos os testes
            getLatencia(requestFields)


def getLatencia(requestFields):
    destinationIP = requestFields[2]
    # Elapsed > monitoringInterval => Timeout   if( media = 0 => resultado = ERROR ) else{ media > 0 => resultado = media}
    monitoringInterval = int(requestFields[3])
    start_timer = time.time()
    if destinationIP == local_ip:
        waitUDP_message(1, monitoringInterval)
    else:
        counter = 0
        while (time.time() <= start_timer + monitoringInterval):
            message = b'Hello World'
            sendUDP_message(message, destinationIP)
            counter = counter + 1
        print("Finished ...")


def waitUDP_message(test, timeout):
    print("(UDP) Waiting Peer message ...")
    timer_start = time.perf_counter()
    socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_UDP.bind((local_ip, UDP_PORT))
    socket_UDP.settimeout(int(timeout))
    packetCounter = 0
    while True:
        try:
            receivedData, addr = socket_UDP.recvfrom(1024)
            print("(UDP) Received Packet " +
                  str(packetCounter)+": "+str(receivedData))
            packetCounter = packetCounter + 1
        except:
            print("Monitoring Finished !")
            break


def sendUDP_message(message, destinationIP):
    print("(UDP) Sending for Peer "+str(destinationIP)+" ...")
    socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timestamp = time.time()
    udpMSG = message #+ timestamp
    socket_UDP.sendto(udpMSG, (destinationIP, UDP_PORT))
    print("(UDP) Sent +"+str(udpMSG)+" ...")


if __name__ == '__main__':
    while 1:
        server_message = waitServerRequest().decode()
        print("Received from Server: "+server_message)
        processRequest(server_message)
