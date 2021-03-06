
import socket
import time

SERVER_IP = 0

SELF_IP = '0.0.0.0'
TCP_PORT = 5000
UDP_PORT = 8000



class udp_socket:
	def __init__(ip, port):
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def bindSocket(self):
		self.sock.bind(self.ip, self.port)

	def closeSocket(self):
		self.sock.close()

	def receiveData(self, data_size):
		data, addr = self.sock.recvfrom(data_size)
		print("received message: %s" % data)
		return data

	def sendData(self, test_data):
		self.sock.sendto(test_data, (self.ip, self.port))


def send_result(tpt, result):
	res_message = b'1'+ tpt + result
	conn.send(res_message)

def loss_packets(n_MBytes, dest_peer_ip):

	destination_peer = udp_socket(dest_peer_ip, UDP_PORT)
	self_peer_udp = udp_socket(SELF_IP, UDP_PORT)
	self_peer_udp.bindSocket()
	self_peer_udp.sock.setdefaultimeout(10)

	n_pacotes = (n_MBytes*10**6)//1024
	
	if(SELF_IP != dest_peer_ip):				#origin peer for test

		for i in range(n_pacotes):
			packet = random.randbytes(1024)
			destination_peer.sendData(packet)

	else:										#destination peer for test
		i=0
		while(1):
			try:
				if(self_peer_udp.receiveData(1024) > len(0)):
					i+=1
			except:
				print("Timeout occured")
				break
		return i



def latency_test(n_messages, dest_peer_ip):
	milliseconds_inicial = 0
	milliseconds_final = 0

	destination_peer = udp_socket(dest_peer_ip, UDP_PORT)
	self_peer_udp = udp_socket(SELF_IP, UDP_PORT)
	self_peer_udp.bindSocket()

	if(SELF_IP != dest_peer_ip): 				#origin peer for test
		MESSAGE = b'1'
		print("UDP target IP: %s" % UDP_IP)
		print("UDP target port: %s" % UDP_PORT)
		print("message: %s" % MESSAGE)
		rtt_mean = 0
	
		for i in range(n_messages):

			milliseconds_inicial = float(round(time.time() * 10000000))
			destination_peer.sendData(MESSAGE)
			
			self_peer_udp.receiveData(1)
			milliseconds_final = float(round(time.time() * 10000000))
			res_mean =+ (milliseconds_final- milliseconds_inicial)

		res_mean = res_mean/n_messages
		self_peer_udp.closeSocket()
		return res_mean

	else:										#destination peer for test
		for i in range(n_messages):
			data = self_peer_udp.receiveData(1)
			milliseconds_final = float(round(time.time() * 10000000))
			data
			destination_peer.sendData(data)

		return 0



def m_interpreter(tpt, ipd, opc):
	if(tpt == "1"):
		ip_dest = socket.inet_ntoa(ipd)
		result = latency_test(10, ip_dest)
		if(SELF_IP != ipd):
			send_result(result)
		conn.close()

	if(tpt == "2"):
		ip_dest = socket.inet_ntoa(ipd)
		result = loss_packets(10, ip_dest)
		if(SELF_IP == ipd):
			send_result(result)
		conn.close()

BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SELF_IP, TCP_PORT))
s.listen(1)

conn, server_addr = s.accept()
print('Connection address:', server_addr)
SERVER_IP = server_addr[0]

while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data: break
	else:

		server_request = data.decode().split()
		tpm = server_message[0]
		tpt = server_message[1]
		ipd = server_message[2]
		opc = server_message[3]

		print(tpm+"||"+tpt+"||"+ipd+"||"+opc)

		if(tpm == 1):
			m_interpreter(tpt, ipd, opc)

		else:
			print('error')
	
conn.close()



