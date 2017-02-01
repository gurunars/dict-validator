#!/bin/bash

set -eu

pep8 dict_validator
pyflakes dict_validator
./build-scripts/custom_pylint.py --rcfile=dict_validator/.pylintrc dict_validator
nosetests --with-coverage --with-doctest --cover-package=dict_validator \
          --cover-min-percentage=100