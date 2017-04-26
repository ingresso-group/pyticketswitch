.. _advanced:

Advanced Guide
--------------

This guide provides additional information about parts of the wrapper that
expands on the :ref:`quick start guide <quickstart>`

Demo User Events
================

.. _demo_events:

At the time of writing this documentation the demo user has access to the
following events:

+---------+------------------------------------+---------------------------------------------------------------------+
| id      | description                        | additional attributes                                               |
+=========+====================================+=====================================================================+
| ``6IE`` | Matthew Bourne's Swan Lake test    | - seated                                                            |
|         |                                    | - default discounts only                                            |
|         |                                    | - reservations for tuesday performances                             |
|         |                                    | - has restricted view seats on ticket 2 and 3 on thursdays          |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``6IF`` | Matthew Bourne's Nutcracker TEST   | - seated                                                            |
|         |                                    | - maximum of 3 mixed discounts                                      |
|         |                                    | - no availability on Saturday nights                                |
|         |                                    | - no discounts in the stalls on the 1st of the month                |
|         |                                    | - no OPA or STUDENT discounts in price band B                       |
|         |                                    | - collect from the venue and post dispatch methods available        |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``6KF`` | V&A Memberships                    | - subscription                                                      |
|         |                                    | - has only single performance that must be selected                 |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``6KS`` | 1-Day Ticket                       | - attraction                                                        |
+---------+------------------------------------+ - not valid on mondays                                              |
| ``6KT`` | 3-Day Hopper                       |                                                                     |
+---------+------------------------------------+                                                                     |
| ``6KU`` | Family Ticket                      |                                                                     |
+---------+------------------------------------+                                                                     |
| ``6KV`` | Individual Ticket                  |                                                                     |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``6L9`` | La Femme                           | - seated                                                            |
|         |                                    | - blanket discounts                                                 |
|         |                                    | - special offer                                                     |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``7AA`` | Toy Story - The Opera              | - seated                                                            |
|         |                                    | - seat selection                                                    |
|         |                                    | - seating plan data available                                       |
|         |                                    | - contiguous seat selection only                                    |
|         |                                    | - cannot leave single seats                                         |
|         |                                    | - self print vouchers                                               |
|         |                                    | - reservations including seat H10 will always fail                  |
|         |                                    | - reservations including seat D7 will return a different            | 
|         |                                    |   seat selection from the same block of seats (as if                |
|         |                                    |   that seat had become unavailable)                                 |
|         |                                    |                                                                     |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``7AB`` | The Unremarkable Incident          | - seated                                                            |
|         | of the Cat at Lunchtime            | - seat selection                                                    |
|         |                                    | - seating plan data available                                       |
|         |                                    | - allows discontiguous seat selection                               |
|         |                                    | - self print vouchers with barcodes                                 |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``9XW`` | Five Day Park Hopper Ticket        | - attraction                                                        |
+---------+------------------------------------+ - is post only (can be used to generate ‘no sends’                  |
| ``9XY`` | Two day Parkhopper                 |   if you select a performance date within the next few days)        |
|         |                                    |                                                                     |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``AG8`` | 1デーパスポート (One Day Passport) | - attraction                                                        |
|         |                                    | - text in japanese (useful for testing unicode support)             |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``DBZ`` | Moulin Rouge (Dinner Show)         | - seated                                                            |
|         |                                    | - priced in euros                                                   |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``DP9`` | Imperial Helicopter Tour           | - tour                                                              |
+---------+------------------------------------+ - many performances (useful for testing pagination, calendars, etc) |
| ``DPB`` | North Canyon Helicopter Tour       |                                                                     |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``GVA`` | Souvenir DVD                       | - merchandise                                                       |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``I3R`` | MGM Grand Accomodation             | - hotel                                                             |
+---------+------------------------------------+                                                                     |
| ``I3S`` | Athenaeum                          |                                                                     |
+---------+------------------------------------+                                                                     |
| ``I3T`` | Corus Hyde Park                    |                                                                     |
+---------+------------------------------------+                                                                     |
| ``I3U`` | Hilton Kensington                  |                                                                     |
+---------+------------------------------------+                                                                     |
| ``I3V`` | St Ermin's                         |                                                                     |
+---------+------------------------------------+---------------------------------------------------------------------+


