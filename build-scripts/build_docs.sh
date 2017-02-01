#!/usr/bin/env bash

set -eu

NAME=$(python setup.py --name)
AUTHOR=$(python setup.py --author)
VERSION=$(python setup.py --version)

export PYTHONPATH="${PWD}"

find dict_validator -name '*.py' ! -name '__init__.py' -print0 | \
    xargs -0 sphinx-apidoc -f -M -F -T -E -d 6 \
    -H "${NAME}" \
    -A "${AUTHOR}" \
    -V "${VERSION}" \
    -R "${VERSION}" \
    dict_validator -o .docs dict_validator
sed -i "s/alabaster/sphinx_rtd_theme/g" .docs/conf.py
mv .docs/dict_validator.rst .docs/index.rst
sphinx-build -b html .docs .docs/html
echo "Docs @ file://${PWD}/.docs/html/index.html"
