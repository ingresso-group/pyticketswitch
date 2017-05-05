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
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.month.Month
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.performance.Performance
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.ticket_type.TicketType
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.price_band.PriceBand
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.discount.Discount
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.send_method.SendMethod
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.trolley.Trolley
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.reservation.Reservation
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.status.Status
   :members:
   :inherited-members:

Bundles and Orders
------------------

.. _bundles_and_orders_api:

Trolley objects, contain Bundle objects, which in turn contain Order objects,
which contain TicketOrder objects. These objects describe the products being
purchased and the current state of those purchases within the purchase process.

.. autoclass:: pyticketswitch.bundle.Bundle
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.order.Order
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.order.TicketOrder
   :members:
   :inherited-members:


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
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.cost_range.CostRange
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.cost_range.CostRangeDetails
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.offer.Offer
   :members:
   :inherited-members:

Event Details
-------------

.. _event_details_api:

These are additional details that are directly related to
:class:`Event <pyticketswitch.event.Event>`

.. autoclass:: pyticketswitch.card_type.CardType
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.field.Field
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.media.Media
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.review.Review
   :members:
   :inherited-members:

Seats
-----

.. _seats_api:

.. autoclass:: pyticketswitch.seat.SeatBlock
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.seat.Seat
   :members:
   :inherited-members:

Payment Details
---------------

.. _payment_details_api:

.. autoclass:: pyticketswitch.payment_methods.PaymentMethod
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.payment_methods.CardDetails
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.payment_methods.RedirectionDetails
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.payment_methods.StripeDetails
   :members:
   :inherited-members:


Callouts
--------
.. _callout_and_callbacks:

.. autoclass:: pyticketswitch.callout.Callout
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.callout.Integration
   :members:
   :inherited-members:

Meta Objects
------------
.. autoclass:: pyticketswitch.event.EventMeta
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.performance.PerformanceMeta
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.availability.AvailabilityMeta
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.currency.CurrencyMeta
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.performance.PerformanceMeta
   :members:
   :inherited-members:

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
    :special-members:
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
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.country.Country
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.user.User
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.customer.Customer
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.debitor.Debitor
   :members:
   :inherited-members:
.. autoclass:: pyticketswitch.card_type.CardType
   :members:
   :inherited-members:
