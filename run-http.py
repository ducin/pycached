#!/usr/bin/python
import argparse

from twisted.internet import reactor
from twisted.web.server import Site

from server.http import PyCachedCommand

parser = argparse.ArgumentParser(description='Run PyCached http access.')
parser.add_argument('port', metavar='port', type=int,
    help='PyCached http access port')
args = parser.parse_args()

print "Starting PyCached http access on port %d" % (args.port)
factory = Site(PyCachedCommand())
reactor.listenTCP(args.port, factory)
reactor.run()
