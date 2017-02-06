.. _quickstart:

Quick Start 
-----------

This page is intended as a quick introduction to pyticketswitch. As such we 
won't cover all the options and things you can do, just a brief end to end 
transaction into a test system.

For the purposes of this example we will use the demo credentials::

    user_id: demo
    password: demopass


If/when you want to play with real products then drop us a line at
commercial@ingresso.co.uk

Ensure that you have pyticketswitch :ref:`properly installed <install>` before
continuing.

The Client
==========

The pyticketswitch wrapper is focused around the 
:class:`Client <pyticketswitch.client.Client>`. Begin by importing it, and
instantiating it with your credentials::

    >>> from pyticketswitch import Client
    >>> client = Client('demo', 'demopass')

We will use this client for the rest of this example. If you loose it somehow
(for example by closing your terminal), just instantiate a new one. The client
holds no relevant state other than the authentication credentials.


Finding Events
==============

The top level object exposed by the API is the 
:class:`Event <pyticketswitch.event.Event>` object and the primary way of 
finding events is 
:func:`list_events() <pyticketswitch.client.Client.list_events()>`::

    >>> client.list_events()
    [
        <Event 6KS: 1-Day Ticket>,
        <Event 6IF: Matthew Bourne's Nutcracker TEST>,
        <Event 6KT: 3-Day Hopper>
        ...
    ]

.. note:: :func:`list_events <pyticketswitch.client.Client.list_performances>` 
          is paginated, as such by default the response will only contain 50
          results. See :ref:`Pagination <pagination>` for more information.

This method will take a number of additional parameters that filter and expand
the results. See :ref:`Searching for an event <event_search>` for more 
information

The demo account has access to a handful of fake events and performances that
should demonstrate most of the common capabilities of the system. For more
information see :ref:`Demo user events <demo_events>`

For the rest of this guide we are going to focus on just a single event 
``6IF: Matthew Bourne's Nutcracker TEST``

If you already have and event ID (the ``6IF`` bit) you can query it directly
with the :func:`get_event(event_id) <pyticketswitch.client.Client.get_event>` method::
    
    >>> client.get_event('6IF')
    <Event 6IF:Matthew Bourne's Nutcracker TEST>


Events have a number of useful attributes from geographic location to critic
reviews. See the :class:`Event <pyticketswitch.event.Event>`'s documentation
for more details.

For the time being all we need to know about this event is that it 
:attr:`is_seated <pyticketswitch.client.Client.is_seated>`, it
:attr:`has_performances <pyticketswitch.client.Client.has_performances>`, and
it :attr:`needs_performance <pyticketswitch.client.Client.needs_performance>`
to book.

Performances
============

To see available performances for a given event we can use the 
:func:`list_performances(event_id) <pyticketswitch.client.Client.list_performances>`
client method::
    
    >>> client.list_performances('6IF')
    [<Performance 6IF-A86: 2017-02-03T19:30:00+00:00>,
     <Performance 6IF-A88: 2017-02-05T19:30:00+00:00>,
     ...,
     <Performance 6IF-B1H: 2017-06-02T19:30:00+01:00>]


.. note:: :func:`list_performances <pyticketswitch.client.Client.list_performances>` 
          is paginated, as such by default the response will only contain 50
          results. See :ref:`Pagination <pagination>` for more information.
          

For the rest of this guide we will focus on the performance furthest from today
``6IF-B1H``. 

Like with events you can use the 
:func:`get_performance(performance_id) <pyticketswitch.client.Client.get_performance>`
method to retrieve a specific performance when you have the performance ID::

    >>> client.get_performance('6IF-B1H')
    <Performance 6IF-B1H: 2017-06-02T19:30:00+01:00>

.. warning:: The performance might have passed by the time you read this, if it
             has then just select another event from the list. **Try and make sure
             it is not a Saturday**, as this will break (intentionally) at later
             stages.

See :class:`Performance <pyticketswitch.performance.Performance>` Documentation
for more information on performances. All we need for now is the 
:attr:`Performance.id <pyticketswitch.performance.Performance.id>` attribute.


Availability
============

Now that we have an :class:`Event <pyticketswitch.event.Event>` and a
:ref:`Performance <pyticketswitch.performance.Performance>`, we need to find
out what tickets and prices are available::
    
    >>> ticket_types, meta = client.get_availability('6IF-B1H')
    >>> ticket_types
    [<TicketType CIRCLE: Upper circle>,
     <TicketType STALLS: Stalls>,
     <TicketType BALCONY: Balcony>]

:func:`get_availability <pyticketswitch.client.Client.get_availability>` returns
a list of :class:`TicketTypes <pyticketswitch.ticket_type.TicketType>` and an
:class:`AvailabilityMeta <pyticketswitch.availability.AvailabilityMeta>` object.

A ticket type can be generally considered to be a part of house, or part of a
venue. :class:`TicketTypes <pyticketswitch.ticket_type.TicketType>` don't have
prices directly attributed to them, but they contain 
:class:`PriceBands <pyticketswitch.price_band.PriceBand>` which in turn contain
a default :class:`Discount <pyticketswitch.discount.Discount>` which does::

    >>> ticket_type = ticket_types[0]
    >>> ticket_type.price_bands





The meta object contains aggregate information relevant to the ticket types and
their children. For example it can be used to the currency of prices and what
are valid quantities available::
    
    >>> meta.valid_quantities
    [2, 3, 4, 5]
    >>> meta.currency
    <Currency gbp>
