<?php

namespace PyCached;

/**
 * PyCached PHP Client class. Connects to pycached service on given host,port
 * and manipulates cache data.
 *
 * @author Tomasz Ducin <tomasz.ducin@gmail.com>
 * @version 1.2
 */
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

    protected function execute($command, $options = array()) {
        $request = array_merge(array('command' => $command), $options);
        $message = json_encode($request);
        $this->write($message);
        $response = json_decode($this->read(), true);
        if ($response['status'] != 'ok')
            throw new \Exception('Something went wrong with PyCached.');
        return isset($response['value']) ? $response['value'] : NULL;
    }

    public function version() {
        return $this->execute('version');
    }

    public function count() {
        return $this->execute('count');
    }

    public function clear() {
        return $this->execute('clear');
    }

    public function items() {
        return $this->execute('items');
    }

    public function status() {
        return $this->execute('status');
    }

    public function set($key, $value) {
        $options = array('key' => $key, 'value' => $value);
        return $this->execute('set', $options);
    }

    public function get($key) {
        $options = array('key' => $key);
        return $this->execute('get', $options);
    }

    public function delete($key) {
        $options = array('key' => $key);
        return $this->execute('delete', $options);
    }

}



