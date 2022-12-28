#!/bin/bash
function usage {
  echo ""
  echo "Auth test"
  echo "${0} <token>"
  echo ""
  exit 1
}

if [ $# -ne 1 ]; then
  usage
fi

token=$1

curl -X 'GET' -H "Authorization: Bearer ${token}" \
  'http://localhost:8080/oauth2/tokeninfo' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
