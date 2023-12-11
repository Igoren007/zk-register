from kazoo.client import KazooClient
import json
import http.server

class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json_string_zk().encode())


def get_hosts_from_zk():

    zk_hosts = []
    zk = KazooClient(hosts='176.57.212.153:2181')
    zk.start()
    children = zk.get_children("/nodes")
#    print(children)
    for i in children:
        data, _ = zk.get(f'/nodes/{i}')
        host = data.decode('utf-8')
        zk_hosts.append(host)
    zk.stop()
    return zk_hosts


def list2dict(lst):
    out = []
    for host in lst:
        ip = host.split(',')[1].split(':')[1]
        dct = {}
        host = []
        host.append(f"{ip}:9100")
#        dct['target'] = f"{ip}:9100"
        dct['target'] = host
        out.append(dct)
    return out


def json_string_zk():
    hosts = list2dict(get_hosts_from_zk())
    json_nodes = json.dumps(hosts)
    return json_nodes

if __name__ == "__main__":

#    print(get_hosts_from_zk())
#    hosts = list2dict(get_hosts_from_zk())
#    print(hosts)
#    f = json.dumps(hosts)
#    print(type(f))
    server_address = ('', 8888)
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    httpd.serve_forever()