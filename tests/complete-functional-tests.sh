#!/bin/bash

id=42
tags='hitchhiker,galaxy'
echo 'adding user: id=$id, tags=$tags'
./postUser.sh $id $tags
echo ''

id=33
tags='fulltime,pilot,cylon'
echo 'adding offer: id=$id, tags=$tags'
./postOffer.sh $id $tags
echo ''

