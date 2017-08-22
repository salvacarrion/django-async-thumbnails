#!/usr/bin/env python

import os
from setuptools import setup, find_packages

NAME = 'django-async-thumbnails'

VERSION = '0.1.0'

DESCRIPTION = 'Asynchronous thumbnailing for remote storages like Google Cloud Storage, Amazon S3,...'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.pypi')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Salva Carrión'
URL = "https://github.com/salvacarrion/django-async-thumbnails"
DOWNLOAD_URL = "https://github.com/salvacarrion/django-async-thumbnails/tarball/{}".format(VERSION)


KEYWORDS = [
    # [PyPi](https://pypi.python.org) packages with keyword "orange3 add-on"
    # can be installed using the Orange Add-on Manager
    'django-async-thumbnails',
    'async thumbnails',
]

INSTALL_REQUIRES = sorted(set(
    line.partition('#')[0].strip()
    for line in open(os.path.join(os.path.dirname(__file__), 'requirements.txt'))
) - {''})

if __name__ == '__main__':
    setup(
        name=NAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        version=VERSION,
        author=AUTHOR,
        url=URL,
        download_url=DOWNLOAD_URL,
        packages=find_packages(),
        platforms='any',
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        keywords=KEYWORDS,
        zip_safe=False,
    )