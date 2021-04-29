import time
import socket
import sys
import os

program = '''

x = {}

output = os.popen('nmap -PE/PP/PM -oG lista 10.0.0-21.0-21').read()
x = output.split(" ")

'''

loc = {}

exec(program, globals(), loc)

texto = []
texto.extend(loc['x'])

#print(texto)

texto_v1 = []
texto_v2 = []
texto_v3 = []
for i in range(len(texto)):
	if(texto[i].startswith("1") == True):
		texto_v1.append(texto[i])




for i in range(len(texto_v1)):
	if(texto_v1[i].endswith("\nHost")==True):
		texto_v2.append(texto_v1[i].split("\nHost"))
		
for i in range(len(texto_v2)):
	if(len(texto_v2[i][0]) > 2 ):
		texto_v3.append(texto_v2[i][0])


print(texto_v3)
	
