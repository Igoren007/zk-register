from kazoo.client import KazooClient
import socket
import time
import signal
from requests import get
import docker

ZK1_HOST = '176.57.212.153:2181'


def reg_in_zk(host, container_list):
    zk = KazooClient(hosts=ZK1_HOST)
    zk.start()
    for container in container_list:
        container_info = f"name:{container.name},id:{container.id}"
        print(container.name)
        zk.ensure_path(f"/nodes/{host}")
        if not zk.exists(f"/nodes/{host}/{container.name}"):
            zk.create(f"/nodes/{host}/{container.name}", bytes(container_info, 'utf-8'))
            print(f"....creating... {container.name}....")
    container_count_in_zk = zk.get_children(f"/nodes/{host}")
    zk.stop()


def check_containers_in_zk(host, containers_on_host):
    zk = KazooClient(hosts=ZK1_HOST)
    zk.start()
    diff = []
    if zk.exists(f"/nodes/{host}"):

        #надо проверять список
        containers_in_zk = zk.get_children(f"/nodes/{host}")
        print(f"Контейнеры на хосте: {[n.name for n in containers_on_host]}")
        print(f"Контейнеры в zk: {containers_in_zk}")
        for item in containers_in_zk:
            if item not in [n.name for n in containers_on_host]:
                #нужно удалить
                print(f"в zk нужно удалить {item}.... удаляем")
                zk.delete(f"/nodes/{host}/{item}")

        for container in containers_on_host:
            print(container.name)
            if container.name not in containers_in_zk:
                print(f"{container.name} нет в zk, добавлю в список для регистрации")
                diff.append(container)
        reg_in_zk(host, diff)
    else:
        #вносим контейнеры
        reg_in_zk(host, containers_on_host)
    zk.stop()


def delete_from_zk(host, container_list):
    zk = KazooClient(hosts=ZK1_HOST)
    zk.start()


if __name__ == "__main__":
    hostname = socket.gethostname()
    #ip_addr = socket.gethostbyname(hostname)
    ip = get('https://api.ipify.org').content.decode('utf8')
    host_info = f"name:{hostname},ip:{ip}"

    while True:
        print("\n----------------------------------------------\n")
        container_list = docker.from_env().containers.list()
        check_containers_in_zk(hostname, container_list)
        time.sleep(15)
