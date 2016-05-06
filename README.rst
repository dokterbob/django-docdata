##############
django-docdata
##############

.. image:: https://img.shields.io/pypi/v/django-docdata.svg
    :target: https://pypi.python.org/pypi/django-docdata

.. image:: https://img.shields.io/travis/dokterbob/django-docdata/master.svg
    :target: http://travis-ci.org/dokterbob/django-docdata

.. image:: https://coveralls.io/repos/dokterbob/django-docdata/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/dokterbob/django-docdata?branch=master

.. image:: https://landscape.io/github/dokterbob/django-docdata/master/landscape.svg?style=flat
   :target: https://landscape.io/github/dokterbob/django-docdata/master
   :alt: Code Health

Python/Django client to the Docdata payment system.

What it does
============
This package offers Python and Django integration for Docdata's WebMenu
product. It offers a direct abstraction of the API living in
`docdata.interface` which does not use Django for anything other than UTF-8
encoding of URL's. On top of this we implemented a Django persistence layer
and a `payment_status_changed` signal for easy integration into webshops and
other applications requiring payments.

Supported versions
==================
This package officially supports Python 2.7 and Django 1.8 and 1.9, pull requests for Python 3 are encouraged.

Who uses this
=============
We are using this package in-house over at `Visualspace <http://www.visualspace.nl/>`_, on a fairly large production webshop. Some version of this software has been included in `pcommerce.payment.docdata <https://pypi.python.org/pypi/pcommerce.payment.docdata/>`_ by Huub Bouma.

Tests
=================
This package has fairly extensive test coverage. However, a significant
portion of the tests currently requires a testing account and
hence `DOCDATA_MERCHANT_NAME` and `DOCDATA_MERCHANT_PASSWORD` to be setup in
the file `test_secrets.py` (see `test_secrets.example`). After that the tests
can be run with::

    ./runtests.py

Coverage
--------
Only offline tests are currently being run with Travis, hence the actual coverage should be much higher. To run the online tests as well, Docdata credentials need to be configured in ``test_project/test_project/test_secrets.py``.

Pull requests for properly mocked online interactions based on the examples in Docdata's implementation manual are greatly appreciated.

Settings
========
`DOCDATA_MERCHANT_NAME`
    Credentials as supplied by the payment provider.

`DOCDATA_MERCHANT_PASSWORD`
    Credentials as supplied by the payment provider.

`DOCDATA_DEBUG`
    Whether or not to run in testing mode. Defaults to `True`.

`DOCDATA_PROFILE`
    Which profile to use for processing payments. Defaults to `standard`.
