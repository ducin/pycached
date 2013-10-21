#!/usr/bin/python
import sys, errno
import socket
import json

class PycachedClient(object):
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
    def _receive(self):
        received = self.s.recv(1024)
        return json.loads(received.rstrip('\n'))
    def _send(self, request):
        self.s.sendall(json.dumps(request))
    def version(self, key):
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

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: ./client.py <host> <port>\n"
        sys.exit(errno.EINVAL)
    host = sys.argv[1]
    port = int(sys.argv[2])
    pc = PycachedClient(host, port)
