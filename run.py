#!/usr/bin/python
import sys, errno
from server.server import CacheFactory
from twisted.internet import reactor

if len(sys.argv) != 2:
    print "Usage: ./run.py <port>\n"
    sys.exit(errno.EINVAL)

reactor.listenTCP(int(sys.argv[1]), CacheFactory())
reactor.run()
