#!/usr/bin/python
import argparse

from twisted.internet import reactor

from server.server import PyCachedFactory

parser = argparse.ArgumentParser(description='Run PyCached server.')
parser.add_argument('port', metavar='port', type=int,
    help='PyCached service port')
parser.add_argument('--http-port', metavar='http-port', type=int, default=None,
    help='PyCached http access port')
args = parser.parse_args()

print "Starting PyCached service on port %d" % (args.port)
reactor.listenTCP(args.port, PyCachedFactory())
reactor.run()
