#!/usr/bin/python
import sys, errno
import json
from twisted.internet import protocol, reactor

if len(sys.argv) != 2:
    print "Usage: ./server.py <port>\n"
    sys.exit(errno.EINVAL)

class Cache(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
    def dataReceived(self, data):
        request = json.loads(data)
        command = "handle_%s" % (request.pop('command'),)
        result = getattr(self.factory, command)(**request)
        self.transport.write(result + "\n")

class CacheFactory(protocol.Factory):
    def __init__(self):
        self.data = {}
    def buildProtocol(self, addr):
        return Cache(self)
    def handle_get(self, key):
        return json.dumps(self.data[key])
    def handle_set(self, key, value):
        self.data[key] = value
        return json.dumps({"status":"ok"})
    def handle_delete(self, key):
        self.data.pop(key)
        return json.dumps({"status":"ok"})
    def handle_count(self):
        return json.dumps(len(self.data))

reactor.listenTCP(int(sys.argv[1]), CacheFactory())
reactor.run()
