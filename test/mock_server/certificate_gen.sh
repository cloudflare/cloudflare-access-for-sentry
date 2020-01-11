#!/bin/bash
set -e

for i in 1 2
do
    KEY_NAME="cert_0"$i
    ssh-keygen -t rsa -b 4096 -m PEM -P "" -f $KEY_NAME.key
    openssl rsa -in $KEY_NAME.key -pubout -outform PEM -out $KEY_NAME.key.pub
    echo ">>> Generated Certificate $i:"
    cat $KEY_NAME.key
    cat $KEY_NAME.key.pub
done