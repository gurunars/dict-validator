#!/bin/bash

set -eu

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Travis specific
if [ -f ${DIR}/deploy_key ]; then
    chmod 600 ${DIR}/deploy_key
    eval $(ssh-agent -s)
    ssh-add ${DIR}/deploy_key
fi

ORIGIN=$(git config remote.origin.url)
ORIGIN=${ORIGIN/https:\/\/github.com\//git@github.com:}
ORIGIN=${ORIGIN%/}

NAME=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32)

cp -ar .docs/html /tmp/${NAME}
cd /tmp/${NAME}
git init
git config user.email "publisher@travis"
git config user.name "Publisher"
git checkout -b gh-pages
touch .nojekyll
git add .
git commit -am init
git remote add origin ${ORIGIN}
git push origin gh-pages -f
rm -rf /tmp/${NAME}