Searching for an Event
======================

.. _event_search:

With no arguments the :meth:`list_events
<pyticketswitch.client.Client.list_events>` will return all events that are
available to your user.

However it is possible to filter the events via a keyword search::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> events, meta = client.list_events(keywords=['matthew', 'bourne'])
    >>> events
    [<Event 6IF:b"Matthew Bourne's Nutcracker TEST">,
     <Event 6IE:b"Matthew Bourne's Swan Lake test">]
    >>> 

Or by country::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> events, meta = client.list_events(country_code='jp')
    >>> events
    [<Event AG8:'1 デーパスポート (One Day Passport)'>]
    >>> 

Or by city::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> events, meta = client.list_events(city_code='paris-fr')
    >>> events
    [<Event DBZ:b'Moulin Rouge (Dinner Show)'>,
     <Event GVA:b'Souvenir DVD'>]
    >>> 

Or within a geographical radius::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> events, meta = client.list_events(latitude=50.62, longitude=3.05, radius=20)
    >>> events
    [<Event 6KS:b'1-Day Ticket'>,
     <Event 6KT:b'3-Day Hopper'>]
    >>> 

When you combine search terms, only intersecting results are returned::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> events, meta = client.list_events(city_code='london-uk')
    >>> events
    [<Event I3S:b'Athenaeum'>,
     <Event I3T:b'Corus Hyde Park'>,
     <Event I3U:b'Hilton Kensington'>,
     <Event 6IF:b"Matthew Bourne's Nutcracker TEST">,
     <Event 6IE:b"Matthew Bourne's Swan Lake test">,
     <Event I3V:b"St Ermin's">,
     <Event 7AB:b'The Unremarkable Incident of the Cat at Lunchtime'>,
     <Event 7AA:b'Toy Story - The Opera'>,
     <Event 6KF:b'V&A Memberships'>]
    >>> events, meta = client.list_events(keywords=['park'])
    >>> events
    [<Event 6KS:b'1-Day Ticket'>,
     <Event AG8:b'1 (One Day Passport)'>,
     <Event 6KT:b'3-Day Hopper'>,
     <Event I3T:b'Corus Hyde Park'>,
     <Event 9XW:b'Five Day Park Hopper Ticket'>,
     <Event 6KV:b'Individual Ticket'>,
     <Event 9XY:b'Two day Parkhopper'>]
    >>> events, meta = client.list_events(keywords=['park'], city_code='london-uk')
    >>> events
    [<Event I3T:b'Corus Hyde Park'>]
    >>> 

Pagination
==========

.. _pagination:

Some calls to the API will return paginated results (most notibly the event and
performance methods). Some of the responses to these calls can be incredibly
long, and so to avoid frying both our servers and yours, these responses are 
fragmented into multiple "pages".

Paginated responses will return meta data objects which inherit from the
:class:`PaginationMixin <pyticketswitch.mixins.PaginationMixin>`::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> events, meta = client.list_events()
    >>> meta.is_paginated()
    False
    >>> meta.page_number
    0
    >>> meta.page_length
    50
    >>> meta.total_results
    29
    >>> meta.pages_remaining
    0
    >>> meta.results_remaining
    0
    >>> performances, meta = client.list_performances('DP9')
    >>> meta.is_paginated()
    True
    >>> meta.page_number
    0
    >>> meta.page_length
    50
    >>> meta.total_results
    360
    >>> meta.results_remaining
    310
    >>> performances, meta = client.list_performances('DP9', page=1)
    >>> meta.page_number
    1
    >>> meta.results_remaining
    260
    >>> meta.pages_remaining
    6
    >>> 

