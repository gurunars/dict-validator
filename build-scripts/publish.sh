#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -f ${DIR}/pypirc ]; then
    cp ${DIR}/pypirc ~/.pypirc
fi

python setup.py sdist upload -r pypi