<?php

use \PyCached\PyCachedClient;

class CacheTest extends PHPUnit_Framework_TestCase
{
    protected function setUp() {
        $this->client = new PyCachedClient;
        $this->client->connect('localhost', 12345);
        $this->client->clear();
    }

    protected function tearDown() {
        $this->client->close();
    }

    protected function getRandomHash($length) {
        return substr(md5(rand().time()), 0, $length);
    }

    protected function assertCacheCount($expected) {
        $count = $this->client->count();
        $this->assertSame($expected, $count);
    }

    public function testVersion() {
        $response = $this->client->version();
        $this->assertInternalType('string', $response);
    }

    public function testStatus() {
        $status = $this->client->status();
        $this->assertArrayHasKey('uptime', $status);
        $this->assertInternalType('float', $status['uptime']);
    }

    public function testEmpty() {
        $this->assertCacheCount(0);
    }

    public function testClear() {
        $elements = 10;
        foreach(range(0, $elements - 1) as $i)
            $this->client->set($this->getRandomHash(32), $i);
        $this->assertCacheCount($elements);
    }

    public function testSimpleSequence() {
        $this->assertCacheCount(0);

        $this->client->set('john', 'doe');
        $this->assertCacheCount(1);

        $response = $this->client->get('john');
        $this->assertSame('doe', $response);

        $this->client->set('john', 'lennon');
        $this->assertCacheCount(1);

        $response = $this->client->get('john');
        $this->assertSame('lennon', $response);

        $this->client->delete('john');
        $this->assertCacheCount(0);
    }

    public function testNestedStructures() {
        $value = range(1, 10);
        $this->client->set('nested', $value);

        $response = $this->client->get('nested');
        $this->assertSame($response, $value);
    }
}
