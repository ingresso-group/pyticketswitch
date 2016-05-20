# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from pyticketswitch import settings
from pyticketswitch.util import date_to_yyyymmdd

from . import event as event_objs
from . import order as order_objs
from . import reservation as res_objs
from .base import InterfaceObject


class Core(InterfaceObject):
    """Object that represents the core API functionality

    Operations that are not related to a particular object are accessible
    from this object, such as the event search. As such, it is commonly the
    starting point for API interactions.

    The only arguments are configuration settings, which are described below
    and are required when constructing several other objects.

    Args:
        username (string): TSW user
        password (string): password for TSW user
        url (string): TSW API URL
        accept_language (string): user's HTTP Accept-Language header
        api_request_timeout (int): Optional, API timeout in seconds
        no_time_descr (string): Optional, text to use if no time is returned
            by the API for a performance
        default_concession_descr (string): Optional, text to use if no
            description is returned by the API for a concession
    """

    def __init__(
        self, **settings
    ):
        self._setup_instance_variables()

        super(Core, self).__init__(**settings)

    def _setup_instance_variables(self):

        self.events = []
        self._cities = {}
        self._countries = {}
        self._categories = {}
        self._custom_fields = {}
        self._custom_filters = {}
        self._min_seatprice_range = []

    def _do_core_event_search(
            self, crypto_block, upfront_data_token, s_keys, s_dates, s_coco,
            s_city, s_geo_lat, s_geo_long, s_geo_rad_km,
            s_src, s_area, s_ven, s_eve,
            s_class, event_token_list,
            request_source_info, request_extra_info, request_video_iframe,
            request_cost_range, request_media, request_custom_fields,
            request_reviews, request_avail_details, request_meta_components,
            s_top, s_user_rating, s_critic_rating,
            s_auto_range, page_length, page_number,
            s_cust_fltr, s_airport, mime_text_type,
            special_offer_only, events=None, iter_index=0, max_iterations=None):

        # There is no filter in the core for special offers, so if only
        # the special offers are requested, then we need to recursively
        # call the event search until we have enough special offer events
        # (or there aren't any more events returned). By default, we do 3 small
        # searches followed by a full search. If max_iterations is provided, we
        # do that many small searches only.
        #
        # If the special_offer_only flag is False, then we can do a search
        # as normal
        if special_offer_only:

            if events is None:
                events = {}

            if not page_length:

                num_required = 0
                num_to_request = None
            else:

                if page_number:
                    num_required = page_length * (page_number + 1)
                else:
                    num_required = page_length

                # if the event search has been called multiple times
                # already, then do a full search
                if not max_iterations and iter_index > 2:
                    num_to_request = None
                else:
                    # arbitrarily choose to request twice as many events
                    # as required looking for special offers
                    num_to_request = num_required * 2

            resp_dict = self.get_core_api().event_search(
                crypto_block=crypto_block,
                upfront_data_token=upfront_data_token,
                s_keys=s_keys, s_dates=s_dates,
                s_coco=s_coco, s_city=s_city,
                s_geo_lat=s_geo_lat, s_geo_long=s_geo_long,
                s_geo_rad_km=s_geo_rad_km, s_src=s_src, s_area=s_area,
                s_ven=s_ven, s_eve=s_eve, s_class=s_class,
                event_token_list=event_token_list,
                request_source_info=request_source_info,
                request_extra_info=request_extra_info,
                request_video_iframe=request_video_iframe,
                request_cost_range=request_cost_range,
                request_media=request_media,
                request_custom_fields=request_custom_fields,
                request_reviews=request_reviews,
                request_avail_details=request_avail_details,
                request_meta_components=request_meta_components,
                s_top=s_top, s_user_rating=s_user_rating,
                s_critic_rating=s_critic_rating, s_auto_range=s_auto_range,
                page_length=num_to_request, page_number=iter_index,
                s_cust_fltr=s_cust_fltr, s_airport=s_airport,
                mime_text_type=mime_text_type,
            )

            # If the event has a special offer, then add it to the list
            for e in resp_dict['event']:
                if e.cost_range and (
                    e.cost_range.best_value_offer or
                    e.cost_range.max_saving_offer or
                    e.cost_range.top_price_offer
                ):

                    if e.event_id not in events:
                        events[e.event_id] = e

            # Return the list of special offer events if we've retrieved the
            # number required or there aren't any more or if max_iterations
            # has been reached
            if (
                not resp_dict['event'] or
                len(events) >= num_required or
                num_to_request is None or
                len(resp_dict['event']) < num_to_request or
                (max_iterations and (iter_index + 1) == max_iterations)
            ):

                if page_length is None:
                    resp_dict['event'] = list(events.values())

                else:

                    start = (page_number or 0) * page_length
                    end = ((page_number or 0) + 1) * page_length

                    resp_dict['event'] = list(events.values())[start:end]

                return resp_dict

            # Call recursively if we haven't found enough special offer
            # events yet
            else:

                iter_index = iter_index + 1

                return self._do_core_event_search(
                    crypto_block=crypto_block,
                    upfront_data_token=upfront_data_token,
                    s_keys=s_keys, s_dates=s_dates, s_coco=s_coco,
                    s_city=s_city, s_geo_lat=s_geo_lat,
                    s_geo_long=s_geo_long, s_geo_rad_km=s_geo_rad_km,
                    s_src=s_src, s_area=s_area, s_ven=s_ven,
                    s_eve=s_eve, s_class=s_class,
                    event_token_list=event_token_list,
                    request_source_info=request_source_info,
                    request_extra_info=request_extra_info,
                    request_video_iframe=request_video_iframe,
                    request_cost_range=request_cost_range,
                    request_media=request_media,
                    request_custom_fields=request_custom_fields,
                    request_reviews=request_reviews,
                    request_avail_details=request_avail_details,
                    request_meta_components=request_meta_components,
                    s_top=s_top, s_user_rating=s_user_rating,
                    s_critic_rating=s_critic_rating,
                    s_auto_range=s_auto_range, page_length=page_length,
                    page_number=page_number,
                    s_cust_fltr=s_cust_fltr, s_airport=s_airport,
                    special_offer_only=special_offer_only,
                    events=events, iter_index=iter_index,
                    mime_text_type=mime_text_type,
                    max_iterations=max_iterations,
                )

        else:
            return self.get_core_api().event_search(
                crypto_block=crypto_block,
                upfront_data_token=upfront_data_token,
                s_keys=s_keys, s_dates=s_dates,
                s_coco=s_coco, s_city=s_city,
                s_geo_lat=s_geo_lat, s_geo_long=s_geo_long,
                s_geo_rad_km=s_geo_rad_km, s_src=s_src, s_area=s_area,
                s_ven=s_ven, s_eve=s_eve, s_class=s_class,
                event_token_list=event_token_list,
                request_source_info=request_source_info,
                request_extra_info=request_extra_info,
                request_video_iframe=request_video_iframe,
                request_cost_range=request_cost_range,
                request_media=request_media,
                request_custom_fields=request_custom_fields,
                request_reviews=request_reviews,
                request_avail_details=request_avail_details,
                request_meta_components=request_meta_components,
                s_top=s_top, s_user_rating=s_user_rating,
                s_critic_rating=s_critic_rating, s_auto_range=s_auto_range,
                page_length=page_length, page_number=page_number,
                s_cust_fltr=s_cust_fltr, s_airport=s_airport,
                mime_text_type=mime_text_type,
            )

    def search_events(
            self, keyword=None,
            earliest_date=None, latest_date=None,
            country=None, city=None,
            latitude=None, longitude=None, radius=None,
            source=None, area_code=None, venue_code=None,
            event_code=None, category=None, event_id_list=None,
            page_length=None, page_number=None,
            sort_by=None, auto_date_range=None,
            request_source_info=None, request_extra_info=None,
            request_video_iframe=None, request_cost_range=True,
            request_media=None, request_custom_fields=True,
            request_reviews=None, request_avail_details=None,
            custom_filter_list=None, airport=None, special_offer_only=False,
            mime_text_type=None, max_iterations=None,
            request_meta_components=None,
    ):
        """Perform event search, returns list of Event objects.

        If no arguments are provided, then the full list of Events
        that are available will be returned.

        Args:
            keyword (string): keyword search key (default None)
            earliest_date (datetime): restrict to Events with Performances
                after this date (default None)
            latest_date (datetime): restrict to Events with Performances
                before this date (default None)
            country (string): ISO 3166-1 country code (default None)
            city (string): TSW city key (default None)
            latitude (float/int/string): (default None)
            longitude (float/int/string): (default None)
            radius (int/string): integer radius from lat/long point in
                km (default None)
            source (string): supplier system name (default None)
            area_code (string): TSW area code (default None)
            venue_code (string): TSW venue code (default None)
            event_code (string): TSW event code (default None)
            category (string): Event category search key (default None)
            event_id_list (list): Event Ids to return (default None)
            page_length (int): for pagination, number of Event objects
                to return (default None)
            page_number (int): for pagination, page number (default None)
            sort_by (string): defines sorting order, either top (best selling),
                user_rating or critic_rating (default None)
            auto_date_range (string): see settings.AUTO_DATE_RANGE for options
                (default None)
            request_source_info (boolean): flag for supplier info
                (default None)
            request_extra_info (boolean): flag for extra info (default None)
            request_video_iframe (boolean): flag for video (default None)
            request_cost_range (boolean): flag for cost range data
                (default True)
            request_media (list): List of strings representing the names
                of the images to request (default None)
            request_custom_fields (boolean): flag for custom fields
                (default True)
            request_reviews (boolean): flag for reviews (default None)
            request_avail_details (boolean): flag for avail_details
                (default None)
            custom_filter_list (list): custom filters to apply (default None)
            airport (string): airport code (default None)
            special_offer_only (boolean): flag for only returning events with
                special offers (default False)
            mime_text_type (string): desired text format for certain fields
                (most common options are 'html' and 'plain') (default None)
            max_iterations (int): used only in conjunction with
                special_offer_only. Sets the maximum number of iterations
                when retrieving special offers to prevent a full product search
                being performed.
            request_meta_components (boolean): flag for including an event's
                composite events (default False)


        Returns:
            list: List of Event objects
        """

        s_top = None
        s_user_rating = None
        s_critic_rating = None

        if sort_by:
            if sort_by == 'top':
                s_top = True
            elif sort_by == 'user_rating':
                s_user_rating = True
            elif sort_by == 'critic_rating':
                s_critic_rating = True

        if earliest_date or latest_date:

            date_range = ['', '']
            if earliest_date:
                date_range[0] = date_to_yyyymmdd(earliest_date)
            if latest_date:
                date_range[1] = date_to_yyyymmdd(latest_date)

            date_range = ':'.join(date_range)
        else:
            date_range = None

        if auto_date_range in settings.AUTO_DATE_RANGE:
            s_auto_range = auto_date_range
        else:
            s_auto_range = None

        if request_media is None:
            request_media = settings.REQUEST_MEDIA

        if custom_filter_list:
            s_cust_fltr = ' '.join(custom_filter_list)
        else:
            s_cust_fltr = None

        if event_id_list:
            event_token_list = ','.join(event_id_list)
        else:
            event_token_list = None

        crypto_block = self.get_crypto_block(
            method_name='start_session',
            password_required=False
        )

        if self.events:
            self._setup_instance_variables()

        resp_dict = self._do_core_event_search(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            s_keys=keyword, s_dates=date_range,
            s_coco=country, s_city=city,
            s_geo_lat=latitude, s_geo_long=longitude,
            s_geo_rad_km=radius, s_src=source, s_area=area_code,
            s_ven=venue_code, s_eve=event_code, s_class=category,
            event_token_list=event_token_list,
            request_source_info=request_source_info,
            request_extra_info=request_extra_info,
            request_video_iframe=request_video_iframe,
            request_cost_range=request_cost_range,
            request_media=request_media,
            request_custom_fields=request_custom_fields,
            request_reviews=request_reviews,
            request_avail_details=request_avail_details,
            s_top=s_top, s_user_rating=s_user_rating,
            s_critic_rating=s_critic_rating, s_auto_range=s_auto_range,
            page_length=page_length, page_number=page_number,
            s_cust_fltr=s_cust_fltr, s_airport=airport,
            special_offer_only=special_offer_only,
            mime_text_type=mime_text_type, max_iterations=max_iterations,
            request_meta_components=request_meta_components,
        )

        requested_data = {}

        if request_source_info:
            requested_data['source_info'] = True

        if request_extra_info:
            requested_data['extra_info'] = True

        if request_video_iframe:
            requested_data['video_iframe'] = True

        if request_cost_range:
            requested_data['cost_range'] = True

        if request_custom_fields:
            requested_data['custom_fields'] = True

        if request_reviews:
            requested_data['reviews'] = True

        if request_avail_details:
            requested_data['avail_details'] = True

        if request_media:
            requested_data['media'] = {}

            for m in request_media:
                requested_data['media'][m] = True

        if request_meta_components:
            requested_data['meta_components'] = True

        events = []

        for core_event in resp_dict['event']:
            # create event objects and append to list
            event = event_objs.Event(
                event_id=core_event.event_token,
                core_event=core_event,
                requested_data=requested_data,
                **self._internal_settings()
            )
            events.append(event)

            if event.city_code:
                self._add_city(event.city_code, event.city_desc)

            if event.country_code:
                self._add_country(event.country_code, event.country_desc)

            if event.categories:
                self._add_categories(event.categories)

            if request_cost_range and event.min_seatprice_float:
                self._min_seatprice_range.append(event.min_seatprice_float)

            if request_custom_fields and event.custom_fields:
                self._add_custom_fields(event.custom_fields)

            if event.custom_filters:
                self._add_custom_filters(event.custom_filters)

        self._set_crypto_block(
            crypto_block=resp_dict['crypto_block'],
            method_name='event_search'
        )

        self.events = events

        return events

    def _add_city(self, code, desc):
        if code in self._cities:
            self._cities[code]['count'] += 1

        else:
            self._cities[code] = {'description': desc, 'count': 1}

    def _add_country(self, code, desc):
        if code in self._countries:
            self._countries[code]['count'] += 1

        else:
            self._countries[code] = {'description': desc, 'count': 1}

    @staticmethod
    def _add_cat_to_dict(category, category_dict):
        if category.search_key in category_dict:
            category_dict[category.search_key]['count'] += 1

        else:
            category_dict[category.search_key] = {
                'count': 1,
                'category': category,
                'sub_categories': {},
            }

        if category.sub_categories:

            for sub in category.sub_categories:

                Core._add_cat_to_dict(
                    sub,
                    category_dict[category.search_key]['sub_categories']
                )

    def _add_categories(self, categories):

        for cat in categories:

            Core._add_cat_to_dict(
                category=cat,
                category_dict=self._categories
            )

    @staticmethod
    def _add_custom_field_to_dict(custom_field, custom_field_dict):
        if custom_field.code in custom_field_dict:
            custom_field_dict[custom_field.code]['count'] += 1

        else:
            custom_field_dict[custom_field.code] = {
                'count': 1,
                'custom_field': custom_field,
            }

    def _add_custom_fields(self, custom_fields):

        for cf in custom_fields:
            Core._add_custom_field_to_dict(
                custom_field=cf,
                custom_field_dict=self._custom_fields
            )

    @staticmethod
    def _add_custom_filter_to_dict(custom_filter, custom_filter_dict):
        if custom_filter.key in custom_filter_dict:
            custom_filter_dict[custom_filter.key]['count'] += 1

        else:
            custom_filter_dict[custom_filter.key] = {
                'count': 1,
                'custom_filter': custom_filter,
            }

    def _add_custom_filters(self, custom_filters):

        for cf in custom_filters:
            Core._add_custom_filter_to_dict(
                custom_filter=cf,
                custom_filter_dict=self._custom_filters
            )

    @property
    def event_cities(self):
        """Dictionary of cities in the search results.

        A dictionary of cities with the code, name and a count
        of how many times it appeared in the search.
        """
        return self._cities

    @property
    def event_categories(self):
        """Dictionary of Category objects in the search results.

        A dictionary of Category objects by their code, also contains
        the count of how many times it appeared and the sub categories.
        """
        return self._categories

    @property
    def event_countries(self):
        """Dictionary of countries in the search results.

        A dictionary of countries with the code, name and a count
        of how many times it appeared in the search.
        """
        return self._countries

    @property
    def event_price_range(self):
        """List of minimum prices in the search results.

        A list of float values of minimum prices of the Events
        in the search, where the information is available.
        Uses the Event.min_combined_price_float value.
        """
        if not self._min_seatprice_range:
            for e in self.events:
                if e.min_combined_price_float:
                    self._min_seatprice_range.append(
                        e.min_combined_price_float
                    )

        return self._min_seatprice_range

    @property
    def event_custom_fields(self):
        """Dictionary of CustomField objects in the search results.

        A dictionary of CustomField objects by their code, also contains
        the count of how many times it appeared.
        """
        return self._custom_fields

    @property
    def event_custom_filters(self):
        """Dictionary of CustomFilter objects in the search results.

        A dictionary of CustomFilter objects by their code, also contains
        the count of how many times it appeared.
        """
        return self._custom_filters

    def create_order(
            self, concessions=None, despatch_method=None):
        """Create a new Order.

        Order objects can be added to a Trolley, allowing multiple
        items to be purchased.

        Args:
            concessions (list): the list of Concession objects to
                create the Order with.
            despatch_method (DespatchMethod): the selected DespatchMethod
                for the Order.

        Returns:
            Order: An Order object
        """

        crypto_block = None

        if not concessions:
            concession_ids = None

            crypto_block = self.get_crypto_block(
                method_name='discount_options',
            )

        else:
            concession_ids = []
            for c in concessions:
                concession_ids.append(
                    c.concession_id
                )
                if not crypto_block:
                    crypto_block = self._get_crypto_block_for_object(
                        method_name='discount_options',
                        interface_object=c
                    )

        if despatch_method is not None:
            despatch_id = despatch_method.despatch_id
        else:
            despatch_id = None

        resp_dict = self.get_core_api().create_order(
            crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            discount_token=concession_ids, despatch_token=despatch_id
        )

        order = order_objs.Order(
            order_id=resp_dict['order_token'],
            core_order=resp_dict['order'],
            core_currency=resp_dict['currency'],
            **self._internal_settings()
        )

        self._set_crypto_block(
            crypto_block=resp_dict['crypto_block'],
            method_name='start_session'
        )

        return order

    def create_reservation(
            self, concessions=None, despatch_method=None):
        """Create a new Reservation object.

        Creates a Reservation object that contains only a single
        Order containing the passed values. It is equivalent to
        creating an Order, adding this to a Trolley and then
        reserving that Trolley.

        Args:
            concessions (list): the list of Concession objects to
                create the Reservation with.
            despatch_method (DespatchMethod): the selected DespatchMethod
                for the Reservation.

        Returns:
            Reservation: A Reservation object
        """

        crypto_block = None

        if not concessions:
            concession_ids = None

            crypto_block = self.get_crypto_block(
                method_name='discount_options',
            )

        else:
            concession_ids = []
            for c in concessions:
                concession_ids.append(
                    c.concession_id
                )
                if not crypto_block:
                    crypto_block = self._get_crypto_block_for_object(
                        method_name='discount_options',
                        interface_object=c
                    )

        if despatch_method is not None:
            despatch_id = despatch_method.despatch_id
        else:
            despatch_id = None

        resp_dict = self.get_core_api().create_order_and_reserve(
            crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            discount_token=concession_ids, despatch_token=despatch_id
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
