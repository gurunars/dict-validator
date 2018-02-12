#!/bin/bash

set -eu

ORIGIN=$(git config remote.origin.url)
ORIGIN=${ORIGIN/https:\/\/github.com\//git@github.com:}
ORIGIN=${ORIGIN%/}

NAME=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32)

cp -ar gen-docs/html /tmp/${NAME}
cd /tmp/${NAME}
git init
git config user.email "publisher@ci-machine"
git config user.name "Publisher"
git checkout -b gh-pages
touch .nojekyll
git add .
git commit -am init
git remote add origin ${ORIGIN}
git push origin gh-pages -f
rm -rf /tmp/${NAME}