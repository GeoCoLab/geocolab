# !/usr/bin/env python
# encoding: utf-8

from setuptools import find_packages, setup

NAME = 'geocolab'
DESCRIPTION = 'Proof of concept app for the NERC digital technologies sprint.'
URL = 'https://github.com/geocolab'
EMAIL = 'geocolab.app@gmail.com'
AUTHOR = 'GeoCoLab'
VERSION = '1.0.0'
REQUIRED = ['gunicorn',
            'celery[redis]',
            'flask-wtf',
            'flask-login',
            'flask-mail',
            'flask-migrate',
            'flask-sqlalchemy',
            'flask',
            'geonamescache',
            'psycopg2',
            'passlib[argon2]',
            'wheel']

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'geocolab=backend.geocolab.cli:cli'
        ],
    },
    license='GPL-3.0-or-later'
)