you can specify both the page number and length as parameters to all calls::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> performances, meta = client.list_performances('DP9', page_length=20, page=2)
    >>> meta.page_number
    2
    >>> meta.page_length
    20
    >>> meta.total_results
    360
    >>> meta.results_remaining
    300
    >>> meta.pages_remaining
    15
    >>> 


Requesting Seat Availability
============================

.. _seated_availability:

The primary mode of sale for all seated backend systems is concept called 
*"best available"* where you specify a ticket type and a price band and we (or
more likely the backend system) picks the specific seats for you from the
seats we have available.

Most theatre backend systems can provide both a list of available seats at
availabilty level and the abililty to reserve specific seats at the reservation
level.

Availability
~~~~~~~~~~~~

To request the available seats simply add the ``seats_blocks`` flag to the
availabilty call::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> ticket_types, meta = client.get_availability('7AA-4', seat_blocks=True)
    >>> for ticket_type in ticket_types:
    ...     for price_band in ticket_type.price_bands:
    ...         for seat_block in price_band.seat_blocks:
    ...             print('SeatBlock with length:', seat_block.length)
    ...             for seat in seat_block.seats:
    ...                 print(seat)
    ...                 
    ...             
    ...         
    ...     
    ... 
    SeatBlock with length: 10
    <Seat A1>
    <Seat A2>
    <Seat A3>
    <Seat A4>
    <Seat A5>
    <Seat A6>
    <Seat A7>
    <Seat A8>
    <Seat A9>
    <Seat A10>
    SeatBlock with length: 8
    <Seat B2>
    <Seat B3>
    <Seat B4>
    <Seat B5>
    <Seat B6>
    <Seat B7>
    <Seat B8>
    <Seat B9>
    SeatBlock with length: 4
    <Seat C3>
    <Seat C4>
    <Seat C5>
    <Seat C6>
    SeatBlock with length: 6
    <Seat D2>
    <Seat D3>
    <Seat D4>
    <Seat D5>
    <Seat D6>
    <Seat D7>
    SeatBlock with length: 2
    <Seat E4>
    <Seat E5>
    SeatBlock with length: 3
    <Seat E7>
    <Seat E8>
    <Seat E9>
    SeatBlock with length: 3
    <Seat F1>
    <Seat F2>
    <Seat F3>
    SeatBlock with length: 4
    <Seat G7>
    <Seat G8>
    <Seat G9>
    <Seat G10>
    SeatBlock with length: 4
    <Seat H1>
    <Seat H2>
    <Seat H3>
    <Seat H4>
    SeatBlock with length: 4
    <Seat H7>
    <Seat H8>
    <Seat H9>
    <Seat H10>

The results will contain a list of seat blocks (all seats in a seat block are
adjacent to one another and can be considered to be *contiguous*, sort of like
a linked list) and each seat block will contain a list of seats.

If you don't care about the seat blocks you can just use the helper method on
ticket type or price band::

    >>> ticket_type = ticket_types[1]
    >>> ticket_type.get_seats()
    [<Seat E4>,
     <Seat E5>,
     <Seat E7>,
     <Seat E8>,
     <Seat E9>,
     <Seat F1>,
     <Seat F2>,
     <Seat F3>,
     <Seat G7>,
     <Seat G8>,
     <Seat G9>,
     <Seat G10>,
     <Seat H1>,
     <Seat H2>,
     <Seat H3>,
     <Seat H4>,
     <Seat H7>,
     <Seat H8>,
     <Seat H9>,
     <Seat H10>]
    >>> price_band = ticket_type.price_bands[1]
    >>> price_band.get_seats()
    [<Seat G7>,
     <Seat G8>,
     <Seat G9>,
     <Seat G10>,
     <Seat H1>,
     <Seat H2>,
     <Seat H3>,
     <Seat H4>,
     <Seat H7>,
     <Seat H8>,
     <Seat H9>,
     <Seat H10>]
    >>> 


The :class:`AvailabilityMeta <pyticketswitch.availability.AvailabilityMeta>`
object returned with your availability data includes some information on what
seats can be selected::

    >>> meta.contiguous_seat_selection_only
    True
    >>> meta.valid_quantities
    [1, 2, 3, 4, 5, 6]
    >>>

