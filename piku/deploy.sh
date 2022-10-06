#!/bin/bash

set +x
set -e

PIKU_APP_NAME=$1
HOST_NAME=$2

# check if empty

branch_name=`git branch --show-current`
app_name=${PIKU_APP_NAME} 
if [ "$branch_name" != "master" ]; then
    app_name=${PIKU_APP_NAME}-test
fi

piku_address="piku@${HOST_NAME}:${app_name}"
echo ${USER} updating piku: ${piku_address}
git remote add piku ${piku_address} || git remote set-url piku ${piku_address}

piku deploy || piku
