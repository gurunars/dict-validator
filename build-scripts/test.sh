#!/bin/bash

set -eu

PKG_NAME=$(python setup.py --provides)

pep8 ${PKG_NAME}
pyflakes ${PKG_NAME}
./build-scripts/custom_pylint.py --rcfile=build-scripts/pylintrc ${PKG_NAME}
nosetests --with-coverage --with-doctest --cover-package=${PKG_NAME} \
          --cover-min-percentage=100
