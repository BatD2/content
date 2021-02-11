#!/usr/bin/env bash
<<<<<<< HEAD
set +e

# replace slashes ('/') in the branch name, if exist, with underscores ('_')
UNDERSCORE_CIRCLE_BRANCH=${CIRCLE_BRANCH//\//_}

#download awsinstancetool
echo "Getting conf from branch $UNDERSCORE_CIRCLE_BRANCH (fallback to master)"
=======
set -e

# download configuration file from github repo
echo "Getting conf from branch $CIRCLE_BRANCH (fallback to master)"
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07

SECRET_CONF_PATH="./conf_secret.json"
echo ${SECRET_CONF_PATH} > secret_conf_path

DEMISTO_LIC_PATH="./demisto.lic"
echo ${DEMISTO_LIC_PATH} > demisto_lic_path

<<<<<<< HEAD
DEMISTO_PACK_SIGNATURE_UTIL_PATH="./signDirectory"
echo ${DEMISTO_PACK_SIGNATURE_UTIL_PATH} > demisto_pack_sig_util_path

# download configuration files from github repo
wget --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN" -O ./test_configuration.zip "https://github.com/demisto/content-test-conf/archive/$UNDERSCORE_CIRCLE_BRANCH.zip" --no-check-certificate -q
if [ "$?" != "0" ]; then
    echo "No such branch in content-test-conf: $UNDERSCORE_CIRCLE_BRANCH , falling back to master"
    wget --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN" -O ./test_configuration.zip "https://github.com/demisto/content-test-conf/archive/master.zip" --no-check-certificate -q
    unzip ./test_configuration.zip
    cp -r ./content-test-conf-master/awsinstancetool ./Tests/scripts/awsinstancetool
    cp -r ./content-test-conf-master/demisto.lic $DEMISTO_LIC_PATH
    cp -r ./content-test-conf-master/conf.json $SECRET_CONF_PATH
    cp -r ./content-test-conf-master/signDirectory $DEMISTO_PACK_SIGNATURE_UTIL_PATH
    rm -rf ./content-test-conf-master
    rm -rf ./test_configuration.zip
  else
    unzip ./test_configuration.zip
    cp -r ./content-test-conf-$UNDERSCORE_CIRCLE_BRANCH/awsinstancetool ./Tests/scripts/awsinstancetool
    cp -r ./content-test-conf-$UNDERSCORE_CIRCLE_BRANCH/demisto.lic $DEMISTO_LIC_PATH
    cp -r ./content-test-conf-$UNDERSCORE_CIRCLE_BRANCH/conf.json $SECRET_CONF_PATH
    cp -r ./content-test-conf-$UNDERSCORE_CIRCLE_BRANCH/signDirectory $DEMISTO_PACK_SIGNATURE_UTIL_PATH
    rm -rf ./content-test-conf-$UNDERSCORE_CIRCLE_BRANCH
    rm -rf ./test_configuration.zip
fi

set -e
=======
curl  --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN"  \
      --location "https://api.github.com/repos/demisto/content-test-conf/contents/conf.json?ref=$CIRCLE_BRANCH" -o "$SECRET_CONF_PATH"

NOT_FOUND_MESSAGE=$(cat $SECRET_CONF_PATH | jq '.message')

if [ "$NOT_FOUND_MESSAGE" != 'null' ]
  then
    echo "Branch $CIRCLE_BRANCH does not exists in content-test-conf repo - downloading from master"
    echo "Got message from github=$NOT_FOUND_MESSAGE"

    curl  --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN"  \
      --location "https://api.github.com/repos/demisto/content-test-conf/contents/conf.json" -o "$SECRET_CONF_PATH"

    echo "Downloading license file..."
    curl  --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN"  \
      --location "https://api.github.com/repos/demisto/content-test-conf/contents/demisto.lic" -o "$DEMISTO_LIC_PATH"

    echo "Downloading instance conf file..."
    if [ -n "${NIGHTLY}" ]
      then
        curl  --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN"  \
          --location "https://api.github.com/repos/demisto/content-test-conf/contents/nightly_instance.json" -o "instance.json"

      else
        curl  --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN"  \
          --location "https://api.github.com/repos/demisto/content-test-conf/contents/instance.json" -o "instance.json"

    fi

  else
    echo "Downloading license file..."
    curl  --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN"  \
      --location "https://api.github.com/repos/demisto/content-test-conf/contents/demisto.lic?ref=$CIRCLE_BRANCH" -o "$DEMISTO_LIC_PATH"

    echo "Downloading instance conf file..."
    if [ -n "${NIGHTLY}" ]
      then
        curl  --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN"  \
          --location "https://api.github.com/repos/demisto/content-test-conf/contents/nightly_instance.json?ref=$CIRCLE_BRANCH" -o "instance.json"

      else
        curl  --header "Accept: application/vnd.github.v3.raw" --header "Authorization: token $GITHUB_TOKEN"  \
          --location "https://api.github.com/repos/demisto/content-test-conf/contents/instance.json?ref=$CIRCLE_BRANCH" -o "instance.json"

    fi

fi
echo "using instance:"
cat instance.json
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
echo "Successfully downloaded configuration files"
