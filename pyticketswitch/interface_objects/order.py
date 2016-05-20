# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from pyticketswitch.util import (
    format_price_with_symbol, to_float_or_none, to_float_summed,
    to_int_or_return
)

from . import availability as availability
from . import event as event_objs
from . import performance as perf_objs
from .base import Commission, Currency, InterfaceObject, Seat


class Order(InterfaceObject):
    """Object that represents a TSW order.

    Information relating to a TSW order is accessible with this
    object, e.g. price information, seats, the event. Orders should
    be created with the Core.create_order method, the constructor is
    intended for internal use.
    """

    def __init__(
        self,
        order_id=None,
        core_order=None,
        core_currency=None,
        **settings
    ):
        self.order_id = order_id
        self._core_order = core_order
        self._core_currency = core_currency
        self._self_print_url = None
        self._self_print_relative_url = None
        self._requested_seats = False

        super(Order, self).__init__(**settings)

    @property
    def item_number(self):
        """Interger for identifying the order within the bundle."""
        return to_int_or_return(
            self._core_order.item_number
        )

    @property
    def self_print_url(self):
        if self._self_print_url:
            return self._self_print_url
        else:
            return None

    @self_print_url.setter
    def self_print_url(self, value):
        self._self_print_url = value

    @property
    def self_print_relative_url(self):
        if self._self_print_relative_url:
            return self._self_print_relative_url
        else:
            return None

    @self_print_relative_url.setter
    def self_print_relative_url(self, value):
        self._self_print_relative_url = value

    @property
    def event_desc(self):
        return self._core_order.event_desc

    @property
    def venue_desc(self):
        return self._core_order.venue_desc

    @property
    def total_combined_float(self):
        """Float value of the total combined price."""
        if self._core_order.total_combined:
            return to_float_or_none(
                self._core_order.total_combined
            )
        else:
            return to_float_summed(
                self._core_order.total_seatprice,
                self._core_order.total_surcharge
            )

    @property
    def total_combined(self):
        """Formatted string value of the total combined price with currency
        symbol.
        """
        return format_price_with_symbol(
            str(self.total_combined_float),
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

    @property
    def total_inc_despatch_float(self):
        """Float value of the total combined price including despatch."""
        total = self.total_combined_float
        if self.despatch_method and self.despatch_method.cost_float:
            total += self.despatch_method.cost_float

        return total

    @property
    def total_inc_despatch(self):
        """Formatted string value of the total combined price including
        despatch with currency symbol.
        """
        return format_price_with_symbol(
            str(self.total_inc_despatch_float),
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

    @property
    def currency(self):
        if self._core_currency:
            return Currency(
                core_currency=self._core_currency
            )

        return None

    @property
    def price_band_code(self):
        return self._core_order.price_band_code

    @property
    def average_price_per_ticket_float(self):
        return (
            self.total_combined_float /
            float(self._core_order.total_no_of_tickets)
        )

    @property
    def performance(self):
        """Performance object for this order."""
        if not hasattr(self, '_performance'):

            if self._core_order.performance:
                self._performance = perf_objs.Performance(
                    core_performance=self._core_order.performance,
                    **self._internal_settings()
                )

            else:
                self._performance = None

        return self._performance

    @property
    def event(self):
        """Event object for this order."""
        if not hasattr(self, '_event'):

            if self._core_order.event:

                self._event = event_objs.Event(
                    event_id=self._core_order.event.event_id,
                    core_event=self._core_order.event,
                    **self._internal_settings()
                )
            else:
                self._event = None

        return self._event

    @property
    def concessions(self):
        """List of Concession objects on this order."""
        if not hasattr(self, '_concessions'):

            self._concessions = []

            for discount in self._core_order.discounts:

                self._concessions.append(availability.Concession(
                    core_discount=discount,
                    core_currency=self._core_currency,
                    **self._internal_settings()
                ))

        return self._concessions

    @property
    def despatch_method(self):
        """DespatchMethod object for this order."""
        if not hasattr(self, '_despatch_method'):

            if self._core_order.despatch_method:

                self._despatch_method = availability.DespatchMethod(
                    core_despatch_method=self._core_order.despatch_method,
                    core_currency=self._core_currency,
                    **self._internal_settings()
                )

        return self._despatch_method

    @property
    def all_seats(self):
        """List of Seat objects on this order."""
        seats = []
        for con in self.concessions:
            seats = seats + con.seats

        return seats

    @property
    def all_seat_ids(self):
        """List of Seat Ids on this order."""
        return [s.seat_id for s in self.all_seats if s.seat_id]

    @property
    def ticket_type_desc(self):
        return self._core_order.ticket_type_desc

    @property
    def ticket_type_code(self):
        return self._core_order.ticket_type_code

    @property
    def backend_purchase_reference(self):
        """Supplier reference for this order."""
        return self._core_order.backend_purchase_reference

    @property
    def has_seat_with_restricted_view(self):
        """Boolean to indicate if any seats have restricted views."""
        restricted = False
        for con in self.concessions:
            if con.has_restricted_view:
                restricted = True

        return restricted

    @property
    def unique_seat_text(self):
        """List of unique seat text strings on this order."""
        seat_text = []
        for con in self.concessions:
            for text in con.unique_seat_text:
                if text not in seat_text:
                    seat_text.append(text)

        return seat_text

    @property
    def requested_seats(self):
        """If specific seats were requested, they will be listed here."""
        if self._requested_seats is False:
            if self._core_order.requested_seats:
                self._requested_seats = []

                for seat in self._core_order.requested_seats:
                    self._requested_seats.append(
                        Seat(core_seat=seat)
                    )
            else:
                self._requested_seats = None

        return self._requested_seats

    @property
    def requested_seat_ids(self):
        """List of requested Seat Ids on this order."""
        return [r.seat_id for r in self.requested_seats if r.seat_id]

    @property
    def seat_request_status(self):
        """Describes the status of the request for specific seats, i.e. were
        the specified seats successfully selected."""
        return self._core_order.seat_request_status

    @property
    def got_all_requested_seats(self):
        """Boolean indicating if the requested seats were successfully
        reserved.

        Returns True if all requested seats were reserved, False if some or
        none of the requested seats were reserved and None if no seats were
        requested.
        """
        if self.seat_request_status == 'not_requested':
            return None
        elif self.seat_request_status == 'got_all':
            return True
        return False

    @property
    def user_commission(self):
        """Returns Commission object representing the user commission for this
        order.
        """
        if self._core_order.user_commission:
            return Commission(
                core_commission=self._core_order.user_commission
            )
        return None

    @property
    def gross_commission(self):
        """Returns Commission object representing the gross commission for this
        order.
        """
        if self._core_order.gross_commission:
            return Commission(
                core_commission=self._core_order.gross_commission
            )
        return None
