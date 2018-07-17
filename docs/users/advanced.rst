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
|         |                                    | - reservations for Tuesday performances                             |
|         |                                    | - has restricted view seats on ticket 2 and 3 on Thursdays          |
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
+---------+------------------------------------+ - not valid on Mondays                                              |
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
|         |                                    | - allows discontinuous seat selection                               |
|         |                                    | - self print vouchers with barcodes                                 |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``9XW`` | Five Day Park Hopper Ticket        | - attraction                                                        |
+---------+------------------------------------+ - is post only (can be used to generate ‘no sends’                  |
| ``9XY`` | Two day Parkhopper                 |   if you select a performance date within the next few days)        |
|         |                                    |                                                                     |
+---------+------------------------------------+---------------------------------------------------------------------+
| ``AG8`` | 1デーパスポート (One Day Passport) | - attraction                                                        |
|         |                                    | - text in Japanese (useful for testing unicode support)             |
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

You can specify both the page number and length as parameters to all calls::

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
availability level and the ability to reserve specific seats at the reservation
level.

Availability
~~~~~~~~~~~~

To request the available seats simply add the ``seats_blocks`` flag to the
availability call::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> ticket_types, meta = client.get_availability(
    ...     performance_id='7AA-4',
    ...     seat_blocks=True
    ... )
    ...
    >>> for ticket_type in ticket_types:
    ...     for price_band in ticket_type.price_bands:
    ...         for seat_block in price_band.seat_blocks:
    ...             print('SeatBlock with length:', seat_block.length)
    ...             for seat in seat_block.seats:
    ...                 print(seat)
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
in pairs (think parent + child events perhaps) might return ``[2, 4, 6]``,
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
a different seat_request_status and available seats from the same price band::

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

The API is designed to allow purchasing multiple tickets to multiple events in
a single transaction. To support this a transaction is organised into several
sub layers that represent the products you are after, it's important to
understand these terms and what they represent.

If you are interested in purchasing multiple items in a single transaction see
the section on :ref:`Bundling <bundling>` below.

The general hierarchy can be thought of as:

- Transaction
- Trolley
- Bundles
- Orders
- Ticket Order

Trolley
~~~~~~~

The trolley represents the general collection of stuff you want to buy. It has
a one to one mapping with the transaction and contains important stuff like
the transaction ids, purchase results, and how long you have before your
reservations expire. The details of the products you are ordering is contained
in a collection of Bundle objects inside the trolley object.

Bundle
~~~~~~

A bundle represents a collection of products from the same backend system
source. It contains information like the total cost of all it's items, the
currency that it's priced in, and the payment method it will be expecting.

Details of Individual events and performances are contained in a collection of
Orders inside the bundle object.

Order
~~~~~

An Order represents a request for tickets for a single event and performance. It
contains information such as the ticket type and prices band, the number of
seats, total price, any requested seats, the send method, and the in event of a
successful purchase the backend purchase reference.

Details of any discounts or assigned seats are contained in a collection of
ticket orders inside this parent order.

Ticket Order
~~~~~~~~~~~~

A Ticket Order represents details about specific tickets. Primarily this is used
to indicate discounts and assigned seat ids, however it also contains
individual and total pricing.


Bundling
=========
.. _bundling:

The API supports bundling where you can purchase multiple items from different
sources as a single transaction.

For example our customer wants to go to two shows in London, and buy a museum
membership::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> events, meta = client.get_events(['6IF', '7AB', '6KF'])
    >>> events
    {'6IF': <Event 6IF:b"Matthew Bourne's Nutcracker TEST">,
     '6KF': <Event 6KF:b'V&A Memberships'>,
     '7AB': <Event 7AB:b'The Unremarkable Incident of the Cat at Lunchtime'>}
    >>>

Building a trolley is a similar process to how we 
:ref:`created a reservation in the quickstart guide <making_a_reservation>`, 
the difference here is that the trolley call doesn't actually reserve any
tickets. This way we can build up a trolley with some stuff in it and pass it
all into the reservation call in one go

