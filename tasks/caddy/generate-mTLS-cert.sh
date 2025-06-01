#!/bin/bash

mkdir -p certs

echo Generating CA certificates
openssl genrsa -out certs/client-ca.key 4096
openssl req -new -x509 -nodes -days 3600 -key certs/client-ca.key -out certs/client-ca.crt

echo Generating a certificate signing request
openssl req -newkey rsa:4096 -nodes -keyout certs/client.key -out certs/client.req

echo Have the CA sign the certificate requests and output the certificates.
openssl x509 -req -in certs/client.req -days 3600 -CA certs/client-ca.crt -CAkey certs/client-ca.key -set_serial 01 -out certs/client.crt

echo
echo "Please enter a STRONG password. Many clients *require* a password for you to be able to import the certificate, and you want to protect it."
echo 

echo "Converting the cerificate to PKCS12 format (for import into browser)"
openssl pkcs12 -export -out certs/client.pfx -inkey certs/client.key -in certs/client.crt

echo Cleaning up
rm certs/client.req
