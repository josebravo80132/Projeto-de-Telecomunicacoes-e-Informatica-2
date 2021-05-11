import time
import socket
import sys
import os
import argparse




#sudo /etc/init.d/snmpd start


#snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.20.1.1 


program = '''

x = {}

output = os.popen('/etc/init.d/snmpd start').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.20.1.1 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.20.1.2 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.22.1.3 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.4.3 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.1.3 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.1.5 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.2.2.1.8 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.2.2.1.2 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.5.1 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.5.14 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.7.1').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.7.4 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.1.5 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.25.1.6 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.25.5.1.1.1 ').read()
print(output)

output = os.popen('snmpwalk -v 2c localhost -c gr2020 .1.3.6.1.2.1.25.5.1.1.2 ').read()
print(output)

'''

loc = {}

exec(program, globals(), loc)

