#!/bin/bash
function usage {
  echo ""
  echo "Post status message"
  echo "${0} <token>"
  echo ""
  exit 1
}

if [ $# -ne 1 ]; then
  usage
fi

token=$1

curl -X 'POST' -H "Authorization: Bearer ${token}" \
  'http://localhost:8080/api/v1/status' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "The new gold image for Fedora 56 is now available",
  "message_type": "important"
}'
