import socket
import json

__author__ = "Tomasz Ducin"
__email__ = "tomasz.ducin@gmail.com"
__license__ = "MIT"
__version__ = "0.1.2"

class PyCachedClient(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        try:
            self.s.connect((host, port))
        except socket.error:
            raise RuntimeError('Something went wrong with PyCached.')

    def close(self):
        self.s.close()

    def _receive(self):
        received = self.s.recv(1024)
        decoded = json.loads(received.rstrip('\n'))
        return decoded['value'] if 'value' in decoded else None

    def _send(self, command, options={}):
        request = {'command': command}
        request.update(options)
        self.s.sendall(json.dumps(request))

    def version(self):
        self._send('version')
        return self._receive()

    def count(self):
        self._send('count')
        return self._receive()

    def clear(self):
        self._send('clear')
        return self._receive()

    def items(self):
        self._send('items')
        return self._receive()

    def status(self):
        self._send('status')
        return self._receive()

    def get(self, key):
        self._send('get', {'key':key})
        return self._receive()

    def set(self, key, value):
        self._send('set', {'key':key, 'value':value})
        return self._receive()

    def delete(self, key):
        self._send('delete', {'key':key})
        return self._receive()
