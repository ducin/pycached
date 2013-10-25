import socket
import json

class PyCachedClient(object):
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
    def _receive(self):
        received = self.s.recv(1024)
        decoded = json.loads(received.rstrip('\n'))
        return decoded['value'] if decoded['value'] else None
    def _send(self, request):
        self.s.sendall(json.dumps(request))
    def version(self):
        self._send({'command':'version'})
        return self._receive()
    def get(self, key):
        self._send({'command':'get', 'key':key})
        return self._receive()
    def set(self, key, value):
        self._send({'command':'set', 'key':key, 'value':value})
        return self._receive()
    def delete(self, key):
        self._send({'command':'delete', 'key':key})
        return self._receive()
    def count(self):
        self._send({'command':'count'})
        return self._receive()
    def close(self):
        self.s.close()
