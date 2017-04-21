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

+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| id  | description                                       | additional attributes                                                                                                                         |
+=====+===================================================+===============================================================================================================================================+
| 6IE | Matthew Bourne's Swan Lake test                   | - seated                                                                                                                                      |
|     |                                                   | - default discounts only                                                                                                                      |
|     |                                                   | - reservations for tuesday performances                                                                                                       |
|     |                                                   | - has restricted view seats on ticket 2 and 3 on thursdays                                                                                    |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| 6IF | Matthew Bourne's Nutcracker TEST                  | - seated                                                                                                                                      |
|     |                                                   | - maximum of 3 mixed discounts                                                                                                                |
|     |                                                   | - no availability on Saturday nights                                                                                                          |
|     |                                                   | - no discounts in the stalls on the 1st of the month                                                                                          |
|     |                                                   | - no OPA or STUDENT discounts in price band B                                                                                                 |
|     |                                                   | - collect from the venue and post dispatch methods available                                                                                  |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| 6KF | V&A Memberships                                   | - subscription                                                                                                                                |
|     |                                                   | - has only single performance that must be selected                                                                                           |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| 6KS | 1-Day Ticket                                      | - attraction                                                                                                                                  |
| 6KT | 3-Day Hopper                                      | - not valid on mondays                                                                                                                        |
| 6KU | Family Ticket                                     |                                                                                                                                               |
| 6KV | Individual Ticket                                 |                                                                                                                                               |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| 6L9 | La Femme                                          | - seated                                                                                                                                      |
|     |                                                   | - blanket discounts                                                                                                                           |
|     |                                                   | - special offer                                                                                                                               |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| 7AA | Toy Story - The Opera                             | - seated                                                                                                                                      |
|     |                                                   | - seat selection                                                                                                                              |
|     |                                                   | - seating plan data available                                                                                                                 |
|     |                                                   | - contiguous seat selection only                                                                                                              |
|     |                                                   | - cannot leave single seats                                                                                                                   |
|     |                                                   | - self print vouchers                                                                                                                         |
|     |                                                   | - reservations including seat H10 will always fail                                                                                            |
|     |                                                   | - reservations including seat D7 will return a different seat selection from the same block of seats (as if that seat had become unavailable) |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| 7AB | The Unremarkable Incident of the Cat at Lunchtime | - seated                                                                                                                                      |
|     |                                                   | - seat selection                                                                                                                              |
|     |                                                   | - seating plan data available                                                                                                                 |
|     |                                                   | - allows discontiguous seat selection                                                                                                         |
|     |                                                   | - self print vouchers with barcodes                                                                                                           |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| 9XW | Five Day Park Hopper Ticket                       | - attraction                                                                                                                                  |
| 9XY | Two day Parkhopper                                | - is post only (can be used to generate ‘no sends’ if you select a performance date within the next few days)                                 |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| AG8 | 1デーパスポート (One Day Passport)                | - attraction                                                                                                                                  |
|     |                                                   | - text in japanese (useful for testing unicode support)                                                                                       |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| DBZ | Moulin Rouge (Dinner Show)                        | - seated                                                                                                                                      |
|     |                                                   | - priced in euros                                                                                                                             |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| DP9 | Imperial Helicopter Tour                          | - tour                                                                                                                                        |
| DPB | North Canyon Helicopter Tour                      | - many performances (useful for testing pagination, calendars, etc)                                                                           |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| GVA | Souvenir DVD                                      | - merchandise                                                                                                                                 |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| I3R | MGM Grand Accomodation                            | - hotel                                                                                                                                       |
| I3S | Athenaeum                                         |                                                                                                                                               |
| I3T | Corus Hyde Park                                   |                                                                                                                                               |
| I3U | Hilton Kensington                                 |                                                                                                                                               |
| I3V | St Ermin's                                        |                                                                                                                                               |
+-----+---------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+


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


