#!/bin/bash

function find_in_remotes () { 
    echo "$(git remote)" | grep -F -q -w "$1"
    return $?
}

branch_name='test'
app_name='origin' # `[ $branch_name == "master" ] && echo aaa || echo aaa-test`
host='rpi'
result=$(find_in_remotes "${appname}")
echo $result

if $(find_in_remotes "${appname}"); then
    echo "found"
    # echo "git remote set-url piku piku@${host}:${app_name}";
else
    echo "not found";
    # echo "git remote add piku piku@${host}:${app_name}"
fi
