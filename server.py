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

def status(fun):
    def execute(self, **kwargs):
        print '%s called' % (fun.__name__,)
        result = {'status': 'ok'}
        raw = fun(self, **kwargs)
        if raw != None:
            result['value'] = raw
        return json.dumps(result)
    return execute

class CacheFactory(protocol.Factory):
    version = '1.0-alpha'

    def __init__(self):
        self.data = {}

    def buildProtocol(self, addr):
        return Cache(self)

    @status
    def handle_version(self):
        return CacheFactory.version

    @status
    def handle_get(self, key):
        return self.data[key]

    @status
    def handle_set(self, key, value):
        self.data[key] = value
        return

    @status
    def handle_delete(self, key):
        self.data.pop(key)
        return

    @status
    def handle_count(self):
        return len(self.data)

reactor.listenTCP(int(sys.argv[1]), CacheFactory())
reactor.run()