First lets create an initial trolley with some tickets to the ``6IF`` event::

    >>> from pyticketswitch import Client
    >>> client = Client(user='demo', password='demopass')
    >>> trolley, meta = client.get_trolley(
    ...     number_of_seats=2,
    ...     ticket_type_code='CIRCLE',
    ...     price_band_code='A/pool',
    ...     performance_id='6IF-B0G'
    ... )
    ...
    >>> trolley.token
    's2--ys4C_FkPOSwdZM72WNGJ1ma0ZoEMYIZ8zWUGne0qaTYMcuc8ovMCWE1sQpjpLDGjZiKK_-6BtoKWkd6u3a56HP6ynJFqCNj_LW9npMLqK-PED8X6mGe-qWugFc714-0JDP31K7YpZUxoo-ADt0LIYUxC06ENJ3ZINjqr4NiWzkDwVHQtvMGAp4K9w_nRyJj2-8AqE_d3HkYfM4i17_FlxMAan0Zkd0fZF7xLySlSZCmuB-umnH-QEp9uWp8aU5yjsEht-oF36n0FgwgozQKhc6vMZxm2R6R2yP_VzSMrGM4cy_Yfoi6moZCG3IPOIu6R0ZeHgdu5RgGw8-yNBYIhx66xHnaIIIJBmQ_MqeKE5d5TBs82Ra3WZ0qAkOambTanAU2ZybRLmtLdSFqWbuFM3KCg9MDBVonmZ'
    >>> trolley.bundles
    [<Bundle ext_test0>]
    >>> trolley.bundles[0].orders
    [<Order 1>]
    >>> trolley.bundles[0].orders[0].event.id
    '6IF'
    >>>

Result! We can see we have trolley object with a trolley token which identifies
this trolley and it's current state. Our trolley now contains a single bundle
for the ``ext_test0`` backend system, and that bundle contains a single order
for the 6IF event.

Now lets add another event to our trolley by the same method, however this time
we will pass in the current trolley token as an additional argument to the
:meth:`get_trolley <pyticketswitch.client.Client.get_trolley>` call::

    >>> trolley, meta = client.get_trolley(
    ...     number_of_seats=2,
    ...     ticket_type_code='STALLS',
    ...     price_band_code='A/pool',
    ...     performance_id='7AB-4',
    ...     token=trolley.token,
    ... )
    ...
    >>> trolley.token
    'M4--hLYu4VwV6QUww385En04K9nZtOYL1uq6Xvyo24CFtP8o-uW_FHqo7DzwILJM3_aIDiCmrIXy7GJN5vkb3HtPdE-jXMEvt7zyxhKRRHzRLuKAjx3M3bhZoetSwB9jE0dYCYpLCsxjVfBCAN22TQ9jck3PD3WSbV1KR98OmQ44I8VFF4UCuBzpDCy78mbZu2DWWjeWyxHQbYM0ZNZrCEEZ2QZzWxeAVoJlCNmorxJIaek57Gr8v_Vj3jnBNLGtjQdbXmf9ENU5WYjkeX3Xgpy2ZTubusvLMn2rRMK7oZ1v4WtdL0fLdZJZNlzia9hJBeL2DQ-QmLvNawX2Rz27OV_TuvZpMkOyF9xpbADd4rg2VuwEHnU1puKX6brmy7PspildvqhjVrAwBcBR3jlDaZtCI6ACMxggTclmXUsGFjwDuWGJM9qBB3g87irMjq6TyZV1mBDFBWlq1BL-hC2Z6jIQ-968Ud8loWm5s5OVXgPZIhTqntoGZB58CinbF3hEY_CxbXycrznqkyHo7aYQVc45Iv1JnNUjvASSZ'
    >>> trolley.bundles
    [<Bundle ext_test0>, <Bundle ext_test1>]
    >>> trolley.bundles[1].orders
    [<Order 2>]
    >>> trolley.bundles[1].orders[0].event.id
    '7AB'

As you can see our trolley token has changed, and the trolley now contains an
additional bundle for ext_test1. This because ``6IF`` and ``7AB`` originate from
different source systems. Our new bundle contains a single order for ``7AB``.

