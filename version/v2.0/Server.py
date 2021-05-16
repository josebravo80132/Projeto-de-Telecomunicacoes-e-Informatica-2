import socket
from threading import Thread
import time
import errno

serverIP = socket.gethostbyname(socket.gethostname())
gestorIP =  socket.gethostbyname("gestorIP")

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


class activatePeers_thread(Thread):

	def __init__(self, peer_socket, message):
		Thread.__init__(self)
		self.peer_socket = peer_socket
		self.message = message

	def run(self):

		self.peer_socket.sendall(message.encode())
		(peer_addr, peer_port) = self.peer_socket.getpeername()
		while peer_addr == peerB_IP:
			print("Entrou no while")
			self.peer_socket.settimeout(20)
			try: 
				res = self.peer_socket.recv(1024).decode()
			except socket.error as e:
				err = e.args[0]
				if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
					sleep(1)
					print("No data available")
					continue
				else:
					print(e)
					self.peer_socket.close()
					break
			print(res)
			sendResult_Gestor(res)
			break	

		self.peer_socket.shutdown(socket.SHUT_RDWR)
		self.peer_socket.close()	

def sendResult_Gestor(resultado):
	port = 5005

	print("(TCP) Connecting to Gestor "+str(gestorIP)+" ...")
	socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_TCP.connect((gestorIP, port))
	socket_TCP.send(resultado.encode())
	socket_TCP.close()


if __name__ == '__main__':

	threads = []
	
	while 1:
		gestorRequest = waitGestorRequest().decode()
		print("Gestor Request: "+str(gestorRequest))

		socket_peer_inicial = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_peer_final = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		

		requestFields = gestorRequest.split()
		typeID = requestFields[0]
		teste = requestFields[1]
		peerA_IP = requestFields[2]
		peerB_IP = requestFields[3]
		optional = requestFields[4]

		socket_peer_inicial.connect((peerA_IP, TCP_PORT))
		socket_peer_final.connect((peerB_IP, TCP_PORT))
		
		
		message = typeID+' '+teste+' '+peerB_IP+' '+optional


		thread_inicial = activatePeers_thread(socket_peer_inicial, message)
		thread_final = activatePeers_thread(socket_peer_final, message)

		thread_inicial.start()
		thread_final.start()

		threads.append(thread_inicial)
		threads.append(thread_final)

		for t in threads:
			t.join()


		#socket_peer.connect()
		#activatePeers(gestorRequest)
		#monitorizationResult = waitPeerResult()
		#print("Monitorization Result: "+str(monitorizationResult))
		#sendResult_Gestor(monitorizationResult)