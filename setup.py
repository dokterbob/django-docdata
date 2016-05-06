#!/usr/bin/env python

import warnings

from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except:
    warnings.warn('Could not read README.rst')
    README = None

try:
    REQUIREMENTS = open('requirements.txt').read()
except:
    warnings.warn('Could not read requirements.txt')
    REQUIREMENTS = None

try:
    TEST_REQUIREMENTS = open('requirements_test.txt').read()
except:
    warnings.warn('Could not read requirements_test.txt')
    TEST_REQUIREMENTS = None


setup(
    name='django-docdata',
    version='0.9',
    description='Python/Django client to the Docdata payment system.',
    long_description=README,
    install_requires=REQUIREMENTS,
    author='Mathijs de Bruin',
    author_email='mathijs@mathijsfietst.nl',
    license='AGPL',
    url='http://github.com/dokterbob/django-docdata/',
    packages=find_packages(exclude=("tests", "test_project")),
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
    test_suite='runtests.run_tests',
    tests_require=TEST_REQUIREMENTS
)
