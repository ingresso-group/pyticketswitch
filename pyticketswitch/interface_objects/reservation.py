# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from pyticketswitch.util import (
    boolean_to_yes_no, dict_ignore_nones, resolve_boolean, to_float_or_zero
)

from . import bundle as bundle_objs
from . import trolley as trolley_objs
from .base import Customer


class Reservation(trolley_objs.Trolley):
    """Object that represents a reserved TSW trolley.

    In TSW, a reservation is not really a separate element to a trolley,
    but they have some different behaviour and attributes, so in this
    library they have been separated to avoid confusuon. The Reservation
    object is a sub class of the Trolley object.

    Operations and information relating to reservations are accessible
    through this object, e.g. making purchases, reservation details,
    cancelling a reservation. Can be constructed with a transaction Id (
    other constructor arguments are for internal use).

    Args:
        transaction_id (string): Id of the TSW transaction.
        settings (kwargs): See Core constructor.
    """

    def __init__(
        self,
        transaction_id=None,
        minutes_left_float=None,
        failed_orders=None,
        need_payment_card=None,
        acceptable_cards=None,
        needs_email_address=None,
        supports_billing_address=None,
        needs_agent_reference=None,
        prefilled_customer_data=None,
        trolley_id=None,
        core_trolley=None,
        **settings
    ):
        self.transaction_id = transaction_id
        self._minutes_left = None
        self._seconds_left = None
        if minutes_left_float:
            self._set_time_left(minutes_left_float)
        if failed_orders is None:
            failed_orders = []
        self.failed_orders = failed_orders
        self._need_payment_card = need_payment_card
        self._needs_email_address = needs_email_address
        self._supports_billing_address = supports_billing_address
        self._needs_agent_reference = needs_agent_reference
        if prefilled_customer_data is None:
            prefilled_customer_data = {}
        self.prefilled_customer_data = prefilled_customer_data
        self._transaction_status = None
        self._remote_site = None
        self._customer = None
        self._confirmation_page_html = None
        self._self_print_urls = None

        self.acceptable_cards = []

        if acceptable_cards is not None:
            if isinstance(acceptable_cards, dict):
                # The can be changed if _get_acceptable_cards in
                # booking.views is removed
                if isinstance(acceptable_cards['card'], list):
                    # Dealing with acceptable cards created by
                    # _get_acceptable_cards
                    for c in acceptable_cards['card']:

                        self.acceptable_cards.append({
                            'card_type': c['card_type'],
                            'card_desc': c['card_desc']
                        })

                elif isinstance(acceptable_cards['card'], dict):
                    # Dealing with acceptable cards from parse
                    self.acceptable_cards.append({
                        'type': acceptable_cards['card']['card_type'],
                        'description': acceptable_cards['card']['card_desc']
                    })
            else:
                self.acceptable_cards = acceptable_cards

        super(Reservation, self).__init__(
            trolley_id=trolley_id,
            core_trolley=core_trolley,
            **settings
        )

    def _get_cache_key(self):
        return self.transaction_id

    @property
    def _core_trolley(self):
        if self._core_trolley_attr is None:
            self.get_details()

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

    @property
    def minutes_left(self):
        """Interger number of minutes this reservation is still valid."""
        if self._minutes_left is None:
            self.get_details()

        if self._minutes_left is False:
            return None
        else:
            return self._minutes_left

    @minutes_left.setter
    def minutes_left(self, value):
        if value is None:
            self._minutes_left = False
        else:
            self._minutes_left = value

    @property
    def seconds_left(self):
        """Interger number of seconds in addition to 'minutes_left' that
        this reservation is still valid.
        """
        if self._seconds_left is None:
            self.get_details()

        if self._seconds_left is False:
            return None
        else:
            return self._seconds_left

    @seconds_left.setter
    def seconds_left(self, value):
        if value is None:
            self._seconds_left = False
        else:
            self._seconds_left = value

    def _set_time_left(self, minutes_left_string):

        self.minutes_left = None
        self.seconds_left = None

        if minutes_left_string is not None:
            minutes_float = to_float_or_zero(minutes_left_string)

            if minutes_float > 0:
                self.minutes_left = int(minutes_float)
                self.seconds_left = int(
                    (minutes_float - self.minutes_left) * 60
                )

            else:
                self.minutes_left = 0
                self.seconds_left = 0

    def delete(self):
        """Cancels this reservation, returns True if successful."""

        crypto_block = self._get_crypto_block_for_object(
            method_name='make_reservation',
            interface_object=self
        )

        resp_dict = self.get_core_api().release_reservation(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
        )

        return resolve_boolean(
            resp_dict['released_ok']
        )

    def purchase_part_one(
        self, return_token, return_domain, return_path,
        return_with_https, encryption_key, customer=None,
        card=None
    ):
        """First part of the 2 stage purchase process.

        See the XML API documentation for more information about the
        purchase process.

        Args:
            return_token (string): Unique token for this purchase call.
            return_domain (string): The domain for the return URL.
            return_path (string): The path for the return URL.
            return_with_https (boolean): Indicates whether the URL should use
                HTTP or HTTPS.
            encryption_key (string): Encryption key for data.
            customer (Customer): Optional, Customer object representing the
                customer making the purchase.
            card (Card): Optional, Card object representing the payment
                card information.

        Returns:
            Dictionary: A dictionary containing an item called
                'redirect_html_page_data' with a string value of
                HTML that should be passed to the user's browser
                in order to perform the redirect.
        """

        if card:
            card_data = dict_ignore_nones(**card._get_dict())
        else:
            card_data = None

        if customer:
            customer_data = dict_ignore_nones(**customer._get_dict())
        else:
            customer_data = None

        https_string = boolean_to_yes_no(
            return_with_https
        )

        crypto_block = self._get_crypto_block_for_object(
            method_name='make_reservation',
            interface_object=self
        )

        resp_dict = self.get_core_api().purchase_reservation_part_one(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            customer_data=customer_data,
            return_token=return_token, return_domain=return_domain,
            return_path=return_path, return_with_https=https_string,
            encryption_key=encryption_key, card_data=card_data,
        )

        return resp_dict

    def purchase_part_two(
        self, returning_token, new_return_token, new_return_path, http_referer,
        http_accept, http_user_agent, callback_data, encryption_key,
        send_confirmation_email=None, results_url=None
    ):
        """Second part of the 2 stage purchase process.

        See the XML API documentation for more information about the
        purchase process.

        Args:
            returning_token (string): The return token from part one.
            new_return_token (string): A new unique token for this call.
            new_return_path (string): The path for the return URL.
            http_referer (string): The user's 'Referer' HTTP header.
            http_accept (string): The user's 'Accept' HTTP header.
            http_user_agent (string): The user's 'User-Agent' HTTP header.
            callback_data (dictionary): All POST and GET variables.
            encryption_key (string): Encryption key for data.
            send_confirmation_email (boolean): Optional, boolean indicating
                whether TSW should send a confirmation email or not.
            results_url (string): Optional, URL of the confirmation page.

        Returns:
            Dictionary: If an additional redirect is required, then the
                dictionary will contain an item called
                'redirect_html_page_data' which is the same as described in
                part one. This redirect must be followed to complete the
                purchase.
        """

        crypto_block = self.get_crypto_block(
            method_name='start_session',
            password_required=False
        )

        resp_dict = self.get_core_api().purchase_reservation_part_two(
            returning_token=returning_token, new_return_token=new_return_token,
            new_return_path=new_return_path, http_referer=http_referer,
            http_accept=http_accept, http_user_agent=http_user_agent,
            callback_data=callback_data, encryption_key=encryption_key,
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            send_confirmation_email=send_confirmation_email,
            results_url=results_url,
        )

        if 'trolley' in resp_dict:
            self.transaction_id = resp_dict['trolley'].transaction_id
            self._core_trolley = resp_dict['trolley']

        if 'trolley_token' in resp_dict:
            self.trolley_id = resp_dict['trolley_token']

        if 'customer' in resp_dict:
            customer = Customer(
                core_customer=resp_dict['customer']
            )

            resp_dict['customer'] = customer
            self.customer = customer
        else:
            self.customer = None

        if 'self_print_html_pages' in resp_dict:
            self.self_print_urls = resp_dict['self_print_html_pages']

        return resp_dict

    def purchase_reservation(
        self, customer=None, send_confirmation_email=None,
    ):
        """A one stage purchase process that should only be used for purchases
        made on credit.

        See the XML API documentation for more information about the
        purchase process. Note the absence of a 'card_data' element
        in the input - this is intentional since the 2-stage purchase process
        (calling purchase_part_one & purchase_part_two) should always be used
        whenever a payment method is required.

        Args:
            customer (Customer): Optional, Customer object representing the
                customer making the purchase.
            send_confirmation_email (boolean): Optional, boolean indicating
                whether TSW should send a confirmation email or not.

        Returns:
            Dictionary: The result of the attempted purchase
        """

        if customer:
            customer_data = dict_ignore_nones(**customer._get_dict())
        else:
            customer_data = None

        crypto_block = self._get_crypto_block_for_object(
            method_name='make_reservation',
            interface_object=self
        )

        resp_dict = self.get_core_api().purchase_reservation(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            customer_data=customer_data,
            send_confirmation_email=send_confirmation_email,
        )

        return resp_dict

    @property
    def transaction_status(self):
        """Status of the reservation."""
        if self._transaction_status is None:
            self.get_details()

        if self._transaction_status:
            return self._transaction_status
        else:
            return None

    @transaction_status.setter
    def transaction_status(self, value):
        if value is None:
            self._transaction_status = False
        else:
            self._transaction_status = value

    @property
    def remote_site(self):
        """The domain that the transaction was made on."""
        if self._remote_site is None:
            self.get_details()

        if self._remote_site:
            return self._remote_site
        else:
            return None

    @remote_site.setter
    def remote_site(self, value):
        if value is None:
            self._remote_site = False
        else:
            self._remote_site = value

    @property
    def customer(self):
        """Customer object representing the customer on the reservation."""
        if self._customer is None:
            self.get_details()

        if self._customer:
            return self._customer
        else:
            return None

    @customer.setter
    def customer(self, value):
        if value is None:
            self._customer = False
        else:
            self._customer = value

    @property
    def confirmation_page_html(self):
        """HTML of the confirmation page, if it was stored."""
        if self._confirmation_page_html is None:
            self.get_details()

        if self._confirmation_page_html:
            return self._confirmation_page_html
        else:
            return None

    @confirmation_page_html.setter
    def confirmation_page_html(self, value):
        if value is None:
            self._confirmation_page_html = False
        else:
            self._confirmation_page_html = value

    def get_details(self):
        """Retrieves information about the reservation.

        Called internally by several methods/properties, it shouldn't
        be necessary to call this method explicitly.

        Returns:
            Reservation: Self, with updated data.
        """
        crypto_block = self.get_crypto_block(
            method_name='start_session',
            password_required=False
        )

        resp_dict = self.get_core_api().transaction_info(
            transaction_id=self.transaction_id, describe_trolley=True,
            describe_customer=True, describe_external_sale_page=True,
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
        )

        self.transaction_status = resp_dict['transaction_status']
        self._set_time_left(resp_dict['minutes_left_on_reserve'])
        self.remote_site = resp_dict['remote_site']

        self._core_trolley = resp_dict['trolley']

        if 'customer' in resp_dict:

            lang_str = resp_dict.get('language_list', None)

            if lang_str:
                langs = lang_str.split(',')

            self.customer = Customer(
                core_customer=resp_dict['customer'],
                languages=langs,
            )

        else:
            self.customer = None

        if 'sale_page' in resp_dict:
            self.confirmation_page_html = resp_dict['sale_page'].sale_page
        else:
            self.confirmation_page_html = None

        if 'self_print_html_pages' in resp_dict:
            self.self_print_urls = resp_dict['self_print_html_pages']

        return self

    @property
    def self_print_urls(self):
        """List of URLs for self print vouchers on this reservation."""
        if self._self_print_urls is None:
            self.get_details()

        return self._self_print_urls

    @self_print_urls.setter
    def self_print_urls(self, value):
        self._self_print_urls = value

    def set_confirmation_page(self, html):
        """Store the confirmation page HTML in the TSW system.

        Args:
            html (string): HTML to store.

        Returns:
            Boolean: True if data was saved successfully.
        """

        crypto_block = self.get_crypto_block(
            method_name='start_session',
            password_required=False
        )

        resp_dict = self.get_core_api().save_external_sale_page(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            transaction_id=self.transaction_id,
            sale_page_type='text', sale_page_subtype='html', sale_page=html,
        )

        if resp_dict['saved_this_page'] == 'yes':
            return True
        else:
            return False

    @property
    def is_released(self):
        """Boolean indicating if the reservation was released."""
        if self.transaction_status == 'released':
            return True
        elif self.transaction_status:
            return False
        return None

    @property
    def is_purchased(self):
        """Boolean indicating if the reservation was purchased successfully."""
        if self.transaction_status == 'purchased':
            return True
        elif self.transaction_status:
            return False
        return None

    @property
    def is_purchase_successful(self):
        """Boolean indicating if the reservation was purchased successfully.

        Overrides trolley function.
        """
        return self.is_purchased

    @property
    def is_reserved(self):
        """Boolean indicating if the Reservation object is reserved."""
        if self.transaction_status == 'reserved':
            return True
        elif self.transaction_status:
            return False
        return None

    @property
    def is_attempting(self):
        """Boolean indicating if TSW is currently attempting to reserve."""
        if self.transaction_status == 'attempting':
            return True
        elif self.transaction_status:
            return False
        return None

    def _create_bundle(self, core_bundle):
        return bundle_objs.Bundle(
            core_bundle=core_bundle,
            self_print_urls=self.self_print_urls,
            **self._internal_settings()
        )

    @property
    def need_payment_card(self):
        """Boolean indicating if a payment card is required for purchase."""
        return resolve_boolean(
            self._need_payment_card
        )

    @property
    def needs_email_address(self):
        """Boolean indicating if an email address is required for purchase."""
        return resolve_boolean(
            self._needs_email_address
        )

    @property
    def supports_billing_address(self):
        """Boolean indicating if billing address can be provided during
        purchase."""
        return resolve_boolean(
            self._supports_billing_address
        )

    @property
    def needs_agent_reference(self):
        return resolve_boolean(
            self._needs_agent_reference
        )
