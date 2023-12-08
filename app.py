from kazoo.client import KazooClient


if __name__ == "__main__":

    zk = KazooClient(hosts='127.0.0.1:2181')
    zk.start()

#    zk.ensure_path("/nodes")
    children = zk.get_children("/nodes")
    print(children)

    data = zk.get("/nodes/node-1")
    print(data[0])


#    zk.create("/nodes/host-4", b"name=host-4")

#    children = zk.get_children("/nodes")
#    print(children)

#    data = zk.get("/nodes/host-1")
#    print(data[0])

#    zk.delete("/nodes/host-1")
