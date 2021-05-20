import socket
from threading import Thread
import time
import errno
import subprocess
import sqlite3

serverIP = socket.gethostbyname(socket.gethostname())
gestorIP =  socket.gethostbyname("gestorIP")

TCP_PORT = 5000


def storeDB(result):
	res_fields = result.split(" ")
	test_id = res_fields[1]
	test_res = res_fields[2]
	traceroute = res_fields[3]
	tr_split = traceroute.split(",") 
	peer_inicial = tr_split[0]
	peer_final = tr_split[-1]


	print(f"ID teste: {test_id}\nResultado: {test_res}\nPeer inicial: {peer_inicial}\nPeer final: {peer_final}\nTraceroute: {traceroute}")
	connDB = sqlite3.connect("/home/jose/Documents/pti2/Projeto-de-Telecomunicacoes-e-Informatica-2/nodelogin/localhost")
	#connDB.execute('''CREATE TABLE IF NOT EXISTS TESTES (ID bigint(20) AUTO_INCREMENT,TESTE text, PEER_I text, PEER_F text, RESULT text, TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)''')
	connDB.execute("INSERT INTO TESTES (ID, PEER_I, PEER_F, RESULT) VALUES(?,?,?,?)", (test_id, peer_inicial, peer_final, test_res))
	connDB.commit()

	# cursor = connDB.execute("SELECT ID, PEER_I, PEER_F, RESULT from TESTES")

	# for row in cursor:
	# 	print("ID = ", row[0])
	# 	print("PEER_I = ", row[1])
	# 	print("PEER_F = ", row[2])
	# 	print("RESULT = ", row[3])

	connDB.close


def message_ID(i):
	switcher= {	0: teste(),	1: result(), 2: error()}

def runPing(ip, nTries):
	res = subprocess.run(["ping", ip, "-c", nTries], stdout=subprocess.PIPE).stdout.decode(
		'utf-8').split("\n")

	response = res.pop(-3)
	print(response)
	result = response.split(',')
	packets_received = int((result[1].split(' '))[1])
	packet_loss_perc = (result[2].split('%'))[0]

	if(packets_received != 0):
		time_info = res.pop(-2)
		avg_time =(time_info.split('/'))[4]
		return  avg_time
	else:
		return(-1)
	# len(res) > 1
	# time_info = res.pop(-1)

	# res.pop(len(res)-1)


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

			if int(teste) == 4 and peerB_IP == "0":
				result = runPing(peerA_IP, optional)
				message_result = "1 " + "4 " + peerA_IP + " " + peerB_IP + " " +  result
				storeDB(message_result)
				conn.send(message_result.encode())

			else:
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
			storeDB(res)
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
