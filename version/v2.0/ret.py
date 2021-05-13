import time
import socket
import sys
import os
import argparse




#sudo /etc/init.d/snmpd start


#snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.20.1.1 


program = '''

x = {}
y = {} 
z = {} 
w = {}
t = {}
u = {}

output = os.popen('/etc/init.d/snmpd start').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.20.1.1 ').read()
print(output)

x = output.split(" ")

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.22.1.3 ').read()
print(output)

y = output.split(" ")

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.1.3 ').read()
print(output)

z = output.split(" ")

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.1.5 ').read()
print(output)

w = output.split(" ")

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.7.1 ').read()
print(output)

t = output.split(" ")

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.7.4 ').read()
print(output)

u = output.split(" ")


'''

loc = {}

exec(program, globals(), loc)

texto = []
texto.extend(loc['x'])

texto_v1 = []
texto_v2 = []
texto_v3 = []
texto_final_1 = []
texto_final_2 = []
texto_final_3 = []
texto_final_4 = []
texto_final_5 = []
texto_final_6 = []
texto_final_7 = []

for i in range(len(texto)):
	if(texto[i].startswith("I") == False):
		texto_v1.append(texto[i])
		
for i in range(len(texto_v1)):
	if(texto_v1[i].endswith("=")==False):
		texto_v2.append(texto_v1[i])
		
for i in range(len(texto_v2)):
	if "\nIP-MIB::ipAdEntAddr." in texto_v2[i]:
		texto_v3.append(texto_v2[i].split("\nIP-MIB::ipAdEntAddr."))


for i in range(len(texto_v3)):
	if(len(texto_v3[i][0]) > 2 ):
		texto_final_1.append(texto_v3[i][0])
		
#hwewebfubweubfuwebfwebfuiwebfiubweifiu

texto.clear()
texto_v1.clear()
texto_v2.clear()
texto_v3.clear()
texto.extend(loc['y'])

for i in range(len(texto)):
	if(texto[i].startswith("I") == False):
		texto_v1.append(texto[i])
			
for i in range(len(texto_v1)):
	if(texto_v1[i].endswith("=")==False):
		texto_v2.append(texto_v1[i])
		
for i in range(len(texto_v2)):
	if "\nIP-MIB::ipNetToMediaNetAddress." in texto_v2[i]:
		texto_v3.append(texto_v2[i].split("\nIP-MIB::ipNetToMediaNetAddress."))

for i in range(len(texto_v3)):
	for j in range(len(texto_v3[i])):
		if(len(texto_v3[i][j]) > 0 ):
			texto_final_2.append(texto_v3[i][j])

#hwewebfubweubfuwebfwebfuiwebfiubweifiu

texto.clear()
texto_v1.clear()
texto_v2.clear()
texto_v3.clear()
texto.extend(loc['z'])

for i in range(len(texto)):
	if(texto[i].startswith("I") == False):
		texto_v1.append(texto[i])
			
for i in range(len(texto_v1)):
	if(texto_v1[i].endswith("\n")== True):
		texto_v2.append(texto_v1[i])

for i in range(len(texto_v2)):
	if "\n" in texto_v2[i]:
		texto_v3.append(texto_v2[i].split("\n"))

for i in range(len(texto_v3)):
	for j in range(len(texto_v3[i])):
		if(len(texto_v3[i][j]) > 0 ):
			texto_final_3.append(texto_v3[i][j])
			
#hwewebfubweubfuwebfwebfuiwebfiubweifiu

texto.clear()
texto_v1.clear()
texto_v2.clear()
texto_v3.clear()
texto.extend(loc['w'])

for i in range(len(texto)):
	if(texto[i].startswith("I") == False):
		texto_v1.append(texto[i])
			
for i in range(len(texto_v1)):
	if(texto_v1[i].endswith("\n")== True):
		texto_v2.append(texto_v1[i])

for i in range(len(texto_v2)):
	if "\n" in texto_v2[i]:
		texto_v3.append(texto_v2[i].split("\n"))

for i in range(len(texto_v3)):
	for j in range(len(texto_v3[i])):
		if(len(texto_v3[i][j]) > 0 ):
			texto_final_4.append(texto_v3[i][j])

#hwewebfubweubfuwebfwebfuiwebfiubweifiu

texto.clear()
texto_v1.clear()
texto_v2.clear()
texto_v3.clear()
texto.extend(loc['t'])

for i in range(len(texto)):
	if(texto[i].startswith("I") == False):
		texto_v1.append(texto[i])
			
for i in range(len(texto_v1)):
	if(texto_v1[i].endswith("\n")== True):
		texto_v2.append(texto_v1[i])

for i in range(len(texto_v2)):
	if "\n" in texto_v2[i]:
		texto_v3.append(texto_v2[i].split("\n"))

for i in range(len(texto_v3)):
	for j in range(len(texto_v3[i])):
		if(len(texto_v3[i][j]) > 0 ):
			texto_final_5.append(texto_v3[i][j])



#hwewebfubweubfuwebfwebfuiwebfiubweifiu

texto.clear()
texto_v1.clear()
texto_v2.clear()
texto_v3.clear()
texto.extend(loc['u'])

for i in range(len(texto)):
	if(texto[i].startswith("I") == False):
		texto_v1.append(texto[i])
			
for i in range(len(texto_v1)):
	if(texto_v1[i].endswith("\n")== True):
		texto_v2.append(texto_v1[i])

for i in range(len(texto_v2)):
	if "\n" in texto_v2[i]:
		texto_v3.append(texto_v2[i].split("\n"))

for i in range(len(texto_v3)):
	for j in range(len(texto_v3[i])):
		if(len(texto_v3[i][j]) > 0 ):
			texto_final_6.append(texto_v3[i][j])


print(texto_final_1)
print(texto_final_2)
print(texto_final_3)
print(texto_final_4)
print(texto_final_5)
print(texto_final_6)

texto_final_7 = ['interfaces:']
texto_final_7.extend(texto_final_1)
texto_final_7.append(" ip_redeslocal:")
texto_final_7.extend(texto_final_2)
texto_final_7.append(" tempo_act:")
texto_final_7.extend(texto_final_3)
texto_final_7.append(" nome:")
texto_final_7.extend(texto_final_4)
texto_final_7.append(" udp_rec:")
texto_final_7.extend(texto_final_5)
texto_final_7.append(" udp_env:")
texto_final_7.extend(texto_final_6)

str_final = ""  
for i in texto_final_7: 
	str_final += i  


print(str_final)







