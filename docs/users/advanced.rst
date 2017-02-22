.. _advanced:

Advanced Guide
--------------

This guide provides additional information about parts of the wrapper that
expands on the :ref:`quick start guide <quickstart>`

Demo User Events
================

.. _demo_events:

At the time of writing this documentation the demo user has access to the
following events::

    2HJD Test Event - Type 1
    3CVA Test Event - Type 1
    3CVB Test Event - Type 10 (d)
    3CVD Test Event - Type 14 (e)
    3CVE Test Event - Type 15 (e)
    3CVF Test Event - Type 9
    3CVG Test Event - Type 13
    3P5L The Matt Allpress Fanclub!
    6IE Matthew Bourne's Swan Lake test
    6IF Matthew Bourne's Nutcracker TEST
    6KF V&A Memberships
    6KS 1-Day Ticket
    6KT 3-Day Hopper
    6KU Family Ticket
    6KV Individual Ticket
    6L9 La Femme
    9XW Five Day Park Hopper Ticket
    9XY Two day Parkhopper
    AG8 1デーパスポート (One Day Passport)
    DBZ Moulin Rouge (Dinner Show)
    DP9 Imperial Helicopter Tour
    DPB North Canyon Helicopter Tour
    GVA Souvenir DVD
    I3R MGM Grand Accomodation
    I3S Athenaeum
    I3T Corus Hyde Park
    I3U Hilton Kensington
    I3V St Ermin's

The three letter events (ie. 6IF, 9XW, DPB, GVA, etc) are fake events, their
responses are generated programatically, and they tend to exhibit a specific 
feature or oddity to simulate a feature of the API. The four letter events 
(i.e. 2HJD, 3CVA, 3P5L) are demonstration events tied to a real backend system
and allow us to simulate parts of our system that require more persistant data
such as individual seats and reporting.


Searching for an Event
======================

.. _event_search:

something something darkside


Pagination
==========

.. _pagination:

ALL THE PAGES BELONG TO US!

Requesting Seat Availability
============================

.. _seated_availability:

seats glorious seats

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
:meth:`Client.list_events <pyticketswitch.client.Client.list_events>`
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


Handling callouts
=================

.. _handling_callouts:


