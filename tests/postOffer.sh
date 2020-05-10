#!/bin/bash

offerId=$1
tags=$2
title=$3

curl -X POST "http://127.0.0.1/postOffer/$offerId/$tags/$title" -H  "accept: application/json"

offerPath='../mockDb/offer'$offerId'.txt'

cat $offerPath
echo ''
