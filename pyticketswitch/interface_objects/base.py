# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import logging

import six
from pyticketswitch import settings as default_settings
from pyticketswitch.interface import CoreAPI
from pyticketswitch.util import (
    format_price_with_symbol, resolve_boolean, to_float_or_none,
    to_int_or_none
)

logger = logging.getLogger(__name__)


class InterfaceObject(object):
    """Superclass for all objects that will perform API operations.

    The class should not be instantiated directly, it is designed to
    be subclassed. Contains a number of internal methods that provide
    standard functionality for API operations.

    Subclasses of this object should call the constructor of this
    object.

    Args:
        username (string): TSW user
        password (string): password for TSW user
        url (string): TSW API URL
        accept_language (string): user's HTTP Accept-Language header
        api_request_timeout (int): API timeout in seconds
        no_time_descr (string): text to use if no time is returned
            by the API for a performance
        default_concession_descr (string): text to use if no description
            is returned by the API for a concession
        remote_ip (string): user's IP address (internal use)
        remote_site (string): domain of the user request (internal use)
        additional_elements (dict): An optional dictionary of key/values to
            include in the XML passed to the API.
        upfront_data_token (string): upfront data token is required by the API
            in certain cases, such as for redeem
        requests_session (requests.Session object): optional Requests session
            to use for making HTTP requests
    """

    CRYPTO_PREFIX = 'CRYPTO_BLOCK'
    USERNAME_PREFIX = 'USERNAME'
    RUNNING_USER_PREFIX = 'RUNNING_USER'

    def __init__(self, **kwargs):

        self._session = None
        self._core_api = None
        self.settings = self._get_settings()
        self._session_store = {}

        if 'session' in kwargs:
            self._session = kwargs.pop('session')

        if '_core_api' in kwargs:
            self._core_api = kwargs.pop('_core_api')

        if '_settings' in kwargs:
            self.settings = kwargs.pop('_settings')

        if '_session_store' in kwargs:
            self._session_store = kwargs.pop('_session_store')

        if kwargs:
            self._configure(**kwargs)

    def _get_settings(
            self, username=None, password=None, sub_id=None, url=None,
            no_time_descr=None, api_request_timeout=None,
            default_concession_descr=None, remote_ip=None,
            remote_site=None, accept_language=None,
            additional_elements=None, upfront_data_token=None,
            requests_session=None, custom_start_session=None):

        return {
            'username': username,
            'password': password,
            'sub_id': sub_id,
            'remote_ip': remote_ip,
            'remote_site': remote_site,
            'accept_language': accept_language,
            'url': url,
            'api_request_timeout': api_request_timeout,
            'no_time_descr': no_time_descr,
            'default_concession_descr': default_concession_descr,
            'additional_elements': additional_elements,
            'upfront_data_token': upfront_data_token,
            'requests_session': requests_session,
            'custom_start_session': custom_start_session,
        }

    def _configure(
            self, username=None, password=None, sub_id=None, url=None,
            no_time_descr=None, api_request_timeout=None,
            default_concession_descr=None, remote_ip=None,
            remote_site=None, accept_language=None,
            additional_elements=None, upfront_data_token=None,
            requests_session=None, custom_start_session=None):

        if (not username) and remote_ip and remote_site:
            username = self._get_cached_username(
                remote_ip=remote_ip,
                remote_site=remote_site
            )

        if (
            (
                'username' in self.settings and
                self.settings['username'] and
                username != self.settings['username']
            ) or
            (
                'remote_ip' in self.settings and
                self.settings['remote_ip'] and
                remote_ip != self.settings['remote_ip']
            ) or
            (
                'remote_site' in self.settings and
                self.settings['remote_site'] and
                remote_site != self.settings['remote_site']
            )
        ):
            self._clear_crypto_blocks()

        if not url:
            url = default_settings.API_URL

        if not api_request_timeout:
            api_request_timeout = default_settings.API_REQUEST_TIMEOUT

        if not no_time_descr:
            no_time_descr = default_settings.NO_TIME_DESCR

        if not default_concession_descr:
            default_concession_descr = (
                default_settings.DEFAULT_CONCESSION_DESCR
            )

        self.settings = self._get_settings(
            username=username, password=password, sub_id=sub_id,
            url=url, no_time_descr=no_time_descr,
            api_request_timeout=api_request_timeout,
            default_concession_descr=default_concession_descr,
            remote_ip=remote_ip,
            remote_site=remote_site,
            accept_language=accept_language,
            additional_elements=additional_elements,
            upfront_data_token=upfront_data_token,
            requests_session=requests_session,
            custom_start_session=custom_start_session,
        )

        self._core_api = CoreAPI(
            username=username,
            password=password,
            sub_id=sub_id,
            url=url,
            remote_ip=remote_ip,
            remote_site=remote_site,
            accept_language=accept_language,
            api_request_timeout=api_request_timeout,
            additional_elements=additional_elements,
            requests_session=requests_session,
            custom_start_session=custom_start_session,
        )

    def get_core_api(self):
        return self._core_api

    def set_session(self, session):
        self._session = session

    def _password_is_set(self):

        if self.settings.get('password'):
            return True
        else:
            return False

    def _start_session(self):
        crypto_block = self.get_core_api().start_session()

        username = self.get_core_api().username

        if (
            not self.settings['username'] or
            username != self.settings['username']
        ):

            remote_ip = self.settings['remote_ip']
            remote_site = self.settings['remote_site']

            self.settings['username'] = username
            self._set_cached_username(
                username=username,
                remote_ip=remote_ip,
                remote_site=remote_site
            )

            self._set_cached_running_user(
                username=username,
                running_user=self.get_core_api().running_user,
            )

        if crypto_block:
            self._set_crypto_block(
                crypto_block=crypto_block,
                method_name='start_session'
            )

        return crypto_block

    def get_username(self):

        if not self.settings['username']:

            remote_ip = self.settings['remote_ip']
            remote_site = self.settings['remote_site']

            username = self._get_cached_username(
                remote_ip=remote_ip,
                remote_site=remote_site
            )

            if not username:
                self._start_session()

        return self.settings['username']

    def _get_running_user(self):
        if not self.get_core_api().running_user:

            running_user = self._get_cached_running_user(
                username=self.get_username()
            )

            if running_user:
                self.get_core_api().running_user = running_user
            else:
                self._start_session()

        return self.get_core_api().running_user

    def get_restrict_group(self):
        return self._get_running_user().sphinx_restrict_group

    def get_default_language_code(self):
        running_user = self._get_running_user()
        if running_user:
            return running_user.default_lang_code

    def get_content_language(self):
        return self.get_core_api().content_language

    def _store_data(self, key, data, save_session=True):

        logger.debug('_store_data, key: %s, data: %s', key, data)

        self._session_store[key] = data

        if self._session is not None:
            self._session[key] = data

            if save_session and hasattr(self._session, 'save'):
                self._session.save()

    def _retrieve_data(self, key):

        data = self._session_store.get(key, None)

        if not data and self._session is not None:
            data = self._session.get(key)

        logger.debug('_retrieve_data, key: %s, data: %s', key, data)

        return data

    def _get_username_session_key(self, remote_ip, remote_site):
        return '{0}_{1}_{2}'.format(
            self.USERNAME_PREFIX, remote_ip, remote_site
        )

    def _get_cached_username(
            self, remote_ip, remote_site):
        key = self._get_username_session_key(
            remote_ip=remote_ip,
            remote_site=remote_site
        )

        return self._retrieve_data(key)

    def _set_cached_username(
            self, username, remote_ip, remote_site):
        key = self._get_username_session_key(
            remote_ip=remote_ip,
            remote_site=remote_site
        )

        self._store_data(key=key, data=username)

    def _get_running_user_session_key(self, username):
        return '{0}_{1}'.format(
            self.RUNNING_USER_PREFIX, username
        )

    def _get_cached_running_user(self, username):

        key = self._get_running_user_session_key(
            username=username,
        )

        return self._retrieve_data(key)

    def _set_cached_running_user(self, username, running_user):

        key = self._get_running_user_session_key(
            username=username,
        )

        self._store_data(key=key, data=running_user)

    def _get_crypto_session_key(self, username, method_name):
        return '{0}_{1}_{2}'.format(
            self.CRYPTO_PREFIX, username, method_name
        )

    def _clear_crypto_blocks(self):

        logger.debug('_clear_crypto_blocks called')

        for key in self._session_store.keys():
            if key.startswith(self.CRYPTO_PREFIX):
                del self._session_store[key]

        if self._session is not None:

            if hasattr(self._session, 'flush_crypto_blocks'):
                self._session.flush_crypto_blocks()
            else:
                for key in self._session.keys():
                    if key.startswith(self.CRYPTO_PREFIX):
                        del self._session[key]

    def get_crypto_block(
            self, method_name, password_required=True):

        crypto_block = None

        if (
            password_required or (
                not password_required and not self._password_is_set()
            )
        ):
            if not self.settings.get('username', False):
                start_session_crypto = self._start_session()
            else:
                start_session_crypto = None

            session_key = self._get_crypto_session_key(
                username=self.settings['username'],
                method_name=method_name
            )

            crypto_block = self._retrieve_data(session_key)

            if not crypto_block and method_name == 'start_session':

                if start_session_crypto:
                    crypto_block = start_session_crypto
                else:
                    crypto_block = self._start_session()

        return crypto_block

    def _set_crypto_block(self, crypto_block, method_name):

        session_key = self._get_crypto_session_key(
            username=self.settings['username'], method_name=method_name
        )

        self._store_data(key=session_key, data=crypto_block)

    def _get_crypto_object_key(
            self, username, method_name, interface_object):

        return '{0}_{1}'.format(
            self._get_crypto_session_key(
                username=username, method_name=method_name
            ), interface_object._get_cache_key()
        )

    def _set_crypto_for_objects(
            self, crypto_block, method_name, interface_objects):

        for i, obj in enumerate(interface_objects):
            key = self._get_crypto_object_key(
                username=self.settings['username'],
                method_name=method_name,
                interface_object=obj
            )

            if i == len(interface_objects) - 1:
                save_session = True
            else:
                save_session = False

            self._store_data(
                key=key, data=crypto_block,
                save_session=save_session
            )

    def _set_crypto_for_object(
            self, crypto_block, method_name, interface_object):

        key = self._get_crypto_object_key(
            username=self.settings['username'],
            method_name=method_name,
            interface_object=interface_object
        )

        self._store_data(
            key=key, data=crypto_block,
        )

    def _get_crypto_block_for_object(self, method_name, interface_object):

        if not self.settings.get('username', False):
            self._start_session()

        key = self._get_crypto_object_key(
            username=self.settings['username'],
            method_name=method_name,
            interface_object=interface_object
        )

        return self._retrieve_data(key)

    def _internal_settings(self):
        return {
            'session': self._session,
            '_core_api': self._core_api,
            '_settings': self.settings,
            '_session_store': self._session_store,
        }

    def __getstate__(self):

        d = self.__dict__.copy()
        d['_session'] = None
        d['_core_api'] = None
        d['settings'] = self._get_settings()
        d['_session_store'] = {}

        return d


