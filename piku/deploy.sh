#!/bin/bash

set +x
set -e

PIKU_APP_NAME=$1

# check if empty

branch_name=`git branch --show-current`
app_name=${PIKU_APP_NAME} 
if [ "$branch_name" != "master" ]; then
    app_name=${PIKU_APP_NAME}-test
fi

piku_address="piku@localhost:${app_name}"
echo ${USER} updating piku remote: ${piku_address}
git remote add piku ${piku_address} || git remote set-url piku ${piku_address}

git fetch --unshallow
git push piku --force