We can add the museum membership in the same way::

    >>> trolley, meta = client.get_trolley(
    ...     number_of_seats=1,
    ...     ticket_type_code='MEMBER',
    ...     price_band_code='X/pool',
    ...     performance_id='6KF-F',
    ...     token=trolley.token
    ... )
    ...
    >>> trolley.bundles
    [<Bundle ext_test0>, <Bundle ext_test1>]
    >>> trolley.bundles[0].orders
    [<Order 1>, <Order 3>]
    >>> trolley.bundles[0].orders[1].event.id
    '6KF'
    >>>

As ``6KF`` and ``6IF`` are on the same backend system this order is added to our
existing ``ext_test0`` bundle.

If our customer decides that this is actually getting a bit pricey and they want
to remove their ``6IF`` tickets they can do this by removing the order (using it's
item number) from the
trolley::


    >>> trolley.bundles[0].orders[0].item
    1
    >>> trolley, meta = client.get_trolley(
    ...     item_numbers_to_remove=[1],
    ...     token=trolley.token
    ... )
    ...
    >>> trolley.get_orders()
    [<Order 3>, <Order 2>]
    >>> trolley.bundles[0].orders
    [<Order 3>]
    >>>

Order 1 has now been removed from the trolley!

When happy with the contents of the trolley, you can use the trolley token
directly in the :meth:`make_reservation()
<pyticketswitch.client.Client.make_reservation>` call::

    >>> reservation, meta = client.make_reservation(
    ...     token=trolley.token
    ... )
    ...
    >>> reservation.status
    'reserved'
    >>> reservation.trolley.transaction_uuid
    'b89747e2-29d0-11e7-b228-0025903268dc'
    >>> reservation.trolley.get_orders()
    [<Order 3>, <Order 2>]
    >>> reservation.trolley.bundles
    [<Bundle ext_test0>, <Bundle ext_test1>]
    >>>

Your trolley is now reserved and you can continue as normal through the rest of
the transaction process.

.. note:: Once the trolley is reserved it becomes immuatable. If you need to
          make changes you should release the reservation then remake it with a
          new trolley token.

          If you hang on to your trolley token from the original
          reservation you can simply restart the modification process using
          that token, avoiding the steps needed to generate a new one. 

          Only trollies returned by the :meth:`get_trolley
          <pyticketswitch.client.Client.get_trolley>` call will return trolley
          tokens.

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

There are multiple ways that we can take payment for a transaction:

- :ref:`on credit <on_credit_payments>` (we invoice you later)
- :ref:`redirection <redirect_payments>` to a third party who takes the card payment (such as paypal)
- :ref:`stripe <stripe_payments>` an on page third party payment provider
- :ref:`directly taking card payments <card_payments>`

.. note:: Generally speaking we are phasing out taking card payments directly
          and you as a user are highly unlikely to ever see a backend system
          that requires it. Regardless it's documented here in case it ever
          crops up.

The below examples will assume that you have the following customer object::

    >>> from pyticketswitch import Client
    >>> from pyticketswitch.customer import Customer
    >>> customer = Customer(
    ...     first_name='Fred',
    ...     last_name='Flintstone',
    ...     address_lines=['301 Cobble stone road', 'Bolder Lane'],
    ...     country_code='us',
    ...     email='fred@slate-rock-gravel.com',
    ...     post_code='70777',
    ...     town='Bedrock',
    ...     county='LA',
    ...     phone='0110134345'
    ... )

On credit
~~~~~~~~~
.. _on_credit_payments:

This is the simplest method of payment as it only requires customer details.
Don't worry though, we will invoice you later!::

    >>> client = Client('demo', 'demopass')
    >>> reservation, meta = client.make_reservation(
    ...     performance_id='7AB-4',
    ...     ticket_type_code='STALLS',
    ...     price_band_code='A/pool',
    ...     number_of_seats=2
    ... )
    >>> status, callout, meta = client.make_purchase(
    ...     reservation.trolley.transaction_uuid,
    ...     customer
    ... )
    >>> status.status
    'purchased'

Job done, ship it!

Redirects
~~~~~~~~~
.. _redirect_payments:

