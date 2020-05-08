<?php

if(!empty($_POST)) {
    $message = $_POST['message'];
    $redis = new Redis();
    $redis->pconnect('REDIS_HOST'); // REDIS_HOST hast to be the same as in BBB_REDIS_HOST
    $redis->publish('REDIS_CHANNEL', $message); // REDIS_CHANNEL hast to be the same as in BBB_REDIS_CHANNEL
    echo "Message published\n";