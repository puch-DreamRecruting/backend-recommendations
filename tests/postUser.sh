#!/bin/bash

userId=$1
tags=$2


curl -X POST "http://127.0.0.1/postUser/$userId/$tags" -H  "accept: application/json"

cat ../data.txt
echo ''
