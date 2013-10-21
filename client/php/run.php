#!/usr/bin/php
<?php

require __DIR__ . '/PyCachedClient.php';

use \PyCached\PyCachedClient;

function display($result) {
    var_export($result);
    echo "\n";
}

$client = new PyCachedClient;
$client->connect('localhost', 12345);

display($client->version());

display($client->count());

display($client->set('john', 'doe'));

display($client->count());

display($client->set('john', 'lennon'));

display($client->count());

display($client->get('john'));

display($client->delete('john'));

display($client->count());

$client->close();