For some payments you will need to redirect your customers browser to a third
party::

    >>> client = Client('demo-redirect', 'demopass')
    >>> reservation, meta = client.make_reservation(
    ...     performance_id='7AB-4',
    ...     ticket_type_code='STALLS',
    ...     price_band_code='A/pool',
    ...     number_of_seats=2
    ... )
    >>> import uuid
    >>> from pyticketswitch.payment_methods import RedirectionDetails
    >>> token = uuid.uuid4()
    >>> details = RedirectionDetails(
    ...     token=token,
    ...     url='https://fromtheboxoffice.com/callback/{}'.format(token),
    ...     user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    ...     accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    ...     remote_site='fromtheboxoffice.com',
    ... )
    ...
    >>>


All redirect payments require a unique return token. The token should be
unique to your user, transaction, and each potential callout. We recommend a
UUID (v1 or v4) so there is no confusion (python has a good implementation).

Your return URL should contain the return token, and importantly **no query
string parameters**. It *can* be a non secure URL, but don't be that guy that
handles payments from a non secure website.

The remote site should match the domain in return URL.

To facilitate some of our weirder redirects you should also pass in your users
``User-Agent`` and ``Accept`` HTTP request headers.

With your redirect details established you can go ahead and make the
purchase::

    >>> status, callout, meta = client.make_purchase(
    ...     reservation.trolley.transaction_uuid,
    ...     customer,
    ...     payment_method=details,
    ... )
    >>> status
    None
    >>> callout
    <Callout ext_test1:95ca436e-e763-4463-954b-2b3eb4d8fdcb>

All redirect payments should return a callback but no status. :ref:`See below 
for how to handle callouts <handling_callouts>`.

Stripe
~~~~~~
.. _stripe_payments:

A common payment method for handling credit/debit cards is the third party
payment provider `stripe`_. Stripe allows us to take card payments without you
having to send us card details and the associated security nightmare that
comes with it. If stripe sounds interesting you can read more about
:ref:`handling front end integrations <frontend_integrations>`, or in
`our main API documentation 
<http://docs.ingresso.co.uk/#purchasing-with-stripe>`_, or `the 
official stripe documentation <https://stripe.com/docs>`_.

For this example  we are going to set up a reservation with more than one
bundle, this is because we must supply a stripe token for each bundle::


    >>> from pyticketswitch import Client
    >>> from pyticketswitch.customer import Customer
    >>> from pyticketswitch.payment_methods import StripeDetails
    >>> client = Client('demo-stripe', 'demopass')
    >>> trolley, meta = client.get_trolley(
    ...         performance_id='7AB-4',
    ...     ticket_type_code='STALLS',
    ...     price_band_code='A/pool',
    ...     number_of_seats=2
    ... )
    >>> reservation, meta = client.make_reservation(
    ...     token=trolley.token,
    ...     performance_id='7AA-4',
    ...     ticket_type_code='STALLS',
    ...     price_band_code='A/pool',
    ...     number_of_seats=2
    ... )
    >>> reservation.trolley.bundles
    [<Bundle ext_test0>, <Bundle ext_test1>]

We will assume that you have also managed to create a stripe token for each
bundle that represents a single use of your customers card details::

    >>> tokens = 
    >>> details = StripeDetails({
    ...     'ext_test0': 'tok_1ADFKNHIklODsaxB3LZqzvpX',
    ...     'ext_test1': 'tok_1ADFKgHIklODsaxBUr5gE6ca',
    ... })
    >>> status, callout, meta = client.make_purchase(
    ...     reservation.trolley.transaction_uuid,
    ...     customer,
    ...     payment_method=details,
    ... )
    >>> status.status
    'purchased'
    >>> 

Result good job!

Stripe payments should not return a callout if you do it in this manner.
However if you miss a token a callout for the remaining payment(s) will be
issued. If this happens you can handle the callback directly passing any
missing stripe token for each callout like so::

    >>> import uuid
    >>> status, callout, meta = client.next_callout(
    ...     callout.return_token,
    ...     uuid.uuid4(),
    ...     {'stripeToken': 'tok_1ADFKgHIklODsaxBUr5gE6ca'}
    ... )
    ...
    >>> status.status
    'purchased'
    >>> 

Card Details
~~~~~~~~~~~~

.. _card_payments:

