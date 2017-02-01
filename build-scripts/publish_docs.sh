#!/bin/bash

set -eu

# Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
openssl aes-256-cbc -K ${ENCRYPTED_KEY} -iv ${ENCRYPTED_IV} \
                    -in deploy_key.enc -out deploy_key -d
chmod 600 deploy_key
eval $(ssh-agent -s)
ssh-add deploy_key

NAME=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32)

cp -ar .docs/html /tmp/${NAME}
cd /tmp/${NAME}
git init
git config user.email "publisher@gurunars.com"
git config user.name "Publisher"
git checkout -b gh-pages
touch .nojekyll
git add .
git commit -am init
git remote add origin ${ORIGIN}
git push origin gh-pages -f
rm -rf /tmp/${NAME}