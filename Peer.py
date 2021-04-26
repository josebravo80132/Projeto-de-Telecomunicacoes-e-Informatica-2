import socket

local_ip = '10.0.16.20' #socket.gethostbyname(socket.gethostname())

def waitForServer():
    #Comunicação Servidor-Peer
    print(local_ip)
    PORT = 5000       

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((local_ip, PORT))
        s.listen()
        print("Waiting for new connection from Server...")
        connection, address = s.accept()    # Bloqueia e espera conexão do servidor
        with connection:
            print('Connected by', address)
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                return data

def send_UDP(server_message):
    destinationIP = server_message[2]
    print('Sending to '+destinationIP+' via UDP ...')

def wait_UDP(server_message):
    print('Waiting via UDP...')

if __name__ == '__main__':
    # ID | tipoTeste | peerDestino | Opcional
    server_message = waitForServer().decode().split()
    
    if server_message[2] == local_ip:
        wait_UDP(server_message)
    else:
        send_UDP(server_message)

    



    