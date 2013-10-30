import cherrypy
from client import PyCachedClient

class PyCachedAdmin(object):
    exposed = True

    def GET(self):
        client = PyCachedClient()
        try:
            client.connect('localhost', 12345)
            status = client.status()
            client.close()
            return "PyCached is up since %0.2f seconds" % (status['uptime'],)
        except:
            return "PyCached is down."

    def POST(self, **kwargs):
        client = PyCachedClient()
        try:
            client.connect('localhost', 12345)
            command_name = kwargs.pop('command')
            command = getattr(client, command_name)
            CORS()
            return command(**kwargs)
        except:
            return "Invalid command"

def CORS():
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
    cherrypy.response.headers['Access-Control-Allow-Methods'] = '*'
    cherrypy.response.headers['Access-Control-Allow-Headers'] = '*'
    cherrypy.response.headers['Access-Control-Max-Age'] = 3600

if __name__ == "__main__":
    # solution from http://permalink.gmane.org/gmane.comp.python.cherrypy/7530 doesn't work as expected
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    cherrypy.quickstart(PyCachedAdmin(), config={'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
