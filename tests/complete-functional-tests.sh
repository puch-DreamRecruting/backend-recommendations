#!/bin/bash

id=1
tags='colonial,gunner,fulltime'
echo 'adding user: id='$id', tags='$tags
./postUser.sh $id $tags
echo ''

id=1
tags='fulltime,gunner,colonial,experienced'
title='Fulltime-colonial-gunner'
echo 'adding offer: id='$id', tags='$tags
./postOffer.sh $id $tags $title
echo ''

# id=1
# echo 'getting recommendations for id='$id
# ./getRecommendations.sh $id
# echo ''
