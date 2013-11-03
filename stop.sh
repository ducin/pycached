#!/bin/bash

function close {
    f="$1.pid"
    if [ -f "$f" ]
    then
        kill -s SIGTERM `cat "$f"`
    fi    
}

close http
close service
