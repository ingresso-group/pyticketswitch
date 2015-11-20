**************
pyticketswitch
**************

A Python interface for Ingresso's TicketSwitch XML API.

Contents:

.. toctree::
   :maxdepth: 2

   Interface <objects>
   exceptions
   example_usage


Overview
========

This Python library was created as a wrapper for Ingresso's Ticketswitch (TSW) XML API, to simplify the use of the API by providing a simple object oriented interface and removing some of the complexity of the TSW XML API.

Before using this library, it may be helpful to read the first few sections of the TSW API documentation, which can be found `here. <http://www.ingresso.co.uk/apidocs/>`_ This gives an outline of how the underlying API works, which may provide some insight into why the library works as it does.


General Behaviour
=================

* All functions are performed on an object and attempt to return an object or list of objects (however, there are some cases where this isn't the case). See the :doc:`Objects </objects>` page for details of the objects available.
* Exceptions will be thrown in the event of a problem, bad input or incorrect usage (they're defined in api_exceptions.py). See the :doc:`Exceptions </exceptions>` page for more information.
* On object construction, some configuration settings are required as parameters. These are the same regardless of which object is being constructed, see `Settings`_ for more information.
* A 'session' argument is required to be passed to the objects when constructed. This should be a dictionary-like object that will store data specific to the current transaction/user session.
    .. note:: This library was originally designed to be used with Django, so the 'session' object in this case is just a Django session object. But it can be replaced with any dictionary-like object that will save data per-user/transaction.

    As with the Django session, the session object passed can temporarily store data and only save the data to a data store when a 'save()' function is called on the object. The library will call save() on the session object when the data it has stored in the object should be saved to a data store (allowing for more efficient bluk operations). This functionality can be ignored though and the object can just behave like a normal dictionary.
* In the XML API, there are a number of flags that are elements with a yes/no string as the value. These are handle as boolean variables in the pyticketswitch interface.
* Generally, if the value of an attribute is unknown for any reason, None will be returned.

Settings
--------

* **username** - The TSW user.
* **password** - Password for the TSW user.
* **url** - The TSW URL.
* **accept_language** - Optional. The user's HTTP Accept-Language header; if provided, will be used to determine the language of the content returned.
* **api_request_timeout** - Optional.
* **no_time_descr** - Optional. The text to use if no time is returned by the API for a performance (i.e. there is just one performance per-day and no specific time is provided). Defaults to 'Select'.
* **default_concession_descr** - Optional. The text to use if no description is returned by the API for a concession (i.e. it is the only option for that TicketType). Defaults to 'Standard'.


Typical Transaction
===================

A typical transaction with pyticketswitch would look something like this:

    #. Create Core object
    #. Perform Event search on Core
    #. Select Event object and get the list of Performances for this Event
    #. Select Performance object and get list of TicketTypes for this Performance
    #. Select TicketType object and get the list of Concessions for this TicketType
    #. Select a Concession object for each ticket required
    #. Get list of DespatchMethods for this Performance
    #. Select a DespatchMethod object
    #. Create an Order object with the selected Concessions and DespatchMethod
    #. Create a Trolley object and add the Order to the Trolley
    #. Repeat this if more than one Order is to be purchased
    #. When ready to purchase, get a Reservation object for the Trolley
    #. Purchase the Reservation object with the 2 stage, redirected purchase process

There is a basic example of how the library could be used :doc:`here </example_usage>`.


Tests
=====

To run tests, run the following command from the root of the project:
    python -m unittest discover

Run an individual test with:
    python -m unittest pyticketswitch.test.test_interface_objs.<TestCase>.<test_method>

Tests can also be run from the root of the project using `pytest`:
    py.test

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
