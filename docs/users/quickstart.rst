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
(for example by closing your terminal), just instantiate a new one and continue 
where you left off. The client holds no relevant state other than the
authentication credentials.


Finding Events
==============

The top level object exposed by the API is the 
:class:`Event <pyticketswitch.event.Event>` object and the primary way of 
finding events is 
:func:`list_events() <pyticketswitch.client.Client.list_events()>`::

    >>> events, meta = client.list_events()
    >>> events
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
    
    >>> performances, meta = client.list_performances('6IF')
    >>> performances
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
:class:`Performance <pyticketswitch.performance.Performance>`, we need to find
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
    [<PriceBand A/pool>, <PriceBand B/pool>, <PriceBand C/pool>]
    >>> price_band = ticket_type.price_bands[0]
    >>> discount = price_band.default_discount
    >>> discount
    <Discount ADULT:Adult standard>
    >>> discount.combined_price()
    35.0
    >>> discount.availability
    6

The combined price is made up of the seatprice (or the facevalue) 
and the surcharge (or booking fee) of a ticket. 

The discount also indicates the number of available tickets in this price band.

The meta object contains aggregate information relevant to the ticket types and
their children. For example it contains information on the currency the tickets
are priced in and what are valid quantities available::
    
    >>> meta.valid_quantities
    [2, 3, 4, 5]
    >>> meta.currency
    <Currency gbp>

Our event is seated but we are unable to reserve individual seats. However some
events do allow this, see 
:ref:`requesting seat availability <seated_availability>` for more information.

For now all we need to continue is a 
:attr:`TicketType.code <pyticketswitch.ticket_type.TicketType.code>`
and a
:attr:`PriceBand.code <pyticketswitch.price_band.PriceBand.code>` so pick one 
of each.

Discounts
=========

Tickets often have a range of discounts that can be applied to them. Usually
these represent a concession that can be applied to a ticket. For example, the
ticket might have reduced prices for children or students::

    >>> discounts, meta = client.get_discounts(
    ...     '6IF-B1H',
    ...     ticket_type.code,
    ...     price_band.code
    ... )
    ...
    >>> discounts
    [<Discount ADULT:Adult standard>,
     <Discount CHILD:Child rate>,
     <Discount STUDENT:Student rate>,
     <Discount OAP:Senior citizen rate>]

.. note:: The default discount for a price band is usually the most expensive
          option and can be considered to be the standard price of the ticket
          inside a price band.

Each discount has the explicit price of the ticket when applied to it's parent 
price band::

    >>> for discount in discounts:
    ...     print(discount.code, discount.combined_price())
    ...     
    ... 
    ADULT 35.0
    CHILD 18.0
    STUDENT 26.0
    OAP 28.0

In addition to the available discounts The 
:func:`get_discounts() <pyticketswitch.client.Client.get_discounts>` call
will return a 
:class:`meta object <pyticketswitch.currency.CurrencyMeta>` that will contain 
information about the currency of the prices contained in the discounts 
response.

Keep the list of discounts around or make a note of the 
:attr:`Discount.code <pyticketswitch.discount.Discount.code>` for adults and 
children (we will need when it comes to making a reservation).


Send Methods
============

After purchasing tickets there are often multiple ways for customers to receive
their tickets, and these may have additional costs associated with them. We
refer to this as a :class:`SendMethod <pyticketswitch.send_method.SendMethod>`.

For example an E-Ticket might be free but posting the ticket in the mail might
have an associated charge::

    >>> send_methods, meta = client.get_send_methods('6IF-B1H')
    >>> send_methods
    [<SendMethod COBO:Collect from the venue>,
     <SendMethod POST:Post (UK & Ireland only)>]
    >>> for send_method in send_methods:
    ...     print(send_method.code, send_method.cost)
    ...     
    ... 
    COBO 1.5
    POST 3.5

.. warning:: It's important to check send methods before attempting a
             reservation as certain send methods might become unavailable as
             one gets closer to the performance date. For example it might take
             up to five working days to ship a physical ticket internationally
             so that send method would not be available with 2 days to go
             before a performance as the ticket would not get to it's 
             destination in time.

