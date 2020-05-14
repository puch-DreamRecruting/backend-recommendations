#!/bin/bash

echo 'adding user'
./postUser.sh 1 colonial gunner fulltime viper galactica
echo ''

echo 'adding offer: id='$id', tags='$tags
./postOffer.sh 2 looking-for-gunner fulltime colonial experienced gunner raptor
echo ''

id=1
echo 'getting recommendations for id='$id
./getRecommendations.sh $id
echo ''
