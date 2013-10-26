import unittest
from time import time
import string, random
from client import PyCachedClient

class MainTest (unittest.TestCase):
    def setUp(self):
        self.client = PyCachedClient()
        self.client.connect('localhost', 12345)
        self.client.clear()

    def tearDown(self):
        self.client.close()

    def random_hash(self, length):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(length))

    def assertCacheCount(self, expected):
        count = self.client.count()
        self.assertEqual(expected, count)

    def test_version(self):
        version = self.client.version()
        self.assertTrue(type(version) is unicode)

    def test_empty(self):
        self.assertCacheCount(0)

    def test_clear(self):
        elements = 10
        for i in range(elements):
            self.client.set(self.random_hash(32), i)
        self.assertCacheCount(elements)

    def test_simple_sequence(self):
        self.assertCacheCount(0)

        self.client.set('john', 'doe')
        self.assertCacheCount(1)

        response = self.client.get('john')
        self.assertEqual('doe', response)

        self.client.set('john', 'lennon')
        self.assertCacheCount(1)

        response = self.client.get('john')
        self.assertEqual('lennon', response)

        self.client.delete('john')
        self.assertCacheCount(0)

    def test_nested(self):
        value = range(1, 10)
        self.client.set('nested', value)

        response = self.client.get('nested')
        self.assertEqual(value, response)
