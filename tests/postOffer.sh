#!/bin/bash

offerId=$1
title=$2
tag1=$3
tag2=$4
tag3=$5
tag4=$6
tag5=$7

curl --header "Content-Type: application/json"   --request POST   \
--data '{"id": '$offerId',"title":"'$title'", "created": 312313131, "added_by": 34, "tags": ["'$tag1'", "'$tag2'", "'$tag3'", "'$tag4'", "'$tag5'"]}'   \
"http://127.0.0.1/postOffer/"

offerPath='../mockDb/offer'$offerId'.txt'

cat $offerPath
echo ''
