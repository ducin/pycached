#!/usr/bin/python
import argparse
import code, readline, rlcompleter

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
readline.set_completer(rlcompleter.Completer(vars).complete)
readline.parse_and_bind("tab: complete")
shell = code.InteractiveConsole(vars)
shell.interact()
