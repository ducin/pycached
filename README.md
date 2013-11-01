pycached
========

Simple key-value storage based on python/twisted. Following commands are provided:

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

PyCached serves following clients:
 * python
 * PHP
 * JavaScript (must run http server)

PyCached is continuously integrated with travis:

[![Build Status](https://travis-ci.org/tkoomzaaskz/pycached.png?branch=master)](https://travis-ci.org/tkoomzaaskz/pycached)
