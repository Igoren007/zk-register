from kazoo.client import KazooClient
import socket
import time


hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)
host_info = f"name:{hostname}, ip:{ip_addr}"

zk = KazooClient(hosts='176.57.212.153:2181')
zk.start()

if zk.exists("/nodes"):
    zk.create(f"/nodes/{hostname}", bytes(host_info, 'utf-8'))
    print("done")
else:
    zk.create("/nodes")
    zk.create(f"/nodes/{hostname}", bytes(host_info, 'utf-8'))
    print("done")

while True:
    time.sleep(1)