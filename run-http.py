#!/usr/bin/python
import argparse

from twisted.internet import reactor
from server.http import PyCachedSite

parser = argparse.ArgumentParser(description='Run PyCached http access.')
parser.add_argument('port', metavar='port', type=int,
    help='PyCached http access port')
args = parser.parse_args()

print "Starting PyCached http access on port %d" % (args.port)
addr = ('localhost', 8001)
reactor.listenTCP(args.port, PyCachedSite(addr))
reactor.run()
