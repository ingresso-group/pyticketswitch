# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import datetime
from operator import attrgetter

from pyticketswitch.util import (
    date_to_yyyymmdd, date_to_yyyymmdd_or_none, hhmmss_to_time,
    resolve_boolean, time_to_hhmmss, to_int_or_none, yyyymmdd_to_date
)

from . import availability as availability
from . import event as event_objs
from .base import CostRangeMixin, InterfaceObject


class Performance(InterfaceObject, CostRangeMixin):
    """Object that represents a TSW performance.

    Operations relating to a TSW performance are accessible through this
    object, e.g. getting available ticket types. Can be constructed with
    the Id of the Performance (other constructor arguments are for
    internal use).

    Inherits from the CostRangeMixin class, so these functions are
    available.

    Args:
        perf_id (string): Id of the Performance
        settings (kwargs): See Core constructor.
    """

    @staticmethod
    def _get_perf_id(
        event_id, perf_token=None, usage_date=None, departure_date=None
    ):

        perf_id = '{0}{1}'.format(
            len(event_id), event_id,
        )

        if departure_date:
            perf_id = '{0}d{1}'.format(
                perf_id, date_to_yyyymmdd(departure_date)
            )

        if perf_token:
            perf_id = '{0}p{1}'.format(
                perf_id, perf_token
            )

        elif usage_date:
            perf_id = '{0}u{1}'.format(
                perf_id, date_to_yyyymmdd(usage_date)
            )

        return perf_id

    def __init__(
        self,
        perf_id=None,
        core_performance=None,
        **settings
    ):
        self.perf_id = perf_id
        self._set_perf_id_attrs(perf_id)
        self._core_performance = core_performance

        self._ticket_types = None
        self._despatch_methods = None
        self._valid_ticket_quantities = None
        self._event = None

        super(Performance, self).__init__(**settings)

        if core_performance is not None:
            self._set_datetime(
                date_yyyymmdd=core_performance.date_yyyymmdd,
                time_hhmmss=core_performance.time_hhmmss
            )
        elif self.usage_date is not None:
            self.date = self.usage_date

        else:
            self._set_datetime(None)

        if self._event_id:
            self._event = event_objs.Event(
                event_id=self._event_id,
                **self._internal_settings()
            )

    @classmethod
    def from_event_and_perf_token(
        cls,
        event,
        perf_token,
        core_performance,
        departure_date=None,
        **settings
    ):

        return cls(
            perf_id=cls._get_perf_id(
                event_id=event.event_id,
                perf_token=perf_token,
                departure_date=departure_date,
            ),
            core_performance=core_performance,
            **settings
        )

    @classmethod
    def from_event_and_usage_date(
        cls,
        event,
        usage_date,
        departure_date=None,
        **settings
    ):

        return cls(
            perf_id=cls._get_perf_id(
                event_id=event.event_id,
                usage_date=usage_date,
                departure_date=departure_date,
            ),
            **settings
        )

    @classmethod
    def from_event_only(
        cls, event, **settings
    ):

        return cls(
            perf_id=cls._get_perf_id(
                event_id=event.event_id,
            ),
            **settings
        )

    def _set_perf_id_attrs(self, perf_id):

        self._event_id = None
        self.departure_date = None
        self._perf_token = None
        self.usage_date = None

        if perf_id:

            event_len = int(perf_id[0])

            self._event_id = perf_id[1:event_len + 1]

            remaining = perf_id[event_len + 1:]

            if remaining and remaining[0] == 'd':
                self.departure_date = yyyymmdd_to_date(
                    remaining[1:9]  # yyyymmdd
                )
                remaining = remaining[9:]

            if remaining and remaining[0] == 'p':
                self._perf_token = remaining[1:]

            elif remaining and remaining[0] == 'u':
                self.usage_date = yyyymmdd_to_date(
                    remaining[1:9]  # yyyymmdd
                )

    def _set_datetime(self, date_yyyymmdd, time_hhmmss=None):

        if date_yyyymmdd:
            self.date = yyyymmdd_to_date(date_yyyymmdd)

        else:
            self.date = None

        if time_hhmmss:
            self.time = hhmmss_to_time(time_hhmmss)

        else:
            self.time = None

    def _get_cache_key(self):
        return self.perf_id

    def _get_core_performance_attr(self, attr):
        return getattr(self._core_performance, attr, None)

    # Overridden function for CostRangeMixin
    def _get_core_cost_range(self):
        return self._get_core_performance_attr('cost_range')

    @property
    def date_desc(self):
        return self._get_core_performance_attr('date_desc')

    @property
    def time_desc(self):
        return self._get_core_performance_attr('time_desc')

    @property
    def date_slug(self):
        return date_to_yyyymmdd(self.date)

    @property
    def time_slug(self):
        return time_to_hhmmss(self.time)

    @property
    def day_name(self):
        if self.date is not None:
            if self.delta_from_today == 0:
                return 'Today'
            elif self.delta_from_today == 1:
                return 'Tomorrow'
            else:
                return self.date.strftime('%A')

    @property
    def delta_from_today(self):
        """Integer number of days from today."""
        if self.date is not None:
            today = datetime.date.today()

            return (self.date - today).days

    @property
    def required_info(self):
        """Required info text.

        Returns a string of the required_info or None if there isn't
        any for this performance. Must be displayed if present.
        """
        return self._get_core_performance_attr('perf_name')

    @property
    def is_limited(self):
        """Boolean flag indicating limited availability."""
        return resolve_boolean(
            self._get_core_performance_attr('is_limited')
        )

    @property
    def cached_max_seats(self):
        """Maximum number of contiguous seats available."""
        return to_int_or_none(
            self._get_core_performance_attr('cached_max_seats')
        )

    @property
    def perf_type_code(self):
        """Type code, for internal use."""
        return self._get_core_performance_attr('perf_type_code')

    @property
    def ticket_types(self):
        """List of TicketType objects for this Performance."""
        if self._ticket_types is None:
            return self.get_availability()
        else:
            return self._ticket_types

    @ticket_types.setter
    def ticket_types(self, value):
        self._ticket_types = value

    @property
    def valid_ticket_quantities(self):
        """List of valid ticket quantities for this Performance."""
        if self._valid_ticket_quantities is None:

            crypto_block = self._get_date_time_options_crypto()

            resp_dict = self.get_core_api().availability_options(
                crypto_block=crypto_block,
                upfront_data_token=self.settings['upfront_data_token'],
                perf_token=self._perf_token,
                usage_date=date_to_yyyymmdd_or_none(self.usage_date),
                departure_date=date_to_yyyymmdd_or_none(self.departure_date),
                quantity_options_only=True
            )

            self._set_ticket_quantities_from_dict(
                resp_dict.get('quantity_options', None)
            )

        return self._valid_ticket_quantities

    def _set_ticket_quantities_from_dict(self, quantity_options_dict):

        valid_list = []

        if quantity_options_dict:

            valid_list = quantity_options_dict.get('valid_quantity', [])

            valid_list = [int(x) for x in valid_list]

        self.valid_ticket_quantities = valid_list

    @valid_ticket_quantities.setter
    def valid_ticket_quantities(self, value):
        self._valid_ticket_quantities = value

    @property
    def event(self):
        """The Event object this performance relates to."""
        if self._event is None:
            self.get_despatch_methods()

        if self._event:
            return self._event
        else:
            return None

    @event.setter
    def event(self, value):
        if value is None:
            self._event = False
        else:
            self._event = value

    def _get_date_time_options_crypto(self):

        crypto_block = self._get_crypto_block_for_object(
            method_name='date_time_options',
            interface_object=self._event,
        )

        if not crypto_block:
            self.event.get_performances()

            crypto_block = self._get_crypto_block_for_object(
                method_name='date_time_options',
                interface_object=self._event,
            )

        return crypto_block

    def get_availability(
        self, include_possible_concessions=None, no_of_tickets=None,
        include_available_seat_blocks=None, include_user_commission=None,
    ):
        """Retrieves ticket availability information for this Performance.

        Returns the list of TicketType objects, called internally by several
        methods, it calls the 'availability_options' API method.
        The 'ticket_types' property should be used to get this information,
        but this method can be called explicitly if required.

        Args:
            include_possible_concessions (boolean): Optional, flag to indicate
                whether to request possible_concession information.
            no_of_tickets (int): Optional, set the number of tickets to
                request, allows actual seats to be returned if possible.
            include_available_seat_blocks (boolean): Optional, flag to indicate
                whether to request the available seat blocks, allowing specific
                seats to be selected.
            include_user_commission (boolean): Optional, flag to indicate
                whether to request the user's commission information.

        Returns:
            list: List of TicketType objects
        """

        crypto_block = self._get_date_time_options_crypto()

        resp_dict = self.get_core_api().availability_options(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            perf_token=self._perf_token,
            usage_date=date_to_yyyymmdd_or_none(self.usage_date),
            departure_date=date_to_yyyymmdd_or_none(self.departure_date),
            self_print_mode='html', add_discounts=include_possible_concessions,
            no_of_tickets=no_of_tickets,
            add_free_seat_blocks=include_available_seat_blocks,
            add_user_commission=include_user_commission
        )

        self._set_crypto_block(
            crypto_block=resp_dict['crypto_block'],
            method_name='availability_options'
        )

        ticket_types = []

        if 'ticket_type' in resp_dict:
            for tt in resp_dict['ticket_type']:
                for pb in tt.price_bands:
                    ticket_type = availability.TicketType(
                        ticket_type_id=pb.band_token, core_ticket_type=tt,
                        core_price_band=pb,
                        core_currency=resp_dict.get('currency', None),
                        **self._internal_settings()
                    )

                    ticket_type.set_valid_quantities(
                        valid_quantities=resp_dict['quantity_options'][
                            'valid_quantity'
                        ]
                    )

                    ticket_types.append(ticket_type)

        self.ticket_types = ticket_types

        self._set_crypto_for_objects(
            crypto_block=resp_dict['crypto_block'],
            method_name='availability_options',
            interface_objects=ticket_types
        )

        self._set_ticket_quantities_from_dict(
            resp_dict.get('quantity_options', None)
        )

        despatch_methods = []

        if 'despatch_options' in resp_dict:

            for dm in resp_dict['despatch_options']['despatch_method']:
                despatch_method = availability.DespatchMethod(
                    despatch_id=dm.despatch_token,
                    core_despatch_method=dm,
                    core_currency=resp_dict.get('currency', None),
                    **self._internal_settings()
                )

                despatch_methods.append(despatch_method)

        self.despatch_methods = despatch_methods

        self._core_performance = resp_dict.get('performance')

        if 'event' in resp_dict:
            event = event_objs.Event(
                event_id=resp_dict['event'].event_id,
                core_event=resp_dict['event'],
                **self._internal_settings()
            )
            self.event = event

        return ticket_types

    def get_initial_ticket_type(self, no_of_tickets):
        if self.ticket_types:
            if int(no_of_tickets) <= 1:
                return self.ticket_types[0]
            else:
                for tt in self.ticket_types:
                    if int(tt.number_available) >= int(no_of_tickets):
                        return tt
        else:
            return None

    @property
    def ticket_types_by_type_then_price(self):
        """Ticket Type objects ordered by description then combined price."""
        return sorted(
            self.ticket_types, key=attrgetter(
                'description', 'price_combined_float'
            )
        )

    @property
    def ticket_types_by_cheapest_type(self):
        """Ticket Type objects ordered by cheapest description then price."""
        order_dict = {}

        i = 0
        for t in self.ticket_types_by_combined_price:
            if not order_dict or t.description not in order_dict:
                order_dict[t.description] = i
                i += 1

        return sorted(
            self.ticket_types, key=lambda x: (
                order_dict[x.description],
                x.price_combined_float,
                x.int_percentage_saving
            )
        )

    @property
    def ticket_types_by_combined_price(self):
        """Ticket Type objects ordered by combined price."""
        return sorted(
            self.ticket_types, key=attrgetter(
                'price_combined_float', 'int_percentage_saving'
            )
        )

    @property
    def ticket_types_by_saving(self):
        """Ticket Type objects ordered by percentage saving."""
        return sorted(
            self.ticket_types,
            key=attrgetter('int_percentage_saving', 'price_combined_float'),
            reverse=True
        )

    @property
    def unique_combined_prices(self):
        """List of unique combined prices."""
        unique_list = []

        for tt in self.ticket_types_by_combined_price:
            if tt.price_combined not in unique_list:
                unique_list.append(tt.price_combined)

        return unique_list

    @property
    def despatch_methods(self):
        """List of DespatchMethod objects for this Performance."""
        if self._despatch_methods is None:
            return self.get_despatch_methods()
        else:
            return self._despatch_methods

    @despatch_methods.setter
    def despatch_methods(self, value):
        self._despatch_methods = value

    def get_despatch_methods(self):
        """Retrieves despatch method information for this Performance.

        Returns the list of DespatchMethod objects, called internally by some
        methods, it calls the 'despatch_options' API method.
        The 'despatch_methods' property should be used to get this information,
        but this method can be called explicitly if required.

        Returns:
            list: List of DespatchMethod objects
        """

        crypto_block = self._get_date_time_options_crypto()

        resp_dict = self.get_core_api().despatch_options(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            perf_token=self._perf_token,
            usage_date=date_to_yyyymmdd_or_none(self.usage_date),
            departure_date=date_to_yyyymmdd_or_none(self.departure_date),
            self_print_mode='html'
        )

        despatch_methods = []

        for dm in resp_dict['despatch_options']['despatch_method']:
            despatch_method = availability.DespatchMethod(
                despatch_id=dm.despatch_token,
                core_despatch_method=dm,
                core_currency=resp_dict.get('currency', None),
                **self._internal_settings()
            )

            despatch_methods.append(despatch_method)

        self.despatch_methods = despatch_methods

        self._core_performance = resp_dict.get('performance')

        event = None
        if 'event' in resp_dict:
            event = event_objs.Event(
                event_id=resp_dict['event'].event_id,
                core_event=resp_dict['event'],
                **self._internal_settings()
            )
        self.event = event

        return despatch_methods
