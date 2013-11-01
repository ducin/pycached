from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

from client import PyCachedClient

host, port = 'localhost', 12345

class PyCachedCommand(Resource):
    isLeaf = True
    def render_GET(self, request):
        client = PyCachedClient()
        try:
            client.connect(host, port)
            status = client.status()
            client.close()
            return "PyCached is up since %0.2f seconds" % (status['uptime'],)
        except:
            return "PyCached is down."

    def render_POST(self, request):
        client = PyCachedClient()
        client.connect(host, port)
        kwargs = {k: v[0] for k,v in request.args.iteritems()}
        print kwargs
        command_name = kwargs.pop('command')
        print command_name
        command = getattr(client, command_name)
        print command
        request.setHeader('Content-Type', 'text/html')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', '*')
        request.setHeader('Access-Control-Allow-Headers', '*')
        request.setHeader('Access-Control-Max-Age', 3600)
        return str(command(**kwargs))

factory = Site(PyCachedCommand())
reactor.listenTCP(8000, factory)
reactor.run()