Sometimes we need to pass the customers card details directly to the backend
system. This method of payment is being phased out and you are extremely
unlikely to come across it, and certainly not without forewarning, however
it's documented here just in case::

    >>> from pyticketswitch import Client
    >>> from pyticketswitch.payment_methods import CardDetails
    >>> client = Client('demo-creditcard', 'demopass')
    >>> reservation, meta = client.make_reservation(
    ...     performance_id='7AB-4',
    ...     ticket_type_code='STALLS',
    ...     price_band_code='A/pool',
    ...     number_of_seats=2
    ... )
    >>> details = CardDetails(
    ...     '4111 1111 1111 1111',
    ...     expiry_month=4,
    ...     expiry_year=19,
    ...     ccv2='123',
    ... )
    >>> status, callout, meta = client.make_purchase(
    ...     reservation.trolley.transaction_uuid,
    ...     customer,
    ...     payment_method=details,
    ... )
    >>> status.status
    'purchased'
    >>> 

If your customer wants to provide an alternate billing address they can do
so::

    >>> from pyticketswitch.address import Address
    >>> billing_address = Address(
    ...     lines=['Slate, Rock, and Gravel', '123 Sediment Row'],
    ...     town='Bedrock',
    ...     country_code='us',
    ...     county='LA',
    ...     post_code='70777',
    ... )
    >>> details = CardDetails(
    ...     '4111 1111 1111 1111',
    ...     expiry_month=4,
    ...     expiry_year=19,
    ...     ccv2='123',
    ...     billing_address=billing_address
    ... )
    >>> status, callout, meta = client.make_purchase(
    ...     reservation.trolley.transaction_uuid,
    ...     customer,
    ...     payment_method=details,
    ... )
    >>> status.status
    'purchased'
    >>>

Some card's require 3D secure validation, if you want to accept these cards
you must pass in the same return_url parameters as with redirect payments::

    >>> import uuid
    >>> token = uuid.uuid4()
    >>> details = CardDetails(
    ...     '4111 1111 1111 1111',
    ...     expiry_month=4,
    ...     expiry_year=19,
    ...     ccv2='123',
    ...     return_token=token,
    ...     return_url='https://fromtheboxoffice.com/callback/{}'.format(token),
    ...     user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    ...     accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    ...     remote_site='fromtheboxoffice.com',
    ... )
    ...
    >>> status, callout, meta = client.make_purchase(
    ...     reservation.trolley.transaction_uuid,
    ...     customer,
    ...     payment_method=details,
    ... )
    >>> status
    None
    >>> callout
    <Callout ext_test1:95ca436e-e763-4463-954b-2b3eb4d8fdcb>

If your customers card requires a redirect to 3D secure then a callout will be
issued :ref:`See below for how to handle callouts <handling_callouts>`.

If you don't provide redirection details, and the card in question requires 3D
secure you will receive a ``auth_failure`` error in the :attr:`purchase_result
<pyticketswitch.trolley.Trolley.purchase_result>` and :attr:`failed_3d_secure
<pyticketswitch.purchase_result.PurchaseResult.failed_3d_secure>` will be set
to :obj:`True`.


Handling Callouts
=================

.. _handling_callouts:

Some payment methods may require redirecting your customer's browser to a
third party. In these situations the :meth:`make_purchase
<pyticketswitch.client.Client.make_purchase>` call or :meth:`next_callout
<pyticketswitch.client.Client.next_callout>` call will return a 
:class:`Callout <pyticketswitch.callout.Callout>` object providing details of
where to send your customer::

    >>> status, callout, meta = client.make_purchase(
    ...     reservation.trolley.transaction_uuid,
    ...     customer,
    ...     payment_method=details,
    ... )
    >>> status
    None
    >>> callout
    <Callout ext_test1:95ca436e-e763-4463-954b-2b3eb4d8fdcb>
    >>> callout.code
    'ext_test1'
    >>> callout.type
    'get'
    >>> callout.destination
    'https://api.ticketswitch.com/tickets/dummy_redirect.buy/demo-redirect'
    >>> callout.parameters
    OrderedDict([
        ('return_url', 'https://fromtheboxoffice.com/callback/010288fe-a196-401f-8319-57bfe0cba552'),
        ('title', "Dummy external card details page for debit on system 'ext_test1'")
    ])
    >>> callout.return_token
    '010288fe-a196-401f-8319-57bfe0cba552'

