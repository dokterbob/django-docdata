django-docdata
##############

.. image:: https://secure.travis-ci.org/dokterbob/django-docdata.png?branch=master
    :target: http://travis-ci.org/dokterbob/django-docdata

Python/Django client to the Docdata payment system.
*****************************************************

What it does
============
This package offers Python and Django integration for Docdata's WebMenu
product. It offers a direct abstraction of the API living in
`docdata.interface` which does not use Django for anything other than UTF-8
encoding of URL's. On top of this we implemented a Django persistence layer
and a `payment_status_changed` signal for easy integration into webshops and
other applications requiring payments.

Who uses this
=============
The `1%CLUB <https://onepercentclub.com/>`_ is using this in their Open Source crowdfunding platform `Project Bluebottle <https://github.com/onepercentclub/bluebottle>`_. Some version of this software has been included in `pcommerce.payment.docdata <https://pypi.python.org/pypi/pcommerce.payment.docdata/>`_ by Huub Bouma. And
surely, we are using this package in-house over at `Visualspace <http://www.visualspace.nl/>`_ as well, ona fairly large production webshop.

Tests
=================
This package has fairly extensive test coverage. However, a significant
portion of the tests currently requires a testing account and
hence `DOCDATA_MERCHANT_NAME` and `DOCDATA_MERCHANT_PASSWORD` to be setup in
the file `test_secrets.py` (see `test_secrets.example`). After that the tests
can be run with::

    python setup.py test

Only the online tests are currently being run with Travis. If you fire pull
requests I would tremendously appreciate offline test coverage
using `httpmock <https://pypi.python.org/pypi/httmock/>`_) over the existing
offline tests, ideally based on the examples in Docdata's
implementation manual.

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
