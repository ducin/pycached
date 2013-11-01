#!/usr/bin/python
import argparse
import code

from client import PyCachedClient

parser = argparse.ArgumentParser(description='Run PyCached server.')
parser.add_argument('host', metavar='host', type=str,
    help='PyCached service host')
parser.add_argument('port', metavar='port', type=int,
    help='PyCached service port')
args = parser.parse_args()

# create client
client = PyCachedClient()
client.connect(args.host, args.port)

# open interactive shell
vars = globals()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()
