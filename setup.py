#!/usr/bin/python
import os
import sys

from setuptools import setup, find_packages

assert sys.version_info.major >= 3, "Only Python 2 is supported"

SRC_DIR = os.path.dirname(__file__)
CHANGES_FILE = os.path.join(SRC_DIR, "CHANGES")

with open(CHANGES_FILE) as fil:
    version = fil.readline().split()[0]


setup(
    url="https://github.com/gurunars/dict-validator",
    name="dict-validator",
    install_requires=[],
    description="A library for structural data validation.",
    version=version,
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
        'Programming Language :: Python :: 2'
    ]
)