class Currency(object):
    """Represents a Currency in TSW, used in several other objects.

    The constructor is for internal user only.
    """

    def __init__(
        self,
        core_currency
    ):
        self._core_currency = core_currency

    @property
    def code(self):
        return self._core_currency.currency_code

    @property
    def number(self):
        return to_int_or_none(
            self._core_currency.currency_number
        )

    @property
    def pre_symbol(self):
        return self._core_currency.currency_pre_symbol

    @property
    def post_symbol(self):
        return self._core_currency.currency_post_symbol

    @property
    def factor(self):
        return to_int_or_none(
            self._core_currency.currency_factor
        )

    @property
    def decimal_places(self):
        return to_int_or_none(
            self._core_currency.currency_places
        )


class Seat(object):
    """Represents a Seat in TSW, used in several other objects.

    The constructor is for internal user only.
    """

    def __init__(
        self,
        core_seat
    ):
        self._core_seat = core_seat

    @property
    def seat_id(self):
        return self._core_seat.full_id

    @property
    def is_restricted_view(self):
        """Boolean representing whether the seat has a restricted view."""
        return resolve_boolean(self._core_seat.is_restricted_view)

    @property
    def seat_text(self):
        """Additional information about this seat.

        E.g. restricted legroom
        """
        return self._core_seat.seat_text

    @property
    def column_id(self):
        return self._core_seat.col_id

    @property
    def row_id(self):
        return self._core_seat.row_id

    @property
    def separator(self):
        """The seat id is made up of row_id + separator + column_id.
        Returns empty string if there is no separator.
        """
        return self._core_seat.separator or ''

    @property
    def column_sort_id(self):
        col = self._core_seat.col_id

        if col:
            try:
                col = int(col)
            except ValueError:
                pass

        return col

    @property
    def row_sort_id(self):
        row = self._core_seat.row_id

        if row:
            try:
                row = int(row)
            except ValueError:
                pass

        return row

    @property
    def barcode(self):
        return self._core_seat.barcode


