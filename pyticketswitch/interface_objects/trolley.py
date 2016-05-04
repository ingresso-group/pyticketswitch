# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from pyticketswitch.util import resolve_boolean, to_int_or_none

from . import bundle as bundle_objs
from . import order as order_objs
from .base import InterfaceObject


class Trolley(InterfaceObject):
    """Object that represents a TSW trolley.

    Operations and information relating to a TSW order are available
    through this object, e.g. adding/removing orders, creating a reservation.
    An empty order can be created by calling the constructor with no arguments,
    otherwise the Id of the Trolley can be passed to access an existing TSW
    trolley.

    Args:
        trolley_id (string): Id of the Trolley
        settings (kwargs): See Core constructor.
    """

    def __init__(
        self,
        trolley_id=None,
        core_trolley=None,
        **settings
    ):
        self.trolley_id = trolley_id
        self._core_trolley_attr = core_trolley
        self._orders = None
        self._bundles = None

        super(Trolley, self).__init__(**settings)

    def add_order(self, order):
        """Add the Order object to this Trolley.

        Args:
            order (Order): The Order object to add.
        """
        crypto_block = self.get_crypto_block(
            method_name='start_session',
        )

        resp_dict = self.get_core_api().trolley_add_order(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            order_token=order.order_id,
            describe_trolley=True,
            trolley_token=self.trolley_id
        )

        self._set_crypto_block(
            crypto_block=resp_dict['crypto_block'],
            method_name='start_session'
        )

        self.trolley_id = resp_dict['trolley_token']
        self._core_trolley = resp_dict['trolley']

    @property
    def order_count(self):
        """Number of orders in this Trolley."""
        return to_int_or_none(
            self._core_trolley.trolley_order_count
        )

    @property
    def is_purchase_successful(self):
        """Check if the trolley was purchased successfully

        Will return True if the purchase was successful,
        False if the purchase was not successful and
        None if no purchase was attempted.
        """
        is_success = None

        if self._core_trolley.purchase_result:

            is_success = resolve_boolean(
                self._core_trolley.purchase_result.success
            )

        return is_success

    @property
    def purchase_failure_reason(self):
        """Reason for purchase failure, None if not attempted or successful."""
        reason = None

        if self.is_purchase_successful is False:
            reason = self._core_trolley.purchase_result.failure_reason

        return reason

    @property
    def purchase_error(self):
        """Error information for failed purchases."""
        purchase_error = None

        if self._core_trolley.purchase_error:
            purchase_error = self._core_trolley.purchase_error

        return purchase_error

    @property
    def _core_trolley(self):
        if self._core_trolley_attr is None:
            self.update()

        if self._core_trolley_attr:
            return self._core_trolley_attr
        else:
            return None

    @_core_trolley.setter
    def _core_trolley(self, value):
        if value is None:
            self._core_trolley_attr = False
        else:
            self._core_trolley_attr = value

        self.orders = None
        self.bundles = None

    def update(self):
        """Updates Trolley data.

        This method is used internally and it shouldn't be necessary
        to call it explicitly.
        """

        crypto_block = self.get_crypto_block(
            method_name='start_session'
        )

        resp_dict = self.get_core_api().trolley_describe(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            trolley_token=self.trolley_id
        )

        self._core_trolley = resp_dict['trolley']

    def remove_order(self, order_item_number):
        """Remove an Order from this Trolley.

        Args:
            order_item_number (int): The item number of the Order to remove.
        """
        crypto_block = self.get_crypto_block(
            method_name='start_session'
        )

        resp_dict = self.get_core_api().trolley_remove(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            trolley_token=self.trolley_id,
            remove_item=order_item_number,
            describe_trolley=True
        )

        self._set_crypto_block(
            crypto_block=resp_dict['crypto_block'],
            method_name='start_session'
        )

        self.trolley_id = resp_dict['trolley_token']
        self._core_trolley = resp_dict['trolley']

    def get_reservation(self):
        """Get a Reservation object for this Trolley.

        This method attempts to reserve the Trolley in the TSW system.

        Returns:
            Reservation: Reservation object for this Trolley.
        """
        from . import reservation as res_objs

        crypto_block = self.get_crypto_block(
            method_name='start_session'
        )

        resp_dict = self.get_core_api().make_reservation(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            trolley_token=self.trolley_id,
            self_print_mode='html',
            describe_trolley=True
        )

        if resp_dict['failed_orders']:
            failed_orders = []

            for failed_order in resp_dict['failed_orders']:
                failed_orders.append(
                    order_objs.Order(
                        order_id=failed_order.order_token,
                        core_order=failed_order,
                        **self._internal_settings()
                    )
                )

        else:
            failed_orders = None

        reservation = res_objs.Reservation(
            transaction_id=resp_dict['transaction_id'],
            minutes_left_float=resp_dict['minutes_left_on_reserve'],
            failed_orders=failed_orders,
            need_payment_card=resp_dict['need_payment_card'],
            acceptable_cards=resp_dict.get('acceptable_cards'),
            needs_email_address=resp_dict.get('needs_email_address'),
            supports_billing_address=resp_dict.get('supports_billing_address'),
            needs_agent_reference=resp_dict['needs_agent_reference'],
            prefilled_customer_data=resp_dict.get('prefilled_customer_data'),
            trolley_id=resp_dict['trolley_token'],
            core_trolley=resp_dict['trolley'],
            **self._internal_settings()
        )

        self._set_crypto_for_object(
            crypto_block=resp_dict['crypto_block'],
            method_name='make_reservation',
            interface_object=reservation
        )

        return reservation

    @property
    def orders(self):
        """List of Order objects in this Trolley."""
        if self._orders is None:

            orders = []

            for bundle in self.bundles:

                for order in bundle.orders:

                    orders.append(order)

                self._orders = orders

        return self._orders

    @orders.setter
    def orders(self, value):
        self._orders = value

    def _create_bundle(self, core_bundle):
        return bundle_objs.Bundle(
            core_bundle=core_bundle,
            **self._internal_settings()
        )

    @property
    def bundles(self):
        """List of Bundle objects in this Trolley."""
        if self._bundles is None:

            bundles = []

            for core_bundle in self._core_trolley.bundles:

                bundle = self._create_bundle(
                    core_bundle=core_bundle
                )

                bundles.append(bundle)

            self._bundles = bundles

        return self._bundles

    @bundles.setter
    def bundles(self, value):
        self._bundles = value

    @property
    def debitor_choices(self):

        debitor_choices = {
            debitor['debitor_name']: debitor
            for bundle in self.bundles
            for debitor in bundle._core_bundle.debitor_choices
        }

        return debitor_choices