When :class:`contiguous_seat_selection_only 
<pyticketswitch.availability.AvailabilityMeta.contiguous_seat_selection_only>`
flag is set then you may only select consecutive seats from a single seat
block. This a common requirement and is something you should keep in mind when
developing a seat selection booking application.

Valid quantities indicates what number of tickets will be considered valid for
a backend system. For example a system that required all tickets to be bought
in pairs (think parent + child events perhaps) might return ``[2, 4, 6]``
whereas a system that had a cap on the maximum tickets purchasable by one
customer might return ``[1, 2, 3]``.

Reservation
~~~~~~~~~~~

Once your customer has selected the seats they want you should reserve them
for them with the ``seats`` argument to the :meth:`make_reservation
<pyticketswitch.client.Client.make_reservation>` call::

    >>> reservation, meta = client.make_reservation(
    ...     performance_id='7AA-4',
    ...     price_band_code='B/pool',
    ...     ticket_type_code='CIRCLE',
    ...     seats=['G7', 'G8'],
    ...     number_of_seats=2
    ... )
    ...
    >>>


For each order you should then check that you got what you where expecting::

    >>> # We only made one order so we extract it from the trolley
    >>> order = reservation.trolley.get_orders()[0]
    >>> order.requested_seat_ids
    ['G7', 'G8']
    >>> order.get_seat_ids()
    ['G7', 'G8']
    >>> order.seat_request_status
    'got_all'
    >>>

It's possible that between being shown availability and making the reservation
those seats were already taken by someone else. In this situation you would get
a different seat_request_status and availabile seats from the same price band::

    >>> reservation, meta = client.make_reservation(
    ...     performance_id='7AA-4',
    ...     price_band_code='B/pool',
    ...     ticket_type_code='STALLS',
    ...     seats=['D6', 'D7'],
    ...     number_of_seats=2
    ... )
    ...
    >>> order = reservation.trolley.get_orders()[0]
    >>> order.requested_seat_ids
    ['D6', 'D7']
    >>> order.get_seat_ids()
    ['D2', 'D3']
    >>> order.seat_request_status
    'got_none'


The possible values for seat_request_status are ``got_all``, ``got_none``,
``got_some``, and ``not_requested``.

.. note:: When you were given seats you no longer want, please consider
          releasing them so that someone else can have them.

.. warning:: When releasing seated tickets there is no garentuee that the same
             seats will be instantly available again. Someone else might have
             taken them, or it may take some time for the backend system to
             recycle them.

Best available should be considered the common standard and you should be aware
of it even if you only intend on implementing seat selection.


Trollies, Bundles, Orders and Ticket orders
===========================================

.. _trollies_bundles_orders_ticket_orders:

Trolley -> Bundle -> Order -> TicketOrder

Basketing
=========

.. _basketing:

I puts the item in the baskets

Sorting search results
======================

.. _sorting_search_results:

The ``sort_order`` argument of the 
:func:`Client.list_events <pyticketswitch.client.Client.list_events>`
method will sort returned events by the specified metric.

Valid values for this attribute are as follows:

===================  ====================================================================
      Value                                    Description
===================  ====================================================================
``most_popular``     sales across all partners over the last 48 hours in descending order
``alphabetic``       event description in ascending order alphabetically
``cost_ascending``   minimum total cost of the ticket in ascending order
``cost_descending``  maximum total cost of the ticket in descending order
``critic_rating``    average critic rating in descending order
``recent``           date we first saw the event in descending order
``last_sale``        the last time we sold a ticket for the event in descending order
===================  ====================================================================

The default sort order is ``alphabetic``. The secondary sorting metric is
always ``alphabetic``.

Taking payments
===============

.. _taking_payments:

SHOW ME THE MONEY


Handling callouts
=================

.. _handling_callouts:

London calling.... hello?

Frontend Integrations
=====================

.. _frontend_integrations:

doing all the stripe and the paypals and the meta debitings etc.