Some tickets may have restrictions on what countries they are available to::

    >>> send_methods[1].description
    'Post (UK & Ireland only)'
    >>> send_methods[1].permitted_countries
    [<Country ie:Ireland>, <Country uk:United Kingdom>]

.. note:: Send methods with additional costs apply to the whole order not
          indivual tickets. For example purchasing five tickets to the same
          show will cost the same to post as purchasing one ticket. Tickets for
          seperate shows by different suppliers may incur multiple send method
          costs; see 
          :ref:`Trollies, Bundles, Orders, and Ticket Orders <trollies_bundles_orders_ticket_orders>`
          for more information.

In addition to the available send methods The 
:func:`get_send_methods() <pyticketswitch.client.Client.get_send_methods>` call
will return a 
:class:`meta object <pyticketswitch.currency.CurrencyMeta>` that will contain 
information about the currency of the prices contained in the send methods 
response.

We now have all the information we need to make a reservation; the ticket type,
price band, discount, and a 
:attr:`SendMethod.code <pyticketswitch.send_method.SendMethod.code>`!


Making a Reservation
====================

Before making a purchase we have to reserve the tickets. Ingresso is often not
the only agent connected to a ticketing system and you are almost certainly
not the only user these tickets are available to. As such it's important to put
a lock on the tickets your customer is interested in so that they are not
snaffled up by some other customer.

For this example we are going to attempt to reserve 3 tickets (two adults and
one child) for ``6IF-B1H``. To do this we make a reservation providing the
information that we gained from the previous performance, availability,
discounts and send method calls::

    >>> performance.id
    '6IF-B1H'
    >>> ticket_type.code
    'CIRCLE'
    >>> price_band.code
    'A/pool'
    >>> adult, child, *_ = discounts
    >>> adult.code
    'ADULT'
    >>> child.code
    'CHILD'
    >>> reservation, meta = client.make_reservation(
    ...     performance_id=performance.id,
    ...     ticket_type_code=ticket_type.code,
    ...     price_band_code=price_band.code,
    ...     number_of_seats=3,
    ...     discounts=[
    ...         adult.code,
    ...         adult.code,
    ...         child.code
    ...     ]
    ... )
    ...

Was the reservation successful? The returned reservation object contains a 
:class:`Trolley object <pyticketswitch.trolley.Trolley>` that will give 
us some information::

    >>> trolley = reservation.trolley
    >>> trolley
    <Trolley uuid:ee39656e-ecc9-11e6-87c4-0025903268a0>

The trolley object contains three important bits of information.

The presence of a 
:attr:`transaction_uuid <pyticketswitch.trolley.Trolley.transaction_uuid>` lets
us know that we were at least somewhat successful in our reservation attempt.
It's a unique identifier that will allow us to get the status of our
reservation/transaction going forwards::

    >>> transaction_uuid = trolley.transaction_uuid
    'ee39656e-ecc9-11e6-87c4-0025903268a0'


Although we have put a lock on these tickets this lock will not last forever
before it's released and become available for someone else to purchase.
As such it's import to check how long we have to make a purchase before our
reservation expires::

    >>> trolley.minutes_left
    13.2

.. note:: This time varies across systems, events and performances, so be sure
          check this after making a reservation and ensure you make your 
          customer aware that they are on the clock.

Lastly our trolley object will contain some 
:class:`Bundles <pyticketswitch.bundle.Bundle>`. 
:class:`Bundles <pyticketswitch.bundle.Bundle>` group our orders by the 
ticketing system they are being made into::

    >>> trolley.bundles
    [<Bundle ext_test0>]
    >>> bundle = trolley.bundles[0]

As we are making a single order from a single system we don't care overly much
about bundles, all we really need to know is that it contains the currency,
total price, and more detailed information of our order::

    >>> bundle.currency
    <Currency gbp>
    >>> bundle.total
    89.5
    >>> bundle.orders
    [<Order 1>]

So what did we actually reserve? lets inspect the 
:class:`Order <pyticketswitch.order.Order>`::

    >>> order = bundle.orders[0]
    >>> order.event.id
    '6IF'
    >>> order.performance.id
    '6IF-B1H'
    >>> order.ticket_type_code
    'CIRCLE'
    >>> order.price_band_code
    'A/pool'
    >>> order.number_of_seats
    3