For simple ``get`` callouts you can just build the URL by adding the callout
parameters to the callout destination::

    >>> from urllib.parse import urlencode
    >>> url = callout.destination
    >>> if callout.parameters:
    ...     url = '{}?{}'.format(
    ...         callout.destination,
    ...         urlencode(callout.parameters),
    ...     )
    ...
    >>> url
    'https://api.ticketswitch.com/tickets/dummy_redirect.buy/demo-redirect?return_url=https%3A%2F%2Ffromtheboxoffice.com%2Fcallback%2F010288fe-a196-401f-8319-57bfe0cba552&title=Dummy+external+card+details+page+for+debit+on+system+%27ext_test1%27'

You can then redirect your customer to the URL with a 302 direct.

Some callouts require a ``post`` request to the destination::

    >>> callout.code
    'ext_test1'
    >>> callout.type
    'post'
    >>> callout.destination
    'https://api.ticketswitch.com/tickets/dummy_redirect.buy/demo-redirect'
    >>> callout.parameters
    OrderedDict([
        ('return_url', 'https://fromtheboxoffice.com/callback/010288fe-a196-401f-8319-57bfe0cba552'),
        ('title', "Dummy external card details page for debit on system 'ext_test1'")
    ])


This cannot be achieved with a simple redirect. Instead you must render an
HTML form and either submit it on behalf of the user or have the user submit
it themselves::

    <html>
      <head>
        <title>Redirecting you to your payment provider</title>
      </head>
      <body>
        <strong>We are redirecting you to your payment provider</strong>

        <form action="https://api.ticketswitch.com/tickets/dummy_redirect.buy/demo-redirect" method="POST" id="calloutForm" name="calloutForm">
          <input type="hidden" name="return_url" value="https://fromtheboxoffice.com/callback/010288fe-a196-401f-8319-57bfe0cba552" />
          <input type="hidden" name="title" value="Dummy external card details page for debit on system 'ext_test1'" />
          <input type="submit" value="Click here to continue to your payment provider" />
        </form>

        <script language="javascript">
          document.getElementById('calloutForm').submit();
          document.getElementById('calloutButton').disabled = true;
        </script>
      </body>
    </html>

.. note:: the callout parameters are a :obj:`collections.OrderDict` and any url
          or form parameters should be passed to the destination in the given
          order.

If you loose the details of where you are supposed to be redirecting your
customer to to can retrieve it again with a :meth:`get_status
<pyticketswitch.client.Client.get_status>` call and find the details on the
:attr:`pending_callout <pyticketswitch.status.Status.pending_callout>`.

Handling Callbacks
==================

.. _handling_callbacks:

When the user has come back to your website from a third party payment
method, the third party should pass you some parameters that need to be passed
back to the API to complete the payment. 

For example if your callback URL looks something like this
``https://example.com/callback/<return_token>/`` and the payment provider
returns your customer to a URL like this
``https://example.com/callback/4e91a978-f7c6-4e38-b6c0-5167a1360398/?success=1&ref=abc123``
you need to pass those parameters back to us::
    
    >>> import uuid
    >>> from pyticketswitch import Client
    >>> client = Client('demo-redirect', 'demopass')
    >>> returned_parameters = {
    ...     'success': '1',
    ...     'ref': 'abc123',
    ... }
    ...
    >>> this_token = '4e91a978-f7c6-4e38-b6c0-5167a1360398'
    >>> next_token = uuid.uuid4()
    >>> status, callout, meta = client.next_callout(
    ...     this_token,
    ...     next_token,
    ...     returned_parameters,
    ... )
    ...
    >>> status.status
    'purchased'
    >>>

.. note:: :class:`next_callout <pyticketswitch.client.Client.next_callout>`
          may return another :class:`Callout <pyticketswitch.callout.Callout>`
          object.

.. warning:: the third party may try to return parameters to you via either a
             ``GET`` **OR** a ``POST`` request **OR** sometimes both (which is
             a clear violation of the HTTP spec but you know it's only the
             worlds largest payment provider, they probably don't know any
             better). As such you should make sure your callback URL responds
             to both ``GET`` and ``POST`` methods, and reads parameters from
             both the URL and the request body.

