import socket
from threading import Thread
import time
import errno

serverIP = socket.gethostbyname(socket.gethostname())
gestorIP =  socket.gethostbyname("gestorIP")

TCP_PORT = 5000


class gestor_thread(Thread):
	def __init__(self, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		print("New thread for manager connection handling")
		

	def run(self):
		socket_peer_inicial = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_peer_final = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		peer_threads = []

		while True:
			gestorRequest = conn.recv(1024).decode()
			print(gestorRequest)

			requestFields = gestorRequest.split()
			typeID = requestFields[0]
			teste = requestFields[1]
			peerA_IP = requestFields[2]
			global peerB_IP
			peerB_IP = requestFields[3]
			optional = requestFields[4]

			socket_peer_inicial.connect((peerA_IP, TCP_PORT))
			socket_peer_final.connect((peerB_IP, TCP_PORT))
			
			global message
			message = typeID+' '+teste+' '+peerB_IP+' '+optional
			print(message)

			thread_inicial = peers_thread(socket_peer_inicial, message, conn)
			thread_final = peers_thread(socket_peer_final, message, conn)

			thread_inicial.start()
			thread_final.start()

			peer_threads.append(thread_inicial)
			peer_threads.append(thread_final)

			for t in peer_threads:
				t.join()

			conn.close()

			break

class peers_thread(Thread):

	def __init__(self, peer_socket, message, gestor_conn):
		Thread.__init__(self)
		self.peer_socket = peer_socket
		self.message = message
		self.gestor_conn = gestor_conn

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
			self.gestor_conn.send(res.encode())
			break	

		self.peer_socket.shutdown(socket.SHUT_RDWR)
		self.peer_socket.close()	

if __name__ == '__main__':


	print("*** Server ***\n Waiting on port "+str(TCP_PORT)+" ...")
	socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_TCP.bind((serverIP, TCP_PORT))

	threads_gestor = []
	
	while 1:
		socket_TCP.listen(1)
		(conn,(ip,port)) = socket_TCP.accept()
		thread_g = gestor_thread(ip, port)
		thread_g.start()

		threads_gestor.append(thread_g)

		for t in threads_gestor:
			t.join()
