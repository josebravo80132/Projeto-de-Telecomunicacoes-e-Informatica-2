import socket
from threading import Thread

serverIP = '10.0.0.10' #socket.gethostbyname(socket.gethostname())
gestorIP = '10.0.0.20'

TCP_PORT = 5000

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


class activatePeers_thread(Thread):

	def __init__(self, peer_socket, message):
		Thread.__init__(self)
		self.peer_socket = peer_sockets
		self.message = message

	def run(self):
		while True:
			peer_socket.send(message.encode())
			peer_socket.settimeout(10)
			try: 
				res = peer_socket.recv(1024)
			except:
				print("An exception ocurred, timeout?")
				peer_socket.close()
				break
			#sendResult_Gestor(res)
			print("-Monitorization Result: "+str(res))
			break
			


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
	while 1:
		gestorRequest = waitGestorRequest().decode()
		print("Gestor Request: "+str(gestorRequest))
		
		requestFields = gestorRequest.split()
		typeID = requestFields[0]
		teste = requestFields[1]
		peerA_IP = requestFields[2]
		peerB_IP = requestFields[3]
		optional = requestFields[4]
		
		message = typeID+' '+teste+' '+peerB_IP+' '+optional

		socket_peer_inicial = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_peer_final = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_peer_inicial.connect((peerA_IP, TCP_PORT))
		socket_peer_final.connect((peerB_IP, TCP_PORT))

		thread_inicial = activatePeers_thread(socket_peer_inicial, message)
		thread_final = activatePeers_thread(socket_peer_final, message)

		#socket_peer.connect()
		#activatePeers(gestorRequest)
		#monitorizationResult = waitPeerResult()
		#print("Monitorization Result: "+str(monitorizationResult))
		#sendResult_Gestor(monitorizationResult)
