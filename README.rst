**************
pyticketswitch
**************

.. image:: https://img.shields.io/pypi/v/pyticketswitch.svg
    :target: https://pypi.python.org/pypi/pyticketswitch

.. image:: https://travis-ci.org/ingresso-group/pyticketswitch.svg?branch=master
    :target: https://travis-ci.org/ingresso-group/pyticketswitch

A Python interface for Ingresso's TicketSwitch XML API.

Installation
------------

Can be installed with pip::

        pip install pyticketswitch


Requirements
------------

As of version 1.8.0, this package requires the `Requests <http://docs.python-requests.org/>`_ library.

As of version 1.12.0 this package is python3 compatible.

Documentation
-------------

The `pyticketswitch documentation can be found here <http://www.ingresso.co.uk/pyticketswitch/>`_ and the general XML API documentation can be accessed `from this page <http://www.ingresso.co.uk/docs/>`_.

Bugs, features, support and discussion
--------------------------------------

Please use the `Github Issues <https://github.com/ingresso-group/pyticketswitch/issues>`_ or contact Ingresso at systems@ingresso.co.uk

Development
-----------

**Running tests**

We are using the `VCR.py <https://github.com/kevin1024/vcrpy>`_ library for
capturing and replaying API calls made to the TicketSwitch XML API. These
'cassette' files are stored in `tests/interface_objects/cassettes`.

If your are experiencing slow tests then you may need to install/link an python-development headers package.


License
-------

Copyright (c) 2016 Ingresso Group

Licensed under the The MIT License.
