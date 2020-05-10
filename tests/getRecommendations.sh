userId=$1

curl -X GET "http://127.0.0.1/getRecommendations/$userId" -H  "accept: application/json"
