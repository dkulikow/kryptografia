#!/bin/bash

FILE="$1"
KEY_STORE="$2"
CIPHER="$3"

function key_gen {
    openssl enc -"$CIPHER" -k "$FILE" -P -md sha1 | sed '2q;d' | cut -b 5-
}

function store_key_in_keystore {
    KEY="$1"
    decrypted_key_store=$(openssl enc -d -aes-256-cbc -in $KEY_STORE -k $PASSWORD)
    my_alias="KEY[$FILE]=$KEY"
    if [[ $decrypted_key_store = *"KEY[$FILE]"* ]]
    then
        echo "$decrypted_key_store" | sed s/"KEY\[$FILE\]".*/$my_alias/| openssl enc -aes-256-cbc -k $PASSWORD -out $KEY_STORE
    else
        echo -e "$decrypted_key_store\n$my_alias" | openssl enc -aes-256-cbc -k $PASSWORD -out $KEY_STORE
    fi
}

function encrypt_file {
    echo "Password: "
    read -s PASSWORD
    KEY=$(key_gen)
    openssl enc -$CIPHER -K $KEY -in $FILE -out $FILE.enc -iv aaa 
    store_key_in_keystore $KEY
}

encrypt_file