class SeatBlock(object):
    """Represents a block of seats in TSW, used when selecting seats in the
    booking process.

    Args:
        seat_block_id (string): Id of the SeatBlock
    """

    def __init__(
        self,
        seat_block_id=None,
        core_seat_block=None,
    ):
        self._core_seat_block = core_seat_block

        if not seat_block_id and core_seat_block:
            seat_block_id = core_seat_block.seat_block_token

        self.seat_block_id = seat_block_id
        self._seats = False

    @property
    def block_length(self):
        if self._core_seat_block:
            return to_int_or_none(
                self._core_seat_block.block_length
            )
        return None

    @property
    def seats(self):
        if self._seats is False:
            if self._core_seat_block:

                self._seats = []

                for seat in self._core_seat_block.seats:
                    self._seats.append(
                        Seat(core_seat=seat)
                    )
            else:
                self._seats = None

        return self._seats


class Customer(object):
    """Object that represents a customer.

    The 'core_customer' argument in the constructor is for internal use.

    The user, supplier and world can_use_data arguments are for data
    protection purposes and control who can use the customer's data.
    User is the TSW affiliate, supplier is the backend ticket supplier and
    world is third parties.

    Args:
        first_name (string): First name.
        last_name (string): Last name.
        home_phone (string): Home phone number.
        work_phone (string): Work phone number.
        address (Address): Home address.
        title (string): Optional, title.
        email_address (string): Optional, email address.
        user_can_use_data (boolean): Optional, data protection flag.
        supplier_can_use_data (boolean): Optional, data protection flag.
        world_can_use_data (boolean): Optional, data protection flag.
    """

    def __init__(
        self,
        core_customer=None,
        first_name=None,
        last_name=None,
        home_phone=None,
        work_phone=None,
        address=None,
        title=None,
        email_address=None,
        user_can_use_data=None,
        supplier_can_use_data=None,
        world_can_use_data=None,
        languages=None,
        agent_ref=None,
    ):

        self._core_customer = core_customer
        self._first_name = first_name
        self._last_name = last_name
        self._home_phone = home_phone
        self._work_phone = work_phone
        self._address = address
        self._title = title
        self._email_address = email_address
        self._user_can_use_data = user_can_use_data
        self._supplier_can_use_data = supplier_can_use_data
        self._world_can_use_data = world_can_use_data
        self._agent_ref = agent_ref

        self.languages = languages

    def _get_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'home_phone': self.home_phone,
            'work_phone': self.work_phone,
            'title': self.title,
            'email_address': self.email_address,
            'country_code': self.country_code,
            'address_line_one': self.address_line_one,
            'address_line_two': self.address_line_two,
            'town': self.town,
            'county': self.county,
            'postcode': self.postcode,
            'user_can_use_data': self.user_can_use_data,
            'supplier_can_use_data': self.supplier_can_use_data,
            'world_can_use_data': self.world_can_use_data,
            'agent_reference': self.agent_ref,
        }

    @property
    def first_name(self):
        if self._core_customer:
            return self._core_customer.first_name
        else:
            return self._first_name

    @property
    def last_name(self):
        if self._core_customer:
            return self._core_customer.last_name
        else:
            return self._last_name

    @property
    def home_phone(self):
        if self._core_customer:
            return self._core_customer.home_phone
        else:
            return self._home_phone

    @property
    def work_phone(self):
        if self._core_customer:
            return self._core_customer.work_phone
        else:
            return self._work_phone

    @property
    def country_code(self):
        if self._core_customer:
            return self._core_customer.country_code
        else:
            return self._address.country_code

    @property
    def address_line_one(self):
        if self._core_customer:
            return self._core_customer.addr_line_one
        else:
            return self._address.address_line_one

    @property
    def address_line_two(self):
        if self._core_customer:
            return self._core_customer.addr_line_two
        else:
            return self._address.address_line_two

    @property
    def town(self):
        if self._core_customer:
            return self._core_customer.town
        else:
            return self._address.town

    @property
    def county(self):
        if self._core_customer:
            return self._core_customer.county
        else:
            return self._address.county

    @property
    def postcode(self):
        if self._core_customer:
            return self._core_customer.postcode
        else:
            return self._address.postcode

    @property
    def country(self):
        if self._core_customer:
            return self._core_customer.country
        else:
            return self._country

    @property
    def title(self):
        if self._core_customer:
            return self._core_customer.title
        else:
            return self._title

    @property
    def email_address(self):
        if self._core_customer:
            return self._core_customer.email_addr
        else:
            return self._email_address

    @property
    def user_can_use_data(self):
        if self._core_customer:
            return resolve_boolean(
                self._core_customer.dp_user
            )
        else:
            if isinstance(self._user_can_use_data, bool):
                return self._user_can_use_data
            elif isinstance(self._user_can_use_data, six.string_types):
                return resolve_boolean(
                    self._user_can_use_data
                )

    @property
    def supplier_can_use_data(self):
        if self._core_customer:
            return resolve_boolean(
                self._core_customer.dp_supplier
            )
        else:
            if isinstance(self._supplier_can_use_data, bool):
                return self._supplier_can_use_data
            elif isinstance(self._supplier_can_use_data, six.string_types):
                return resolve_boolean(
                    self._supplier_can_use_data
                )

    @property
    def world_can_use_data(self):
        if self._core_customer:
            return resolve_boolean(
                self._core_customer.dp_world
            )
        else:
            if isinstance(self._world_can_use_data, bool):
                return self._world_can_use_data
            elif isinstance(self._world_can_use_data, six.string_types):
                return resolve_boolean(
                    self._world_can_use_data
                )

    @property
    def agent_ref(self):
        if self._core_customer:
            return self._core_customer.agent_ref
        else:
            return self._agent_ref


