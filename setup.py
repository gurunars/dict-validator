#!/usr/bin/python
import os
import sys

from setuptools import setup, find_packages
from pip.req import parse_requirements

assert sys.version_info.major == 3, "Only Python 3 is supported"


def _pt(name):
    return os.path.join(os.path.dirname(__file__), name)


def _read(name):
    with open(_pt(name)) as fil:
        return fil.read()


def _get_version():
    return _read("CHANGES").split("\n")[0].split()[0]


def _get_long_description():
    return _read("README.rst")


def _get_requirements():
    req_f = _pt("requirements.txt")
    if os.path.exists(req_f):
        return [str(ir.req) for ir in parse_requirements(req_f)]
    else:
        return []


setup(
    url="https://github.com/gurunars/dict-validator",
    name="dict-validator",
    provides=["dict_validator"],
    install_requires=_get_requirements(),
    description="A library for structural data validation.",
    long_description=_get_long_description(),
    version=_get_version(),
    packages=find_packages(exclude=["test"]),
    author="Anton Berezin",
    author_email="gurunars@gmail.com",
    include_package_data=True,
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
