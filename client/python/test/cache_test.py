import unittest
from client import PyCachedClient

class MainTest (unittest.TestCase):
    def setUp(self):
        self.client = PyCachedClient('localhost', 12345)

    def tearDown(self):
        self.client.close()

    def test_version(self):
        version = self.client.version()
        self.assertTrue(type(version) is unicode)

    def test_empty(self):
        count = self.client.count()
        self.assertEqual(count, 0)

    def test_nested(self):
        value = range(1, 10)
        self.client.set('nested', value)

        response = self.client.get('nested')
        self.assertEqual(value, response)

        self.client.delete('nested')
