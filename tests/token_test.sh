#!/bin/bash
function usage {
  echo ""
  echo "Create token and test uauth"
  echo "${0} <scope>"
  echo ""
  exit 1
}

if [ -z "$1" ]; then
    echo "No argument supplied"
fi

pushd ../.
source bin/activate

read_token=$(./token_manage.py create test_read read | awk '{ print $2 }')
admin_token=$(./token_manage.py create test_admin admin | awk '{ print $2 }')

echo $read_token
echo $admin_token

echo 'Test read token:'
curl -X 'GET' -H "Authorization: Bearer ${read_token}" \
  'http://localhost:8080/oauth2/tokeninfo' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'

echo 'Test admin token:'
curl -X 'GET' -H "Authorization: Bearer ${admin_token}" \
  'http://localhost:8080/oauth2/tokeninfo' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'

echo 'Test post message with read token'
curl -X 'POST' -H "Authorization: Bearer ${read_token}" \
  'http://localhost:8080/api/v1/status' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "The new gold image for Fedora 56 is now available",
  "message_type": "important"
}'

echo 'Test post message with admin token'
echo -n "HTTP code: "
curl --write-out %{http_code} -X 'POST' -H "Authorization: Bearer ${admin_token}" \
  'http://localhost:8080/api/v1/status' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "The new gold image for Fedora 56 is now available",
  "message_type": "important"
}'
echo ''


./token_manage.py delete test_read
./token_manage.py delete test_admin
