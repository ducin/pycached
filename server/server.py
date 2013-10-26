__author__ = "Tomasz Ducin"
__email__ = "tomasz.ducin@gmail.com"
__license__ = "MIT"
__version__ = "1.1"

import json
from time import mktime
from datetime import datetime
from twisted.internet import protocol

class CacheEncoder(json.JSONEncoder):
    def datetime_to_string(self, d):
        return str(d)
    def datetime_to_timestamp(self, d):
        return int(mktime(d.timetuple()))
    def default(self, o):
        if isinstance(o, datetime):
            return self.datetime_to_timestamp(o)
        return json.JSONEncoder.default(self, o)

def status(fun):
    def execute(self, **kwargs):
        result = {'status': 'ok'}
        raw = fun(self, **kwargs)
        if raw != None:
            result['value'] = raw
        return json.dumps(result, cls=CacheEncoder)
    return execute

class Cache(protocol.Protocol):
    def __init__(self, factory, verbose):
        self.factory = factory
        self.verbose = verbose
    def dataReceived(self, data):
        if self.verbose:
            print 'received: %s' % (data,)
        request = json.loads(data)
        if self.verbose:
            print 'request: %s' % (request,)
        command = "handle_%s" % (request.pop('command'),)
        if self.verbose:
            print 'command: %s\n' % (command,)
        result = getattr(self.factory, command)(**request)
        self.transport.write(result + "\n")

class CacheFactory(protocol.Factory):
    def __init__(self, verbose=False):
        self.clear()
        self.start_time = datetime.now()
        self.verbose = False

    def clear(self):
        '''
        Clears entire cache.
        '''
        self.data = {}

    def buildProtocol(self, addr):
        '''
        Returns instance of PyCached protocol.
        '''
        return Cache(self, self.verbose)

    def setVerbosity(self, verbose):
        '''
        Sets verbosity. It will be passed to each cache protocol instance.
        '''
        self.verbose = verbose

    @status
    def handle_version(self):
        return __version__

    @status
    def handle_count(self):
        return len(self.data)

    @status
    def handle_clear(self):
        self.clear()
        return

    @status
    def handle_items(self):
        return self.data

    @status
    def handle_status(self):
        return {'uptime': (datetime.now() - self.start_time).total_seconds()}

    @status
    def handle_get(self, key):
        item = self.data[key]
        item[2] += 1
        return item[0]

    @status
    def handle_set(self, key, value):
        self.data[key] = [value, datetime.now(), 0]
        return

    @status
    def handle_delete(self, key):
        self.data.pop(key)
        return