class Card(object):
    """Object that represents a payment card.

    Args:
        card_number (string): The main card number.
        expiry_date (datetime.date): Expiry date of the card.
        cv_two (string): The card verification number (a.k.a CVV).
        start_date (datetime.date): Optional, start date of card.
        issue_number (string): Optional, card issue number.
        billing_address (Address): Optional, alternative billing address.
    """

    def __init__(
        self,
        card_number,
        expiry_date,
        cv_two,
        start_date=None,
        issue_number=None,
        billing_address=None
    ):

        self._card_number = card_number
        self._start_date = start_date
        self._expiry_date = expiry_date
        self._cv_two = cv_two
        self._issue_number = issue_number
        self._billing_address = billing_address

    def _get_dict(self):
        return {
            'card_number': self.card_number,
            'start_date': self.start_date_mmyy,
            'expiry_date': self.expiry_date_mmyy,
            'cv_two': self.cv_two,
            'issue_number': self.issue_number,
            'address_line_one': self.billing_address_line_one,
            'address_line_two': self.billing_address_line_two,
            'town': self.billing_town,
            'county': self.billing_county,
            'postcode': self.billing_postcode,
            'country_code': self.billing_country_code
        }

    @property
    def card_number(self):
        return self._card_number

    @property
    def start_date(self):
        return self._start_date

    @property
    def start_date_mmyy(self):
        """Returns string value in mmyy format"""
        if self.start_date:
            return self.start_date.strftime('%m%y')
        else:
            return None

    @property
    def expiry_date(self):
        return self._expiry_date

    @property
    def expiry_date_mmyy(self):
        """Returns string value in mmyy format"""
        return self.expiry_date.strftime('%m%y')

    @property
    def cv_two(self):
        return self._cv_two

    @property
    def issue_number(self):
        return self._issue_number

    @property
    def billing_address_line_one(self):
        if self._billing_address:
            return self._billing_address.address_line_one
        else:
            return None

    @property
    def billing_address_line_two(self):
        if self._billing_address:
            return self._billing_address.address_line_two
        else:
            return None

    @property
    def billing_town(self):
        if self._billing_address:
            return self._billing_address.town
        else:
            return None

    @property
    def billing_county(self):
        if self._billing_address:
            return self._billing_address.county
        else:
            return None

    @property
    def billing_postcode(self):
        if self._billing_address:
            return self._billing_address.postcode
        else:
            return None

    @property
    def billing_country_code(self):
        if self._billing_address:
            return self._billing_address.country_code
        else:
            return None


