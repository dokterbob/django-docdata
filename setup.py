#!/usr/bin/env python

from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except:
    README = None

try: 
    LICENSE = open('LICENSE.txt').read()
except: 
    LICENSE = None

setup(
    name = 'django-docdata',
    version = '0.1',
    description='Python/Django client to the Docdata payment system.',
    long_description=README,
    author = 'Mathijs de Bruin',
    author_email = 'mathijs@mathijsfietst.nl',
    license = LICENSE,
    url = 'http://github.com/dokterbob/django-docdata/',
    packages = find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
    ],
)
