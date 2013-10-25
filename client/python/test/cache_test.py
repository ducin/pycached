import unittest
from client import PyCachedClient

class MainTest (unittest.TestCase):
    def test_run(self):
        client = PyCachedClient('localhost', 12345)
        version = client.version()
        self.assertIsInstance(version, unicode)
        client.close()
