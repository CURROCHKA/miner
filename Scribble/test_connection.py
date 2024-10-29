import socket
import json


class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        self.port = 5555
        self.address = (self.server, self.port)
        self.name = name
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.address)
            self.client.sendall(self.name.encode())
            return json.loads(self.client.recv(2048))
        except Exception as e:
            self.disconnect(str(e))

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())

            d = ''
            while True:
                last = self.client.recv(1024).decode()
                d += last
                try:
                    if d.count('}') == d.count('{'):
                        break
                except:
                    break

            keys = [str(key) for key in data.keys()]
            return json.loads(d)[keys[0]]
        except socket.error as e:
            self.disconnect(e)

    def disconnect(self, msg: str):
        print(f'[EXCEPTION] Disconnected from server: {msg}')
        self.client.close()


n = Network('Ivan')
print(n.send({3: []}))
