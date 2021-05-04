import socket
import time
import secrets

local_ip = socket.gethostbyname(socket.gethostname())
serverIP = socket.gethostbyname("serverIP")
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
            elif teste == "2":
                getLostPackets(requestFields)

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
                message = (str(counter) + " ").encode()
                sendUDP_message(message, destinationIP)
                counter = counter + 1
            print("Finished ...")

def getLostPackets(requestFields):
        destinationIP = requestFields[2]
        nPackets = int(requestFields[3])
        start_timer = time.time()
        if destinationIP == local_ip:
            waitUDP_message(2, 5)
        else:
            counter = 0
            while counter < nPackets:
                data = str(secrets.token_bytes(1020))
                data = data.replace(" ", "-")				
                message = ((str(counter) + " ")+data).encode()
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
        tmstpAUX = 0
        while True:
            try:
                receivedData, addr = socket_UDP.recvfrom(1024)
                if test == 1:
                       dataFields = receivedData.decode().split()
                       tmstpAUX += time.time()-float(dataFields[1])
                print("(UDP) Received Packet " +str(packetCounter)+": "+str(receivedData))
                packetCounter = packetCounter + 1
            except:
                if test == 1:
                    print("Monitoring Finished - Latencia Media = " +
                          str(tmstpAUX/packetCounter)+" ")
                    sendTCP_Server(1, test, str(tmstpAUX/packetCounter))
                    
                elif test == 2:
                    print("Monitoring Finished - Pacotes Recebidos = " +
                          str(packetCounter)+" ")
                    sendTCP_Server(1, test, str(packetCounter))
                break

def sendUDP_message(message, destinationIP):
        print("(UDP) Sending for Peer "+str(destinationIP)+" ...")
        socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timestamp = time.time()
        udpMSG = message + str(timestamp).encode()
        socket_UDP.sendto(udpMSG, (destinationIP, UDP_PORT))
        print("(UDP) Sent +"+str(udpMSG)+" ...")

def sendTCP_Server(typeID, teste, resultado):
        # |ID| TESTE | Resultado | Opcional |
        message = str(typeID)+' '+str(teste)+' '+str(resultado)
        print("Starting TCP connection with "+serverIP+" ...")
        port = 5000

        # socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket_TCP.connect((serverIP, port))
        socket_TCP.send(message.encode())
        socket_TCP.close()

if __name__ == '__main__':
        while 1:
            server_message = waitServerRequest().decode()
            print("Received from Server: "+server_message)
            processRequest(server_message)
