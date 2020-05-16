#!/bin/bash

userId=$1
tag1=$2
tag2=$3
tag3=$4
tag4=$5
tag5=$6

curl --header "Content-Type: application/json"   --request POST   \
--data '{"id": '$userId', "tags": ["'$tag1'", "'$tag2'", "'$tag3'", "'$tag4'", "'$tag5'"]}'   \
"http://127.0.0.1/postUser/"

echo ''
