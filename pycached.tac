# this file is a stub, it doesn't work as expected

from twisted.application import internet, service
from server.service import PyCachedFactory
from server.http import PyCachedSite

application = service.Application('pycached')
# pycached core service
pycachedService = internet.TCPServer(8001, PyCachedFactory())
pycachedService.setServiceParent(application)
# pycached http access
addr = ('localhost', 8001)
pycachedHttp = internet.TCPServer(8002, PyCachedSite(addr))
pycachedHttp.setServiceParent(application)
