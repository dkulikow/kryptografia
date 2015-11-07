#!/bin/bash

FILE="$1"
KEY_STORE="$2"
CIPHER="$3"
PASSWORD="$4"

function get_key {
    PASSWORD=$1
    openssl enc -d -aes-256-cbc -in $KEY_STORE -k $PASSWORD | grep $FILE | cut -d= -f2
}

function decrypt_file {
    PASSWORD=$1
    KEY=$(get_key $PASSWORD)
    openssl enc -d  -iv "aaa" -$CIPHER -in $FILE.enc -K "$KEY" 
}

decrypt_file $PASSWORD