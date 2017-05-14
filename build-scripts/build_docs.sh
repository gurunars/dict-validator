#!/usr/bin/env bash

set -eu

NAME=$(python setup.py --name)
AUTHOR=$(python setup.py --author)
VERSION=$(python setup.py --version)
PKG_NAME=$(python setup.py --provides)

export PYTHONPATH="${PWD}"

find ${PKG_NAME} -name '*.py' ! -name '__init__.py' -print0 | \
    xargs -0 sphinx-apidoc -f -M -F -T -E -d 6 \
    -H "${NAME}" \
    -A "${AUTHOR}" \
    -V "${VERSION}" \
    -R "${VERSION}" \
    ${PKG_NAME} -o .docs ${PKG_NAME}
sed -i "s/alabaster/sphinx_rtd_theme/g" .docs/conf.py
mv .docs/${PKG_NAME}.rst .docs/index.rst
sphinx-build -b html .docs .docs/html
echo "Docs @ file://${PWD}/.docs/html/index.html"