class Address(object):
    """Object that represents an address.

    The attributes are the same as the constructor arguments.

    Args:
        address_line_one (string): 1st line of address.
        country_code (string): 2 digit ISO 3166 country code.
        address_line_two (string): Optional, 2nd line of address.
        town (string): Optional, town.
        county (string): Optional, county.
        postcode (string): Optional, postcode.
    """

    def __init__(
        self,
        address_line_one,
        country_code,
        address_line_two=None,
        town=None,
        county=None,
        postcode=None
    ):

        self.address_line_one = address_line_one
        self.address_line_two = address_line_two
        self.town = town
        self.county = county
        self.postcode = postcode
        self.country_code = country_code


class SpecialOffer(object):
    """Represents a special offer in TSW, used in objects with cost range
    information.

    The constructor is for internal user only.
    """

    def __init__(self, core_offer, core_currency, offer_type):

        self._core_offer = core_offer
        self._core_currency = core_currency
        self.offer_type = offer_type
        self.currency = Currency(
            core_currency=core_currency
        )

    @property
    def full_combined_price(self):
        """Formatted string value of the full combined price with
        currency symbol.
        """
        return format_price_with_symbol(
            self._core_offer['full_combined'],
            self.currency.pre_symbol,
            self.currency.post_symbol
        )

    @property
    def full_combined_price_float(self):
        """Float value of the full combined price."""
        return to_float_or_none(
            self._core_offer['full_combined']
        )

    @property
    def full_seatprice(self):
        """Formatted string value of the full seatprice price with
        currency symbol.
        """
        return format_price_with_symbol(
            self._core_offer['full_seatprice'],
            self.currency.pre_symbol,
            self.currency.post_symbol
        )

    @property
    def full_seatprice_float(self):
        """Float value of the full seatprice price."""
        return to_float_or_none(
            self._core_offer['full_seatprice']
        )

    @property
    def full_surcharge_price(self):
        """Formatted string value of the full surcharge price with
        currency symbol.
        """
        return format_price_with_symbol(
            self._core_offer['full_surcharge'],
            self.currency.pre_symbol,
            self.currency.post_symbol
        )

    @property
    def full_surcharge_price_float(self):
        """Float value of the full surcharge price."""
        return to_float_or_none(
            self._core_offer['full_surcharge']
        )

    @property
    def offer_combined_price(self):
        """Formatted string value of the offer combined price with
        currency symbol.
        """
        return format_price_with_symbol(
            self._core_offer['offer_combined'],
            self.currency.pre_symbol,
            self.currency.post_symbol
        )

    @property
    def offer_combined_price_float(self):
        """Float value of the offer combined price."""
        return to_float_or_none(
            self._core_offer['offer_combined']
        )

    @property
    def offer_seatprice(self):
        """Formatted string value of the offer seatprice price with
        currency symbol.
        """
        return format_price_with_symbol(
            self._core_offer['offer_seatprice'],
            self.currency.pre_symbol,
            self.currency.post_symbol
        )

    @property
    def offer_seatprice_float(self):
        """Float value of the offer seatprice price."""
        return to_float_or_none(
            self._core_offer['offer_seatprice']
        )

    @property
    def offer_surcharge_price(self):
        """Formatted string value of the offer surcharge price with
        currency symbol.
        """
        return format_price_with_symbol(
            self._core_offer['offer_surcharge'],
            self.currency.pre_symbol,
            self.currency.post_symbol
        )

    @property
    def offer_surcharge_price_float(self):
        """Float value of the offer surcharge price."""
        return to_float_or_none(
            self._core_offer['offer_surcharge']
        )

    @property
    def percentage_saving(self):
        """Formatted string value of the percentage saving with
        percent sign.
        """
        return '{0}%'.format(
            self._core_offer['percentage_saving']
        )

    @property
    def percentage_saving_float(self):
        """Float value of the percentage saving."""
        return to_float_or_none(
            self._core_offer['percentage_saving']
        )

    @property
    def absolute_saving_float(self):
        """Float value of the absolute saving."""
        ab_val = self._core_offer.get('absolute_saving', None)

        if (
            ab_val is None and
            self.full_combined_price_float is not None and
            self.offer_combined_price_float is not None
        ):
            ab_val = (
                self.full_combined_price_float -
                self.offer_combined_price_float
            )

        return to_float_or_none(ab_val)

    @property
    def absolute_saving(self):
        """Formatted string value of the absolute saving value with
        currency symbol.
        """

        ret_val = None

        if self.absolute_saving_float is not None:

            ret_val = format_price_with_symbol(
                self.absolute_saving_float,
                self.currency.pre_symbol,
                self.currency.post_symbol
            )
        return ret_val

    @property
    def is_no_booking_fee_offer(self):
        """Boolean indicating if this is a no booking fee offer."""
        if (
            self.full_seatprice_float == self.offer_seatprice_float and
            (
                self.full_combined_price_float >
                self.offer_combined_price_float
            ) and
            not self.offer_surcharge_price_float
        ):
            return True

        return False


