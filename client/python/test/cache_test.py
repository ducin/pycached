import unittest
from client import PyCachedClient

class MainTest (unittest.TestCase):
    def setUp(self):
        self.client = PyCachedClient('localhost', 12345)
    def tearDown(self):
        self.client.close()
    def test_run(self):
        version = self.client.version()
        self.assertTrue(type(version) is unicode)
