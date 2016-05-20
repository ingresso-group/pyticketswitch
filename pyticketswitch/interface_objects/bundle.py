# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from pyticketswitch.util import (
    format_price_with_symbol, resolve_boolean, to_float_or_none,
    to_int_or_none, to_int_or_return
)

from . import order as order_objs
from .base import InterfaceObject


class Bundle(InterfaceObject):
    """Object that represents a TSW bundle.

    A TSW bundle is a collection of orders for a particular supplier,
    so Trolleys are made up of Bundles containing Orders. Information
    about a TSW bundle is available with this object. Bundle objects
    should always be accessed from a Trolley/Reservation object, the
    constructor is intended for internal use only.
    """

    def __init__(
        self,
        core_bundle,
        self_print_urls=None,
        **settings
    ):
        self._core_bundle = core_bundle
        self._orders = None
        self._self_print_urls = self_print_urls

        super(Bundle, self).__init__(**settings)

    @property
    def source_description(self):
        """Supplier name."""
        return self._core_bundle.bundle_source_desc

    @property
    def source_code(self):
        """Supplier code."""
        return self._core_bundle.bundle_source_code

    @property
    def order_count(self):
        """Number of orders in this Bundle."""
        return to_int_or_none(
            self._core_bundle.bundle_order_count
        )

    @property
    def total_seatprice(self):
        """Formatted string value of the total seat price with currency
        symbol."""
        return format_price_with_symbol(
            self._core_bundle.bundle_total_seatprice,
            self._core_bundle.currency.currency_pre_symbol,
            self._core_bundle.currency.currency_post_symbol
        )

    @property
    def total_surcharge(self):
        """Formatted string value of the total surcharge cost with currency
        symbol."""
        return format_price_with_symbol(
            self._core_bundle.bundle_total_surcharge,
            self._core_bundle.currency.currency_pre_symbol,
            self._core_bundle.currency.currency_post_symbol
        )

    @property
    def total_despatch(self):
        """Formatted string value of the total despatch cost with currency
        symbol."""
        return format_price_with_symbol(
            self._core_bundle.bundle_total_despatch,
            self._core_bundle.currency.currency_pre_symbol,
            self._core_bundle.currency.currency_post_symbol
        )

    @property
    def total_cost(self):
        """Formatted string value of the total combined price with currency
        symbol."""
        return format_price_with_symbol(
            self._core_bundle.bundle_total_cost,
            self._core_bundle.currency.currency_pre_symbol,
            self._core_bundle.currency.currency_post_symbol
        )

    @property
    def total_cost_float(self):
        """Float value of the total combined price."""
        return to_float_or_none(
            self._core_bundle.bundle_total_cost
        )

    @property
    def orders(self):
        """List of Order objects in this Bundle."""
        if self._orders is None:
            orders = []

            for core_order in self._core_bundle.orders:

                currency = (
                    core_order.currency or
                    self._core_bundle.currency or
                    None
                )

                order = order_objs.Order(
                    core_order=core_order,
                    core_currency=currency,
                    **self._internal_settings()
                )

                if self._self_print_urls:
                    for s in self._self_print_urls:

                        if to_int_or_return(
                            s.item_number
                        ) == order.item_number:

                            order.self_print_url = s.complete_page_url
                            order.self_print_relative_url = s.page_url

                orders.append(order)

            self._orders = orders

        return self._orders

    @property
    def is_purchase_successful(self):
        """Boolean indicating if the bundle was purchased successfully

        Will return True if the purchase was successful,
        False if the purchase was not successful and
        None if no purchase was attempted.
        """
        is_success = None

        if self._core_bundle.purchase_result:

            is_success = resolve_boolean(
                self._core_bundle.purchase_result.success
            )

        return is_success

    @property
    def purchase_failure_reason(self):
        """Reason why purchase failed, None if not attempted."""
        reason = None

        if self.is_purchase_successful is False:
            reason = self._core_bundle.purchase_result.failure_reason

        return reason