class CostRangeMixin(object):
    """Object to provide common cost range related functionality."""

    def _get_core_cost_range(self):
        """ This method must be overridden and should return a core
            cost range object.
        """
        raise NotImplementedError(
            'Subclasses must override _get_core_cost_range()'
        )

    @property
    def special_offers(self):
        """Returns a list of SpecialOffer objects."""
        offers = [
            self.best_value_offer, self.max_saving_offer,
            self.top_price_offer
        ]

        return [o for o in offers if o is not None]

    @property
    def currency(self):
        """Returns a currency object."""
        currency = None
        cost_range = self._get_core_cost_range()

        if cost_range:
            currency = Currency(
                core_currency=cost_range.currency
            )

        return currency

    @property
    def best_value_offer(self):
        """Object representing the best value offer. Returns None
        if there is no best value offer.
        """
        offer = None
        cost_range = self._get_core_cost_range()

        if cost_range and cost_range.best_value_offer:

            offer = SpecialOffer(
                core_offer=cost_range.best_value_offer,
                core_currency=cost_range.currency,
                offer_type='best_value',
            )

        return offer

    @property
    def max_saving_offer(self):
        """Object representing the max saving offer. Returns None
        if there is no max saving offer.
        """
        offer = None
        cost_range = self._get_core_cost_range()

        if cost_range and cost_range.max_saving_offer:

            offer = SpecialOffer(
                core_offer=cost_range.max_saving_offer,
                core_currency=cost_range.currency,
                offer_type='max_saving',
            )

        return offer

    @property
    def top_price_offer(self):
        """Object representing the top price offer. Returns None
        if there is no top price offer.
        """
        offer = None
        cost_range = self._get_core_cost_range()

        if cost_range and cost_range.top_price_offer:

            offer = SpecialOffer(
                core_offer=cost_range.top_price_offer,
                core_currency=cost_range.currency,
                offer_type='top_price',
            )

        return offer

    @property
    def min_seatprice(self):
        """Formatted string value of the minimun seat price with
        currency symbol.
        """
        min_price = None
        cost_range = self._get_core_cost_range()

        if cost_range:

            min_price = format_price_with_symbol(
                cost_range.min_seatprice,
                cost_range.currency.currency_pre_symbol,
                cost_range.currency.currency_post_symbol
            )

        return min_price

    @property
    def min_seatprice_float(self):
        """Float value of the minumum seat price."""
        fl_sp = None

        cost_range = self._get_core_cost_range()

        if cost_range:
            fl_sp = to_float_or_none(
                cost_range.min_seatprice
            )
        return fl_sp

    @property
    def min_combined_price(self):
        """Formatted string value of the minimun combined price with
        currency symbol.
        """
        min_price = None
        cost_range = self._get_core_cost_range()

        if cost_range:

            min_price = format_price_with_symbol(
                cost_range.min_combined,
                cost_range.currency.currency_pre_symbol,
                cost_range.currency.currency_post_symbol
            )

        return min_price

    @property
    def min_combined_price_float(self):
        """Float value of the minumum combined price."""
        fl_sp = None

        cost_range = self._get_core_cost_range()

        if cost_range:
            fl_sp = to_float_or_none(
                cost_range.min_combined
            )
        return fl_sp

    @property
    def max_combined_price_float(self):
        """Float value of the maximum combined price."""
        fl_sp = None

        cost_range = self._get_core_cost_range()

        if cost_range:
            fl_sp = to_float_or_none(
                cost_range.max_combined
            )
        return fl_sp

    @property
    def is_special_offer(self):
        """Boolean indicating if the object has a special offer."""
        if self.special_offers:
            return True

        return False

    @property
    def max_saving_percent(self):
        """Formatted string value of the maximum saving percentage
        with a '%' symbol.
        """
        if self.best_value_offer:
            return self.best_value_offer.percentage_saving

        return None

    @property
    def max_saving_absolute(self):
        """Formatted string value of the maximum possible saving with
        currency symbol.
        """
        if self.max_saving_offer:
            return self.max_saving_offer.absolute_saving

        return None

    @property
    def best_value_non_offer_combined_price(self):
        """Formatted string value of the original cost of the best value
        offer price with currency symbol (i.e. if there was no offer).
        """
        if self.best_value_offer:
            return self.best_value_offer.full_combined_price

        return None

    @property
    def best_value_offer_combined_price(self):
        """Formatted string value of the best value offer price with
        currency symbol.
        """
        if self.best_value_offer:
            return self.best_value_offer.offer_combined_price

        return None

    @property
    def has_no_booking_fee_offer(self):
        """Boolean to indicate if there is an offer that has no
        booking fee."""
        for o in self.special_offers:
            if o.is_no_booking_fee_offer:
                return True

        return False

    @property
    def cached_valid_ticket_quantities(self):
        """Returns a list of the valid ticket quantities that have been
        cached"""
        ticket_quantities = []
        cost_range = self._get_core_cost_range()

        if cost_range:
            if cost_range.quantity_options:
                ticket_quantities = cost_range.quantity_options.get(
                    'valid_quantity', []
                )
                ticket_quantities = [int(x) for x in ticket_quantities]

        return ticket_quantities

    @property
    def no_singles(self):
        """Returns a sub cost range object representing a cost range when
        selecting more than one ticket."""

        cost_range = self._get_core_cost_range()

        if cost_range and cost_range.no_singles_cost_range:
            return CostRange(cost_range.no_singles_cost_range)

        return None


class CostRange(CostRangeMixin):
    """A class providing the same functionality as CostRangeMixin, for use
    where an actual cost range object is required"""

    def __init__(self, core_cost_range):

        self._core_cost_range = core_cost_range

    def _get_core_cost_range(self):
        return self._core_cost_range


class Commission(object):
    """Object that represents a commission (either user comission or gross
    commission)
    """

    def __init__(self, core_commission):
        self._core_commission = core_commission

    @property
    def amount_excluding_vat(self):
        """Float value of the commission excluding VAT"""
        if self._core_commission.amount_excluding_vat:
            return to_float_or_none(
                self._core_commission.amount_excluding_vat
            )
        return None

    @property
    def amount_including_vat(self):
        """Float value of the commission including VAT"""
        if self._core_commission.amount_including_vat:
            return to_float_or_none(
                self._core_commission.amount_including_vat
            )
        return None

    @property
    def commission_currency(self):
        """Returns Currency object representing the currency that the
        commission values are provided in
        """
        if self._core_commission.commission_currency:
            return Currency(
                core_currency=self._core_commission.commission_currency
            )
        return None
