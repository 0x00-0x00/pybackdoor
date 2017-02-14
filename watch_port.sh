#!/bin/bash

if [[ $1 == "" ]]; then
    echo "Usage: $0 <PORT>";
    exit;
fi


function connect_to_port
{
    nc -zv localhost $1 > /dev/null 2>&1;
    if [[ $? -eq 0 ]]; then
        echo "[+] Port $1 is open.";
        return 0
    else
        echo "[+] Port $1 is closed.";
        exit;
    fi
}

connect_to_port $1
while [[ $? != 0 ]];
do
    connect_to_port $1
done

