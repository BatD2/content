#!/usr/bin/env bash

echo "start instance test"

SECRET_CONF_PATH=$(cat secret_conf_path)

<<<<<<< HEAD
USERNAME=$(cat $SECRET_CONF_PATH | jq '.username')
PASSWORD=$(cat $SECRET_CONF_PATH | jq '.userPassword')
=======
USERNAME="admin"
PASSWORD=$(cat $SECRET_CONF_PATH | jq '.adminPassword')
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07

# remove quotes from password
temp="${PASSWORD%\"}"
temp="${temp#\"}"
PASSWORD=$temp

<<<<<<< HEAD
# remove quotes from username
temp="${USERNAME%\"}"
temp="${temp#\"}"
USERNAME=$temp

[ -n "${INSTANCE_TESTS}" ] && IS_INSTANCE_TESTS=true || IS_INSTANCE_TESTS=false

python3 ./Tests/instance_notifier.py -t $IS_INSTANCE_TESTS -s "$SLACK_TOKEN" -e "$SECRET_CONF_PATH" -u "$USERNAME" -p "$PASSWORD" -b "$CIRCLE_BUILD_URL" -n "$CIRCLE_BUILD_NUM"

echo "Finished slack notifier execution"
=======
[ -n "${NIGHTLY}" ] && IS_NIGHTLY=true || IS_NIGHTLY=false

SERVER_IP=$(cat public_ip)
SERVER_URL="https://$SERVER_IP"

python ./Tests/instance_notifier.py -n $IS_NIGHTLY -s "$SLACK_TOKEN" -e "$SECRET_CONF_PATH" -u "$USERNAME" -p "$PASSWORD" -c "$SERVER_URL"

echo "Finished slack notifier execution"
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
