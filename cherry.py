import cherrypy
from client import PyCachedClient

class PyCachedAdmin(object):
    def index(self):
        client = PyCachedClient()
        try:
            client.connect('localhost', 12345)
            status = client.status()
            client.close()
            return "PyCached is up since %0.2f seconds" % (status['uptime'],)
        except:
            return "PyCached is down."
    index.exposed = True

cherrypy.quickstart(PyCachedAdmin())
