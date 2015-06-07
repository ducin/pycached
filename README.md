# PyCached

PyCached is a simple key-value storage based on python/[twisted](http://twistedmatrix.com/) library.

## Commands

Following commands are provided:

| Command       | Arguments     | Description  |
| ------------- |:-------------:| ------------:|
| version | - | returns pycached server version |
| count | - | returns number of cache entries |
| clear | - | removes all cache entries |
| items | - | returns all cache entries |
| status | - | returns pycached server status (uptime) |
| get | key | returns cache entry for a given key |
| set | key, value | sets/overwrites cache entry for a given key with a given value |
| delete | key | deletes cache entry for a given key |

## Clients

PyCached serves following clients:
 * python
 * PHP
 * JavaScript (must run http server)

## Interactive console client

You may play with PyCached using interactive console client tool (just like you
do with python interactive shell). Simply start the service and then start the
client:

    export PYTHONPATH="$PYTHONPATH:`pwd`/client/python"
    ./run-service 8081
    ./run-client localhost 8081

Then the python shell shall open with the `client` object ready to be used:

    Python 2.7.2+ (default, Jul 20 2012, 22:12:53)
    [GCC 4.6.1] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> client
    <client.PyCachedClient object at 0xb72ae34c>
    >>> client.version()
    u'1.2'

## HTTP Access

### work in progress

PyCached is bundled with an HTTP server that connects to the main service. This
enables browser clients to send requests to the cache indirectly.

## Tests & Continuous Integration

PyCached is continuously integrated with travis:

[![Build Status](https://travis-ci.org/ducin/pycached.png?branch=master)](https://travis-ci.org/ducin/pycached)

Automated test execution perform following steps:

 * set environment variables (pycached host and port)
 * run the server
 * run tests (all tests rely on the same server process)
 * kill the server process
