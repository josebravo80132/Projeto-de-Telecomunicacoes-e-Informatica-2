import time
import socket
import sys
import os
import argparse

def disp():
	program = '''

x, y, z, w, t, u = {}, {}, {}, {}, {}, {}

output = os.popen('/etc/init.d/snmpd start').read()
output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.20.1.1 ').read()
x = output.split(" ")
output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.22.1.3 ').read()
y = output.split(" ")
output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.1.3 ').read()
z = output.split(" ")
output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.1.5 ').read()
w = output.split(" ")
output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.7.1 ').read()
t = output.split(" ")
output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.7.4 ').read()
u = output.split(" ")

	'''

	loc = {}

	exec(program, globals(), loc)

	texto, texto_v1, texto_v2, texto_v3 = [], [], [], []
	str_final = "" 

	for i in loc:

		if(i=='x'):
			texto.append("intf:")
			texto.extend(loc[i])
		if(i=='y'):
			texto.append(" ip_rlocal:")
			texto.extend(loc[i])
		if(i=='z'):
			texto.append(" t_act:")
			texto.extend(loc[i])
		if(i=='w'):
			texto.append(" nome:")
			texto.extend(loc[i])
		if(i=='t'):
			texto.append(" udp_rec:")
			texto.extend(loc[i])
		if(i=='u'):
			texto.append(" udp_env:")
			texto.extend(loc[i])

	for i in range(len(texto)):
		if("\n" in texto[i] or "intf:" in texto[i] or " ip_rlocal:" in texto[i] or " t_act:" in texto[i] or " nome:" in texto[i] or " udp_rec:" in texto[i] or " udp_env:" in texto[i]):
			texto_v1.append(texto[i])
			
	for i in range(len(texto_v1)):
		texto_v2.append(texto_v1[i].splitlines())
		
	for i in range(len(texto_v2)):
		for j in range(len(texto_v2[i])):
			word = texto_v2[i][j]
			if(len(word)<=15):
				texto_v3.append(word)
				
	for i in texto_v3: 
		str_final += i+' '  

	return str_final

a = disp()

print(a)


