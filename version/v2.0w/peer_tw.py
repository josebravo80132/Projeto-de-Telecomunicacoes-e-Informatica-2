import socket
import time
import secrets
import subprocess
import errno

local_ip = socket.gethostbyname(socket.gethostname())
serverIP = socket.gethostbyname("serverIP")
UDP_PORT = 8000
TCP_PORT = 5000


def waitServerRequest():

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
        elif teste == "3":
            getBandwidth(requestFields)
        elif teste == "4":
            getDisponibilidade(requestFields)


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
        time.sleep(1)
        counter = 0
        while counter < nPackets:
            data = str(secrets.token_bytes(1020))
            data = data.replace(" ", "-")
            message = ((str(counter) + " ")+data).encode()
            sendUDP_message(message, destinationIP)
            counter = counter + 1
        print("Finished ...")

def getBandwidth(requestFields):
    destinationIP = requestFields[2]
    nPackets = 10000
    if destinationIP == local_ip:
        waitUDP_message(3, 1)
    else:
        counter = 0
        while counter < nPackets:
            data = str(secrets.token_bytes(1000))
            data = data.replace(" ", "-")
            message = data.encode()
            sendUDP_message(message, destinationIP)
            counter = counter + 1
        print("Finished ...")

def getDisponibilidade(requestFields):
    destinationIP = requestFields[2]
    nTentativas = int(requestFields[3])
    start_timer = time.time()
    if destinationIP == local_ip:
        waitUDP_message(4, 5)
    else:
        counter = 0
        while (counter < nTentativas):
            time.sleep(0.1)
            message = (str(counter) + " ").encode()
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
            receivedData, (fromIP, ports) = socket_UDP.recvfrom(1024)
            packetCounter = packetCounter + 1
            if test == 1 or test == 4:
                dataFields = receivedData.decode().split()
                tmstpAUX += time.perf_counter()-float(dataFields[1])
           
        except socket.error as e:
            err = e.args[0]
            if err == errno.ETIMEDOUT:
                if test == 1:
                    print("Monitoring Finished - Latencia Media = " +
                          str(tmstpAUX/packetCounter)+" segundos")
                    socket_UDP.settimeout(None)
                    sendTCP_Server(1, test, str(tmstpAUX/packetCounter), fromIP)

                elif test == 2:
                    print("Monitoring Finished - Pacotes Recebidos = " +
                          str(packetCounter)+" ")
                    sendTCP_Server(1, test, str(packetCounter), fromIP)
                elif test == 3:
                    timer_end = time.perf_counter()
                    result_bw = ((packetCounter*1000)/(timer_end-timer_start))
                    print("Demorou "+format((timer_end-timer_start),".2f")+ " segundos a transmitir 10 Mb")
                    print("Monitoring Finished - Largura de banda = " + 
                        format(((packetCounter*1000)/(timer_end-timer_start)), ".2f")+ " bytes/seg" )
                    sendTCP_Server(1, test, result_bw, fromIP )
                elif test == 4:
                    if packetCounter == 0:
                        print("Nao disponivel")
                        sendTCP_Server(2, test, "-1", fromIP)
                    else:
                        print("Monitoring Finished - Teste de disponibilidade tempo de contacto = " + str(tmstpAUX/packetCounter))
                        sendTCP_Server(1, test, str(tmstpAUX/packetCounter), fromIP)
            else:
                print("Socket error: " + err)
                sendTCP_Server(2, "-1", "-1", fromIP) 
            break


def sendUDP_message(message, destinationIP):
    socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timestamp = time.perf_counter()
    udpMSG = message + str(timestamp).encode()
    socket_UDP.sendto(udpMSG, (destinationIP, UDP_PORT))
    print("(UDP) Sending for Peer "+str(destinationIP)+" ...")


def sendTCP_Server(typeID, teste, resultado, tracerouteIP):
    rota = execute("traceroute", tracerouteIP)
    message = str(typeID)+' '+str(teste)+' '+str(resultado)+' '+str(rota)
    print(message)
    print("(TCP) Sending result to server ("+serverIP+") ...")
    connection.send(message.encode())


def execute(comando, arg1):
    print("\nExecuting "+comando)
    res = subprocess.run([comando, arg1], stdout=subprocess.PIPE).stdout.decode(
        'utf-8').split("\n")
    res.pop(0)
    res.pop(len(res)-1)
    #print(res)
    interfacesIP = ""
    for line in res:
        fields = line.split("  ")
        #print(fields)
        fields = fields[1].split()
        interfacesIP += str(fields[1])+","
    interfacesIP = interfacesIP[:-1]
    return interfacesIP


if __name__ == '__main__':
    socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_TCP.bind((local_ip, TCP_PORT))

    while True:
        print("*** Peer ("+local_ip +
              ") ***\n (TCP) Waiting Server request on port "+str(TCP_PORT)+" ...")
        socket_TCP.listen(1)
        connection, address = socket_TCP.accept()

        server_message = waitServerRequest().decode()
        print("Received from Server: "+server_message)
        processRequest(server_message)
        time.sleep(4)