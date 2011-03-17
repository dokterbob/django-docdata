#!/usr/bin/env python
import sys
from os.path import dirname, abspath
from django.conf import settings

if not settings.configured:
    settings.configure(
        
        DATABASE_ENGINE='sqlite3',
        # HACK: this fixes our threaded runserver remote tests
        DATABASE_NAME='test_docdata.sqlite',
        TEST_DATABASE_NAME='test_docdata.sqlite',
        INSTALLED_APPS=[
            'docdata',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,
    )

from django.test.simple import run_tests

def runtests(*test_args):
    if not test_args:
        test_args = ['docdata']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])