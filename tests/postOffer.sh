#!/bin/bash

offerId=$1
tags=$2


curl -X POST "http://127.0.0.1/postOffer/$offerId/$tags" -H  "accept: application/json"

cat ../data.txt
echo ''
