<?php

use \PyCached\PyCachedClient;

class CacheTest extends PHPUnit_Framework_TestCase
{
    protected function setUp() {
        $this->client = new PyCachedClient;
        $this->client->connect('localhost', 12345);
    }

    protected function tearDown() {
        $this->client->close();
    }

    public function testVersion()
    {
        $response = $this->client->version();
        $this->assertInternalType('string', $response);
    }

    public function testEmpty()
    {
        $response = $this->client->count();
        $this->assertSame(0, $response);
    }

    public function testSimpleSequence()
    {
        $response = $this->client->count();
        $this->assertSame(0, $response);

        $this->client->set('john', 'doe');
        $response = $this->client->count();
        $this->assertSame(1, $response);

        $response = $this->client->get('john');
        $this->assertSame('doe', $response);

        $this->client->set('john', 'lennon');
        $response = $this->client->count();
        $this->assertSame(1, $response);

        $response = $this->client->get('john');
        $this->assertSame('lennon', $response);

        $this->client->delete('john');
        $response = $this->client->count();
        $this->assertSame(0, $response);
    }
}
