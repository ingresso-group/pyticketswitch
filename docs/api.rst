.. _api:

Developer Interface
===================

.. module:: pyticketswitch

This part of the documentation covers all the interfaces of Pyticketswitch

Ticketswitch Client
-------------------

.. _client_api:

.. autoclass:: pyticketswitch.client.Client
   :inherited-members:

Core
----

.. _core_api:

The follow are the core business objects.

.. autoclass:: pyticketswitch.event.Event
.. autoclass:: pyticketswitch.month.Month
.. autoclass:: pyticketswitch.performance.Performance
.. autoclass:: pyticketswitch.ticket_type.TicketType
.. autoclass:: pyticketswitch.price_band.PriceBand
.. autoclass:: pyticketswitch.discount.Discount
.. autoclass:: pyticketswitch.send_method.SendMethod
.. autoclass:: pyticketswitch.trolley.Trolley
.. autoclass:: pyticketswitch.reservation.Reservation
.. autoclass:: pyticketswitch.status.Status

Bundles and Orders
------------------

.. _bundles_and_orders_api:

Trolley objects, contain Bundle objects, which in turn contain Order objects,
which contain TicketOrder objects. These objects describe the products being
purchased and the current state of those purchases within the purchase process.

.. autoclass:: pyticketswitch.bundle.Bundle
.. autoclass:: pyticketswitch.order.Order
.. autoclass:: pyticketswitch.order.TicketOrder


Pricing
-------

.. _pricing_api:

Any call that returns a price should also contain a description of the currency
that price is in. In some cases a :class:`Currency <pyticketswitch.currency.Currency>` object will be part
of the object containing the price, otherwise the :class:`Client <pyticketswitch.client.Client>` method
will return a :class:`CurrencyMeta <pyticketswitch.currency.CurrencyMeta>` object that describes the currency
for the whole response.

:class:`Event <pyticketswitch.event.Event>` and 
:class:`Performance <pyticketswitch.performance.Performance>` 
can provide estimates on the prices available ahead of actually calling
:func:`Client.get_availability() <pyticketswitch.client.Client.get_availability>`.
These results will be generated from cached data and should not be considered
100% accurate.

.. autoclass:: pyticketswitch.currency.Currency
.. autoclass:: pyticketswitch.cost_range.CostRange
.. autoclass:: pyticketswitch.cost_range.CostRangeDetails
.. autoclass:: pyticketswitch.offer.Offer

Event Details
-------------

.. _event_details_api:

These are additional details that are directly related to
:class:`Event <pyticketswitch.event.Event>`

.. autoclass:: pyticketswitch.content.Content
.. autoclass:: pyticketswitch.field.Field
.. autoclass:: pyticketswitch.media.Media
.. autoclass:: pyticketswitch.review.Review

Seats
-----

.. _seats_api:

.. autoclass:: pyticketswitch.seat.SeatBlock
.. autoclass:: pyticketswitch.seat.Seat

Meta Objects
------------
.. autoclass:: pyticketswitch.availability.AvailabilityMeta
.. autoclass:: pyticketswitch.currency.CurrencyMeta
.. autoclass:: pyticketswitch.performance.PerformanceMeta



Utilities
---------

.. _utils_api:

.. automodule:: pyticketswitch.utils
    :members:
    :undoc-members:


Mixins
------

.. _mixins_api:

.. automodule:: pyticketswitch.mixins
    :members:
    :undoc-members:

Exceptions
----------

.. _exceptions_api:

.. automodule:: pyticketswitch.exceptions
    :members:
    :undoc-members:

Miscellaneous
-------------

.. _misc_api:

.. autoclass:: pyticketswitch.address.Address
.. autoclass:: pyticketswitch.country.Country
.. autoclass:: pyticketswitch.user.User
