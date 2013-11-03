__author__ = "Tomasz Ducin"
__email__ = "tomasz.ducin@gmail.com"
__license__ = "MIT"
__version__ = "1.2"

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
        log.msg('GET')
        try:
            client = self.getServiceClient()
            status = client.status()
            client.close()
            return "PyCached is up since %0.2f seconds" % (status['uptime'],)
        except:
            return "PyCached is down."

    def render_POST(self, request):
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
    def __init__(self, service_address):
        resource = PyCachedCommand()
        resource.service_address = service_address
        Site.__init__(self, resource)
