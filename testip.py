from kazoo.client import KazooClient
import socket
import time
import signal
from requests import get
import subprocess


SIGNAL_STATUS = True
hostname = socket.gethostname()

addresses = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).stdout
#print(type(rez.stdout))

host_info = ''
#addresses = ''
#ip_list = ['1.1.1.1', '2.2.2.2', '3.3.3.3']
#for ip in ip_list:
#    addresses += f"{ip}-"

host_info += f"name:{hostname},ip:{addresses}"

#print(host_info)

a = host_info.split(',')[1].split(':')[1].split(' ')[0:-1]
#print(a)

b = []
dct = {}

for i in a:
    b.append(f"{i}:8080")
dct["targets"] = b
print(dct)