Excellent we got the all the stuff we asked for! But wait there's more! Our 
event is seated so we should have been allocated the specific seat that we will
be purchasing::
    
    >>> order.get_seats()
    [<Seat ZT149>, <Seat ZT148>, <Seat ZT147>]

This is just a simple reservation, but the system can handle much more complex
orders to multiple systems, in multiple currencies, and to multiple events and 
performances. If you are interested in package deals or up-selling then you
should probably take a look at :ref:`Basketing <basketing>`.

.. note:: We have glossed over a lot of information contained in the above 
          objects with the aim of getting you purchasing quickly, if you want
          more information then have a read of 
          :ref:`Trollies, Bundles, Orders, and Ticket orders <trollies_bundles_orders_ticket_orders>` .

The only thing we need to carry on to the next steps is the 
:attr:`transaction_uuid <pyticketswitch.trolley.Trolley.transaction_uuid>` that
identifies our reservation, so make a note of it.


Making a Purchase
=================

The final step in the transaction process is actually give us money and for us
to tell the supplier to put a hold on the requested tickets permanently.

There are a number of different payment methods available but for the time 
being we will focus on the most common; *credit*. This where we take nothing
from you at the time of purchase and invoice you at a later date for the amount
you owe! This also happens to be the simplest payment method.

.. note:: There are other payment methods that you might come across. So it's a
          good idea to read :ref:`Taking payments <taking_payments>` before 
          going live.

Before we can continue we need to gather some information about the customer
that we are selling to::

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
    ...)

The required fields are 
the customers :attr:`first <pyticketswitch.customer.Customer.first_name>` and
:attr:`last <pyticketswitch.customer.Customer.last_name>` name,
at least one line of a  
:attr:`postal address <pyticketswitch.customer.Customer.address_lines>`,
the :attr:`country code <pyticketswitch.customer.Customer.address_lines>` for 
the postal address,
a contact :attr:`phone number <pyticketswitch.customer.Customer.address_lines>`
and unless otherwise specified by the 
:attr:`Reservation.needs_email_address <pyticketswitch.reservation.Reservation.needs_email_address>`
field a :attr:`valid email address <pyticketswitch.customer.Customer.email>`.

You may provide additional information about the customer as you see fit, but 
the more information we have the easier it will be for us or the venue to 
contact them in case of a problem, and it also allows us to protect both you
and us from fraudulent transactions. `Here is our privacy policy`_. 

You can also specify who we can send this information to with the 
:attr:`supplier_can_use_data <pyticketswitch.customer.Customer.supplier_can_use_data>` 
(generally recommened),
:attr:`user_can_use_data <pyticketswitch.customer.Customer.supplier_can_use_data>` 
(this is your organisation, for example in reporting, or by email),
:attr:`world_can_use_data <pyticketswitch.customer.Customer.supplier_can_use_data>`
(in my opinion this should always be off), flags.

.. _`Here is our privacy policy`: https://ingresso.co.uk/privacy_policy

With our customer object in hand we can now make the purchase::

    >>> status, callback = client.make_purchase(
    ...     transaction_uuid,
    ...     customer,
    ...)

For the time being we can can ignore the callback, just check that we don't 
have one::

    >>> assert not callback


Assuming no errors were raised, that's it! Your tickets are booked!

The status object should contain information about your purchase::

    >>> status.status
    'purchased'
    >>> status.trolley.transaction_id
    'T000-0000-8MU2-Z5E4'
    >>> status.trolley.bundles[0].total
    118.5
    >>> status.trolley.bundles[0].orders[0].backend_purchase_reference
    'PURCHASE-17461-1'
    >>> status.trolley.bundles[0].orders[0].get_seats()
    [<Seat GB506>, <Seat GB505>, <Seat GB504>]


Retrieving Transactions
=======================

If at any point in the process you need to retrieve the status of a transaction
or reservation you can do so using the :meth:`Client.get_status
<pyticketswitch.client.Client.get_status>` call and the **transaction_uuid**::

    >>> status, meta = client.get_status('ee39656e-ecc9-11e6-87c4-0025903268a0')
    >>> status.status
    'purchased'


-----------------------

Ready for more? Check out the :ref:`advanced <advanced>` section.
