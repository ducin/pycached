<?php

namespace PyCached;

class PyCachedClient {
    private $buffer_size = 2048;

    public function __construct() {
        $this->_socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        if ($this->_socket === false)
            throw new \Exception(socket_strerror(socket_last_error()));
    }

    public function connect($host, $port) {
        $result = socket_connect($this->_socket, $host, $port);
    }

    public function close() {
        socket_close($this->_socket);
    }

    private function write($message) {
        socket_write($this->_socket, $message, strlen($message));
    }
    
    private function read() {
        return socket_read($this->_socket, $this->buffer_size);
    }

    protected function execute($request) {
        $message = json_encode($request);
        $this->write($message);
        $response = json_decode($this->read(), true);
        if ($response['status'] != 'ok')
            throw new \Exception('Something went wrong with PyCached.');
        return isset($response['value']) ? $response['value'] : NULL;
    }

    public function version() {
        $request = array('command' => 'version');
        return $this->execute($request);
    }

    public function count() {
        $request = array('command' => 'count');
        return $this->execute($request);
    }

    public function set($key, $value) {
        $request = array('command' => 'set', 'key' => $key, 'value' => $value);
        return $this->execute($request);
    }

    public function get($key) {
        $request = array('command' => 'get', 'key' => $key);
        return $this->execute($request);
    }

    public function delete($key) {
        $request = array('command' => 'delete', 'key' => $key);
        return $this->execute($request);
    }

}



