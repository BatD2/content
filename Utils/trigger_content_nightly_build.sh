#!/usr/bin/env bash

<<<<<<< HEAD
_circle_token=$1
[ -n "$2" ] && _branch="$2" || _branch="$(git branch  --show-current)"

trigger_build_url="https://circleci.com/api/v2/project/github/demisto/content/pipeline"

post_data=$(cat <<-EOF
{
  "branch": "${_branch}",
  "parameters": {
    "nightly": "true",
    "time_to_live": "900"
  }
}
EOF
)

=======
_branch=$1
_circle_token=$2

trigger_build_url=https://circleci.com/api/v1/project/demisto/content/tree/${_branch}?circle-token=${_circle_token}

post_data=$(cat <<EOF
{
  "build_parameters": {
    "NIGHTLY": "true"
  }
}
EOF)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07

curl \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
<<<<<<< HEAD
-k \
--data "${post_data}" \
--request POST ${trigger_build_url} \
--user "$_circle_token:"
=======
--data "${post_data}" \
--request POST ${trigger_build_url}
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
