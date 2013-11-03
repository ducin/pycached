#!/usr/bin/python
import argparse
import os

from twisted.internet import reactor

parser = argparse.ArgumentParser(description='Run PyCached server.')
parser.add_argument('port', metavar='port', type=int,
    help='PyCached service port')
parser.add_argument('--http-port', metavar='http-port', type=int, default=None,
    help='PyCached http access port')
args = parser.parse_args()

def dumpPid(name):
    f = open(name + '.pid', 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()

def erasePid(name):
    os.remove(name + '.pid')

def run(name, port, factory):
    dumpPid(name)
    print "Starting PyCached %s on port %d" % (name, port)
    reactor.listenTCP(port, factory)
    reactor.run()
    erasePid(name)
    print "Successfully stopped PyCached %s" % (name,)

# start service (required)
fork_pid = os.fork()
if fork_pid == 0:
    from server.service import PyCachedFactory
    run('service', args.port, PyCachedFactory())
else:
    # start http access (optional)
    if args.http_port:
        fork_pid = os.fork()
        if fork_pid == 0:
            from server.http import PyCachedSite
            addr = ('localhost', args.port)
            run('http', args.http_port, PyCachedSite(addr))
        else:
            pass