.. warning:: If your user gets lost and doesn't complete their transaction we
             will after a time attempt to clean up the transaction by
             returning to your return URL ourselves and returning no data. As
             such you should not assume things like cookies or sessions, or
             local storage, and you should be able to complete the callback
             withonly the data contained in the return url. If this is a
             problem for you let us know and we will see what we can do.


Setting tracking ID
=====================

.. _setting_tracking_id:

When instantiating Client object it's also possible to set optional tracking ID 
that will be set with each request performed by `make_request` method::

    >>> from pyticketswitch import Client
    >>> client = Client('example-user', 'some-password', tracking_id='xyz')
    >>> client.make_request('test.v1', {})

This is useful when using a common id for tracking requests across the 
whole infrastructure, and if set might prove helpful when debugging failing
queries.

Additionally it's also possible to set a tracking id not only
when instantiating the API Client but also using separate
tracking id each time a call is made.

If global tracking id is set when instantiating API client
it will be overwritten by per request tracking id

For example to set custom tracking id each time the `list_events`
method is called append `tracking_id` parameter as a kwarg.
    >>> from pyticketswitch import Client
    >>> client = Client('example-user', 'some-password')
    >>> client.list_events(tracking_id='123')


Frontend Integrations
=====================

.. _frontend_integrations:

For payment methods like stripe you will need some information ahead of
purchase time in order to capture payment details. The API provides the
:class:`Debitor <pyticketswitch.debitor.Debitor>` object for each bundle so
you can determine how you should be capturing these details::

    >>> from pyticketswitch import Client
    >>> client = Client('demo-stripe', 'demopass')
    >>> reservation, meta = client.make_reservation(
    ...     performance_id='7AB-4',
    ...     ticket_type_code='STALLS',
    ...     price_band_code='A/pool',
    ...     number_of_seats=2
    ... )
    >>> debitor = reservation.trolley.bundles[0].debitor
    >>> debitor
    <Debitor stripe:stripe>
    >>> debitor.description
    'Stripe Debitor'
    >>> debitor.type
    'stripe'
    >>> debitor.name
    'stripe'
    >>> debitor.integration_data
    {'publishable_key': 'pk_test_b7N9DOwbo4B9t6EqCf9jFzfa',
     'statement_descriptor': 'Test Stripe Account'}
    >>> 

You can then use the integration data to initialise a card details capture or
similar front end integration.

Events that don't need performance selection
============================================

.. _events_that_dont_need_performance_selection:

Some events available via the API don't require the customer to specify a
date/time on which they want to attend. For example a t-shirt might be
represented as an event on the API, but it doesn't need a performance, neither
does a season pass, nor a voucher.

This is indicated by the :attr:`Event.needs_performance
<pyticketswitch.event.Event.needs_performance>` flag::

    >>> from pyticketswitch import Client
    >>> client = Client('demo', 'demopass')
    >>> event, meta = client.get_event('7AA')
    >>> event.needs_performance
    True
    >>> event, meta = client.get_event('6KS')
    >>> event.needs_performance
    False
    >>> 

While the customer may not need to provide you with any additional
information, you still need to provide a valid performance id to a number of
calls such as :meth:`Client.get_availability
<pyticketswitch.client.Client.get_availability>`,
:meth:`Client.get_send_methods
<pyticketswitch.client.Client.get_send_methods>`, or
:meth:`Client.make_reservation
<pyticketswitch.client.Client.make_reservation>`.

You should still fetch this in the normal way via
:meth:`Client.list_performances
<pyticketswitch.client.Client.list_performances>`, however only one
:class:`Performance <pyticketswitch.performance.Performance>` will be
returned. Additionally :attr:`PerformanceMeta.auto_select
<pyticketswitch.performance.PerformanceMeta.auto_select>` should be set to
``True``, indicating that this performance should be automatically selected
for the customer::

    >>> from pyticketswitch import Client
    >>> client = Client('demo', 'demopass')
    >>> perfs, meta = client.list_performances('6KS')
    >>> perfs
    [<Performance 6KS-E3L>]
    >>> meta.auto_select
    True
    >>> 

.. warning:: Auto-generated performances change every day, you should be
             calling :meth:`Client.list_performances
             <pyticketswitch.client.Client.list_performances>` at least once a
             day in order to ensure you have the correct performance ID.

.. _`stripe`: https://stripe.com/gb
