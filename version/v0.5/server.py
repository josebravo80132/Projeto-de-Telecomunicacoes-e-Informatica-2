import time
import socket
import sys
from threading import Thread

SELF_IP ='0.0.0.0'

TCP_PORT = 5000       
UDP_PORT = 8000

def getAvailablePeers():
	print("Available peers")

class manager_thread(Thread):

	def __init__(self, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		print("New thread for manager connection handling")

	def run(self):
		while True:
			data = conn.recv(10).decode()
			print(data)

			if data[0] == "0" : 
				getAvailablePeers()
				a = socket.inet_aton('192.168.0.1')
				b = socket.inet_aton('192.168.0.2')
				c = socket.inet_aton('192.168.0.3')
				response =b'0' + a + b + c 
				print(response)
				conn.send(response)
				break


if __name__ == '__main__':

	tcp_manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_manager.bind((SELF_IP, TCP_PORT))
	threads = []

	while True:
		tcp_manager.listen(4)
		print("Waiting for connections from managers")
		(conn, (ip, port)) = tcp_manager.accept()
		thread_man = manager_thread(ip, port)
		thread_man.start()

		threads.append(thread_man)

		for t in threads:
			t.join()

		

	