__author__ = "Tomasz Ducin"
__email__ = "tomasz.ducin@gmail.com"
__license__ = "MIT"
__version__ = "0.1.2"

from twisted.web.resource import Resource
from twisted.python import log
from twisted.web.server import Site
from client import PyCachedClient

class PyCachedCommand(Resource):
    isLeaf = True

    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Max-Age': 3600
    }

    def getServiceClient(self):
        client = PyCachedClient()
        client.connect(*self.service_address)
        return client

    def render_GET(self, request):
        '''
        Renders service status as plain text.
        '''
        log.msg('GET')
        request.setHeader('Content-Type', 'text/plain')
        try:
            client = self.getServiceClient()
            status = client.status()
            client.close()
            return "PyCached is up since %0.2f seconds" % (status['uptime'],)
        except:
            return "PyCached is down."

    def render_POST(self, request):
        '''
        Executes pycached request ad returns the response.
        '''
        log.msg('POST %s' % (str(request.args)))
        client = self.getServiceClient()
        kwargs = {k: v[0] for k,v in request.args.iteritems()}
        command_name = kwargs.pop('command')
        command = getattr(client, command_name)
        result = str(command(**kwargs))
        client.close()
        request.setHeader('Content-Type', 'text/plain')
        for header, value in PyCachedCommand.cors_headers.iteritems():
            request.setHeader(header, value)
        return result

class PyCachedSite(Site):
    '''
    Performs all operations for PyCached HTTP access.
    '''
    def __init__(self, service_address, **kwargs):
        '''
        This class uses predefined Resource type (which cannot be changed).
        Instead of Resource typ, the constructor accepts PyCached service
        address, which is a (host, port) 2-tuple. This address is available
        to all resources (as they conect to PyCached service each time).
        '''
        resource = PyCachedCommand()
        resource.service_address = service_address
        Site.__init__(self, resource, **kwargs)
