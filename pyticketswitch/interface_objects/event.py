# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import datetime
from copy import deepcopy
from operator import attrgetter, itemgetter

from pyticketswitch import settings
from pyticketswitch.api_exceptions import InvalidId
from pyticketswitch.util import (
    date_to_yyyymmdd_or_none, dates_in_range, hhmmss_to_time, resolve_boolean,
    to_int_or_none, yyyymmdd_to_date
)

from six.moves import range

from . import availability as avail_objs
from .base import CostRangeMixin, InterfaceObject


class Category(object):
    """Object representing a TSW event category.

    In the XML API documentation this is also referred to as the
    event class
    """

    def __init__(
        self,
        core_class=None,
        core_subclass=None
    ):
        self._core_class = core_class
        if not core_class:
            self._core_subclass = core_subclass
        self._sub_categories = None

    @property
    def code(self):
        if self._core_class:
            return self._core_class.class_code
        else:
            return self._core_subclass.subclass_code

    @property
    def description(self):
        if self._core_class:
            return self._core_class.class_desc
        else:
            return self._core_subclass.subclass_desc

    @property
    def is_main(self):
        """Flag to indicate if this is the primary category for the event."""
        if self._core_class:
            return resolve_boolean(self._core_class.is_main_class)
        else:
            return resolve_boolean(self._core_subclass.is_main_subclass)

    @property
    def search_key(self):
        """String representation for use in the event search"""
        if self._core_class:
            return self._core_class.search_key
        else:
            return self._core_subclass.search_key

    @property
    def slug_search_key(self):
        """Slug of the search key"""
        return self.search_key.replace('/', '_')

    @staticmethod
    def deslug_search_key(slug_search_key):
        """Returns the search key from a slugged search key.

        Args:
            slug_search_key (string): A slug_search_key

        Returns:
            string: The search_key
        """
        return slug_search_key.replace('_', '/')

    @property
    def sub_categories(self):
        """List of sub categories"""
        if self._core_class and self._sub_categories is None:

            self._sub_categories = []

            for sub in self._core_class.subclasses:

                self._sub_categories.append(
                    Category(core_subclass=sub)
                )

        return self._sub_categories


class CustomField(object):
    """Represents a TSW event custom field."""

    def __init__(
        self,
        core_custom_field,
    ):
        self._core_custom_field = core_custom_field

    @property
    def description(self):
        if self._core_custom_field.custom_field_label:
            return self._core_custom_field.custom_field_label
        return None

    @property
    def code(self):
        return self._core_custom_field.custom_field_name

    @property
    def key(self):
        return self.code

    @property
    def values(self):
        return self._core_custom_field.custom_field_data.split(', ')


class CustomFilter(object):
    """Represents a TSW event custom filter."""

    def __init__(
        self,
        core_custom_filter,
    ):
        self._core_custom_filter = core_custom_filter

    @property
    def description(self):
        return self._core_custom_filter.custom_filter_desc

    @property
    def key(self):
        return self._core_custom_filter.custom_filter_key


class StructuredContentItem(object):
    """Represents an item of Structured Content.

    For example, Events may have an associated 'Overview' Structured
    Content Item, which would have a key of 'overview'. The name would
    then be the translated name of the item (so 'Overview' in English)
    and the value would be the translated value of this item for the Event.
    """

    def __init__(
        self,
        core_structured_info_item,
    ):
        self._core_structured_info_item = core_structured_info_item

    @property
    def key(self):
        return self._core_structured_info_item.key

    @property
    def name(self):
        return self._core_structured_info_item.name

    @property
    def value(self):
        return self._core_structured_info_item.value


class Event(InterfaceObject, CostRangeMixin):
    """Object that represents a TSW event.

    Operations relating to TSW events are accessible through here,
    e.g. retrieving event information, listing performances, etc.

    The Event Id (event_id) is the only required argument apart from
    configuration settings, which are explained in the Core object
    constructor. The other arguments are for internal use.

    Inherits from the CostRangeMixin class, so these functions are
    available.

    Args:
        event_id (string): The Id of the Event object.
        settings (kwargs): See Core constructor.
    """

    _attr_request_map = {
        'event_info': 'extra_info',
        'venue_info': 'extra_info',
        'venue_addr': 'extra_info',
        'source_t_and_c': 'source_info',
        'critic_review_percent': 'extra_info',
        'user_review_percent': 'extra_info',
        'reviews': 'reviews',
        'cost_range': 'cost_range',
        'video_iframe': 'video_iframe',
        'custom_fields': 'custom_fields',
        'event_medias': 'media',
        'structured_info': 'extra_info_only',
        'event_quantity_options': 'extra_info_only',
        'avail_details': 'avail_details',
        'component_events': 'extra_info',
    }

    def __init__(
        self,
        event_id,
        core_event=None,
        requested_data=None,
        **settings
    ):

        self.event_id = event_id
        self._core_event = core_event
        self._performance_calendar = {}
        self._performances = None
        self._need_departure_date = None
        self._categories = None
        self._critic_reviews = None
        self._user_reviews = None
        self._video = None
        self._months = None
        self._custom_fields = None
        self._custom_filters = None
        self._perfs_have_usage_date = None
        self._perfs_have_required_info = None
        self._has_single_false_perf = None
        self._structured_content = None
        self._valid_ticket_quantities = None
        self._avail_details = None
        self._component_events = None

        if not requested_data:
            self._requested_data = {}
        else:
            self._requested_data = deepcopy(requested_data)

        super(Event, self).__init__(**settings)

    def __getstate__(self):
        """This method determines what data will be pickled, and therefore,
        what data will be stored in the event cache.
        Any attributes that should not be stored in the cache should be
        set to None in the returned dictionary.
        """

        d = super(Event, self).__getstate__()

        # Don't cache avail details
        d['_avail_details'] = None
        # Remove avail details from requested data to make sure it is
        # requested again next time
        if self._attr_request_map['avail_details'] in self._requested_data:
            del self._requested_data[self._attr_request_map['avail_details']]

        return d

    def _get_cache_key(self):
        return self.event_id

    def _get_core_event_attr(self, attr_name):

        if not self._core_event:
            try:
                self.get_details()
            except InvalidId:
                return None

        attr_value = getattr(self._core_event, attr_name, None)

        if not attr_value:
            if attr_name in self._attr_request_map:
                request_val = self._attr_request_map[attr_name]

                if request_val not in self._requested_data:
                    self.get_details()

                    attr_value = getattr(self._core_event, attr_name, None)

        return attr_value

    # Overridden function for CostRangeMixin
    def _get_core_cost_range(self):
        return self._get_core_event_attr('cost_range')

    @property
    def description(self):
        return self._get_core_event_attr('event_desc')

    @property
    def information(self):
        return self._get_core_event_attr('event_info')

    @property
    def venue_desc(self):
        return self._get_core_event_attr('venue_desc')

    @property
    def venue_info(self):
        return self._get_core_event_attr('venue_info')

    @property
    def venue_addr(self):
        return self._get_core_event_attr('venue_addr')

    @property
    def supplier_code(self):
        return self._get_core_event_attr('source_code')

    @property
    def supplier_desc(self):
        return self._get_core_event_attr('source_desc')

    @property
    def supplier_t_and_c(self):
        return self._get_core_event_attr('source_t_and_c')

    @property
    def city_code(self):
        return self._get_core_event_attr('city_code')

    @property
    def city_desc(self):
        return self._get_core_event_attr('city_desc')

    @property
    def country_code(self):
        return self._get_core_event_attr('country_code')

    @property
    def country_desc(self):
        return self._get_core_event_attr('country_desc')

    @property
    def is_seated(self):
        return resolve_boolean(
            self._get_core_event_attr('is_seated')
        )

    @property
    def has_no_perfs(self):
        return resolve_boolean(
            self._get_core_event_attr('has_no_perfs')
        )

    @property
    def event_type(self):
        return self._get_core_event_attr('event_type')

    @property
    def upsell_list(self):
        return self._get_core_event_attr('event_upsell_list')

    @property
    def show_perf_time(self):
        return resolve_boolean(
            self._get_core_event_attr('show_perf_time')
        )

    @property
    def need_performance(self):
        return resolve_boolean(
            self._get_core_event_attr('need_performance')
        )

    @property
    def need_duration(self):
        return resolve_boolean(
            self._get_core_event_attr('need_duration')
        )

    @property
    def valid_ticket_quantities(self):
        """Returns a list of the valid ticket quantities."""

        if self._valid_ticket_quantities is None:

            self._valid_ticket_quantities = []
            # Call extra_info to make sure we get latest data
            # (Important for redeem users for example, since we don't want
            # to get old cached data)
            self.get_details()

            if self.cached_valid_ticket_quantities:
                self._valid_ticket_quantities = (
                    self.cached_valid_ticket_quantities
                )

            else:
                quantity_options_dict = self._get_core_event_attr(
                    'event_quantity_options'
                )
                if quantity_options_dict:
                    valid_list = quantity_options_dict.get(
                        'valid_quantity', []
                    )
                    self._valid_ticket_quantities = [
                        int(x) for x in valid_list
                    ]

        return self._valid_ticket_quantities

    @property
    def latitude(self):
        geo_data = self._get_core_event_attr('geo_data')

        if geo_data:
            return geo_data.latitude

        else:
            return None

    @property
    def longitude(self):
        geo_data = self._get_core_event_attr('geo_data')

        if geo_data:
            return geo_data.longitude

        else:
            return None

    @property
    def critic_review_percent(self):
        rev_per = self._get_core_event_attr('critic_review_percent')

        if rev_per:
            if rev_per == '0':

                rev_per = None
            else:
                rev_per = rev_per + '%'

        return rev_per

    @property
    def user_review_percent(self):
        rev_per = self._get_core_event_attr('user_review_percent')

        if rev_per:
            if rev_per == '0':

                rev_per = None
            else:
                rev_per = rev_per + '%'

        return rev_per

    def _build_reviews(self):
        self._critic_reviews = []
        self._user_reviews = []
        for r in self._get_core_event_attr('reviews'):

            is_user_bool = resolve_boolean(r.is_user_review)

            review = Review(
                core_review=r, is_user_review=is_user_bool
            )

            if is_user_bool:
                self._user_reviews.append(review)
            else:
                self._critic_reviews.append(review)

    @property
    def critic_reviews(self):
        """List of Review objects."""
        if self._critic_reviews is None:
            self._build_reviews()

        return self._critic_reviews

    @property
    def user_reviews(self):
        """List of Review objects."""
        if self._user_reviews is None:
            self._build_reviews()

        return self._user_reviews

    @property
    def categories(self):
        """List of Category objects."""

        if self._categories is None:

            self._categories = []

            for c in self._get_core_event_attr('classes'):
                #  self._categories[c.class_code] = c.class_desc

                self._categories.append(Category(core_class=c))

        return self._categories

    @property
    def video(self):
        """Video object for this Event."""
        if self._video is None:

            core_video = self._get_core_event_attr('video_iframe')

            if core_video:

                self._video = Video(
                    core_video_iframe=core_video
                )

        return self._video

    @property
    def start_date(self):
        start_date = None
        date_range_start = self._get_core_event_attr('date_range_start')

        if date_range_start:
            start_date = yyyymmdd_to_date(
                date_range_start['date_yyyymmdd']
            )

        return start_date

    @property
    def end_date(self):
        end_date = None
        date_range_end = self._get_core_event_attr('date_range_end')

        if date_range_end:
            end_date = yyyymmdd_to_date(
                date_range_end['date_yyyymmdd']
            )

        return end_date

    @property
    def custom_fields(self):
        """Returns list of CustomField objects"""
        if self._custom_fields is None:

            self._custom_fields = []

            for c in self._get_core_event_attr('custom_fields'):
                self._custom_fields.append(
                    CustomField(core_custom_field=c)
                )

        return self._custom_fields

    @property
    def custom_filters(self):
        """Returns list of CustomFilter objects"""
        if self._custom_filters is None:

            self._custom_filters = []

            for c in self._get_core_event_attr('custom_filters'):
                self._custom_filters.append(
                    CustomFilter(core_custom_filter=c)
                )

        return self._custom_filters

    def _get_image(self, name, request_all_images=True):

        make_request = True

        if (
            self._attr_request_map['event_medias'] in
            self._requested_data
        ):

            for req in self._requested_data[
                self._attr_request_map['event_medias']
            ].keys():
                if req in name or req == name:
                    make_request = False
                    break

        if make_request:
            if request_all_images:
                request_media = None
            else:
                request_media = [name]

            self.get_details(request_media=request_media)

        event_medias = self._get_core_event_attr('event_medias')

        if event_medias:
            for i in event_medias:
                if i.name == name:
                    return i.secure_complete_url

        return None

    def get_large_image(self):
        return self._get_image(settings.LARGE_IMAGE)

    def get_large_images(self):

        images = []

        i = 0

        for name in settings.LARGE_IMAGE_LIST:

            url = self._get_image(name)

            if url:
                images.append(
                    {'url': url, 'index': i}
                )
                i = i + 1

        return images

    def get_medium_image(self):
        return self._get_image(settings.MEDIUM_IMAGE)

    def get_small_image(self):
        return self._get_image(settings.SMALL_IMAGE)

    def get_marquee_image(self):
        return self._get_image(settings.MARQUEE_IMAGE)

    def get_seating_plan(self):
        return self._get_image(settings.SEATING_IMAGE)

    def get_supplier_image(self):
        return self._get_image(settings.SUPPLIER_IMAGE)

    def get_details(
        self, request_media=None, source_info=True,
        request_reviews=True, request_avail_details=None,
        mime_text_type='html',
    ):
        """Retrieves data for the current Event.

        This is called internally to get information about
        the current Event, but can be called explicitly
        if required (could reduce the number of API calls
        in some circumstances).
        """
        from . import core as core_objs

        if request_media is None:
            request_media = settings.REQUEST_MEDIA

        crypto_block = self.get_crypto_block(
            method_name='event_search',
        )

        detailed_event = None
        extra_info_called = False

        if crypto_block:

            detailed_event = self.get_core_api().extra_info(
                crypto_block=crypto_block,
                upfront_data_token=self.settings['upfront_data_token'],
                event_token=self.event_id,
                request_media=request_media, source_info=source_info,
                request_avail_details=request_avail_details,
                mime_text_type=mime_text_type,
            )

            request_reviews = True
            extra_info_called = True

        else:
            core = core_objs.Core(
                **self._internal_settings()
            )
            events = core.search_events(
                event_id_list=[self.event_id], request_media=request_media,
                request_source_info=source_info, request_extra_info=True,
                request_video_iframe=True, request_cost_range=True,
                request_custom_fields=True, request_reviews=request_reviews,
                request_avail_details=request_avail_details,
                request_meta_components=True, mime_text_type=mime_text_type,
            )
            if events:
                detailed_event = events[0]._core_event

            else:
                raise InvalidId(
                    call="event_search",
                    description="Event does not exist"
                )

        if self._core_event is None:
            self._core_event = detailed_event

        else:
            self._core_event.add_extra_info(detailed_event)

        self._requested_data['extra_info'] = True
        self._requested_data['video_iframe'] = True
        self._requested_data['cost_range'] = True
        self._requested_data['custom_fields'] = True

        if source_info:
            self._requested_data['source_info'] = True

        if request_media:
            if 'media' not in self._requested_data:
                self._requested_data['media'] = {}
            for m in request_media:
                self._requested_data['media'][m] = True

        if request_reviews:
            self._requested_data['reviews'] = True

        if request_avail_details:
            self._requested_data['avail_details'] = True

        if extra_info_called:
            self._requested_data['extra_info_only'] = True

    @property
    def performance_calendar(self):
        """Dictionary of Performances for this Event by date.

        Performance objects are returned as a dictionary,
        organised by Year -> Month -> Day, with a list of
        all the performances that day.
        """
        if not self._performance_calendar:

            for performance in self.performances:

                if performance.date:
                    year = performance.date.year
                    month = performance.date.month
                    day = performance.date.day

                    if performance.time:
                        time_desc = '.'.join((str(
                            int(performance.time.strftime('%I'))),
                            performance.time.strftime('%M%p')
                        ))
                    else:
                        time_desc = self.settings['no_time_descr']

                    if year not in self._performance_calendar:
                        self._performance_calendar[year] = {}

                    if month not in self._performance_calendar[year]:
                        self._performance_calendar[year][month] = {}

                    if (
                        day not in
                        self._performance_calendar[year][month]
                    ):
                        self._performance_calendar[year][month][day] = []

                    if (
                        time_desc not in
                        self._performance_calendar[year][month][day]
                    ):
                        self._performance_calendar[year][month][day].append(
                            {'time': time_desc, 'performance': performance}
                        )

        return self._performance_calendar

    def _get_search_crypto(self):
        from . import core as core_objs

        crypto_block = self.get_crypto_block(
            method_name='event_search',
        )

        if not crypto_block:

            core = core_objs.Core(
                **self._internal_settings()
            )
            events = core.search_events(
                event_id_list=[self.event_id]
            )
            if events:
                self._core_event = events[0]._core_event
            else:
                raise InvalidId(
                    call="event_search",
                    description="Event does not exist"
                )

            crypto_block = self.get_crypto_block(
                method_name='event_search',
            )

        return crypto_block

    @property
    def months(self):
        """List of months that have performances.

        Returns a list of dictionaries with 'month' and 'year'
        keys. Each dictionary represents a month that contains
        Performances of this Event.
        """
        if self._months is None:
            return self.get_valid_months()
        else:
            return self._months

    @months.setter
    def months(self, value):
        self._months = value

    def get_valid_months(self):
        """Retrieves the list of months that contain performances.

        This method is called internally by the 'months' property,
        but can be called explicitly if required.
        """

        crypto_block = self._get_search_crypto()

        resp_dict = self.get_core_api().month_options(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            event_token=self.event_id
        )

        months = []

        for m in resp_dict['months']:
            months.append({
                'year': int(m.year_number),
                'month': int(m.month_number),
            })

        self.months = sorted(
            months, key=itemgetter('year', 'month')
        )

        return self.months

    @property
    def performances(self):
        """List of Performance objects for this Event."""
        if self._performances is None:
            return self.get_performances()
        else:
            return self._performances

    @performances.setter
    def performances(self, value):
        self._performances = value

    @property
    def need_departure_date(self):
        """Flag to indicate that a departure date is required.

        Value can be True/False (a departure date is/isn't required)
        or None (the data could not be retrieved/unknown).
        See the API documentation for more information about the
        'need_departure_date' flag.
        """

        if self._need_departure_date is None:
            need_departure_date = self._get_core_event_attr(
                'need_departure_date'
            )

            if need_departure_date:

                self._need_departure_date = resolve_boolean(
                    need_departure_date
                )

            else:
                self.get_performances()

        if self._need_departure_date:
            return self._need_departure_date
        else:
            return None

    @need_departure_date.setter
    def need_departure_date(self, value):
        if value is None:
            self._need_departure_date = False
        else:
            self._need_departure_date = value

    @property
    def perfs_have_usage_date(self):
        """Flag to indicate if the Performances are using usage dates.

        True if the Performances for this Event are using a usage date
        (see the API documentation for more information).
        """
        if self._perfs_have_usage_date is None:
            self.get_performances()

        return self._perfs_have_usage_date

    @perfs_have_usage_date.setter
    def perfs_have_usage_date(self, value):
        self._perfs_have_usage_date = value

    @property
    def perfs_have_required_info(self):
        """Flag to indicate if any of the Performances have
        'required_info' text.

        Value will be True if any of the Performances for this
        Event has required_info text that must be displayed.
        """
        if self.perfs_have_usage_date or self.has_single_false_perf:
            return None

        elif self._perfs_have_required_info is None:
            self.get_performances()

        return self._perfs_have_required_info

    @perfs_have_required_info.setter
    def perfs_have_required_info(self, value):
        self._perfs_have_required_info = value

    @property
    def has_single_false_perf(self):
        """Flag to indicate that there is only one Performance.

        The value will be True if this Event only has a single
        Performance that has been created by this library to
        standardise the booking process. If this flag is True,
        there is no need to display the Performances for this
        Event.
        """
        if self.need_performance or self.need_departure_date:
            return False

        elif self._has_single_false_perf is None:
            self.get_performances()

        return self._has_single_false_perf

    @has_single_false_perf.setter
    def has_single_false_perf(self, value):
        self._has_single_false_perf = value

    @property
    def show_performances(self):
        """Flag to indicate whether to display individual Performances.

        Value will be False if there is no need to show any more
        information about a Performance other than the date.
        """
        if self.has_single_false_perf:
            return False
        elif not self.show_perf_time:
            if self.perfs_have_usage_date:
                return False
            elif not self.perfs_have_required_info:
                return False

        return True

    def get_performances(self, earliest_date=None, latest_date=None, **kwargs):
        """Retrieves the Performances for this Event.

        Returns the list of Performances for the Event, called internally
        by several other methods, it calls the 'date_time_options' API method.
        The 'performances' property should be used to get this information
        unless a specific date range is required.

        Args:
            earliest_date (datetime.date): restrict the list of
                Performances to be later than this date.
            latest_date (datetime.date): restrict the list of
                Performances to be earlier than this date.

        Returns:
            list: List of Performance objects
        """
        from . import performance as perf_objs

        crypto_block = self._get_search_crypto()

        resp_dict = self.get_core_api().date_time_options(
            crypto_block=crypto_block,
            upfront_data_token=self.settings['upfront_data_token'],
            event_token=self.event_id,
            earliest_date=date_to_yyyymmdd_or_none(earliest_date),
            latest_date=date_to_yyyymmdd_or_none(latest_date),
            request_cost_range=True,
            **kwargs
        )

        performances = []

        self.need_departure_date = resolve_boolean(
            resp_dict['need_departure_date']
        )

        if 'using_perf_list' in resp_dict:

            self.perfs_have_required_info = resolve_boolean(
                resp_dict['has_perf_names']
            )

            self.perfs_have_usage_date = False
            self.has_single_false_perf = False

            for p in resp_dict['using_perf_list']['performances']:

                if self.need_departure_date:
                    departure_date = p.date
                else:
                    departure_date = None

                performances.append(
                    perf_objs.Performance.from_event_and_perf_token(
                        event=self,
                        perf_token=p.perf_token,
                        core_performance=p,
                        departure_date=departure_date,
                        **self._internal_settings()
                    )
                )

        elif 'using_usage_date' in resp_dict:

            self.perfs_have_usage_date = True
            self.has_single_false_perf = False
            self.perfs_have_required_info = False

            performances = self._build_performances_from_usage(
                usage_date_dict=resp_dict['using_usage_date'],
                need_departure_date=self.need_departure_date,
                latest_date=latest_date
            )

        else:

            self.perfs_have_usage_date = False
            self.has_single_false_perf = True
            self.perfs_have_required_info = False

            performances.append(perf_objs.Performance.from_event_only(
                event=self,
                **self._internal_settings()
            ))

        self.performances = performances

        self._set_crypto_for_object(
            crypto_block=resp_dict['crypto_block'],
            method_name='date_time_options',
            interface_object=self
        )

        return performances

    def _build_performances_from_usage(
        self, usage_date_dict, need_departure_date, latest_date
    ):
        from . import performance as perf_objs

        inv_dates = []

        if 'invalid_range' in usage_date_dict:
            usage_inv_range = usage_date_dict['invalid_range']
            if type(usage_inv_range) == list:

                for inv in usage_inv_range:
                    inv_first_date = yyyymmdd_to_date(
                        inv['first_invalid_date_yyyymmdd']
                    )

                    inv_last_date = yyyymmdd_to_date(
                        inv['last_invalid_date_yyyymmdd']
                    )

                    inv_dates.extend(dates_in_range(
                        inv_first_date, inv_last_date
                    ))

            else:
                inv_first_date = yyyymmdd_to_date(
                    usage_inv_range['first_invalid_date_yyyymmdd']
                )

                inv_last_date = yyyymmdd_to_date(
                    usage_inv_range['last_invalid_date_yyyymmdd']
                )

                inv_dates.extend(dates_in_range(inv_first_date, inv_last_date))

        inv_weekdays = []

        if 'invalid_weekday' in usage_date_dict:
            usage_inv_weekdays = usage_date_dict['invalid_weekday']

            if type(usage_inv_weekdays) == list:

                for inv_weekday in usage_inv_weekdays:
                    inv_weekdays.append(inv_weekday['weekday_number'])

            else:
                inv_weekdays.append(int(usage_inv_weekdays['weekday_number']))

        performances = []

        first_date = yyyymmdd_to_date(
            usage_date_dict['first_valid_date_yyyymmdd']
        )

        last_date = yyyymmdd_to_date(
            usage_date_dict['last_valid_date_yyyymmdd']
        )

        if latest_date:

            if latest_date < last_date:
                last_date = latest_date

        delta = last_date - first_date

        for i in range(delta.days + 1):
            perf_date = first_date + datetime.timedelta(days=i)

            if (
                perf_date.isoweekday() not in inv_weekdays and
                perf_date not in inv_dates
            ):

                if need_departure_date:
                    departure_date = perf_date
                else:
                    departure_date = None

                performances.append(
                    perf_objs.Performance.from_event_and_usage_date(
                        event=self,
                        usage_date=perf_date,
                        departure_date=departure_date,
                        **self._internal_settings()
                    )
                )

        return performances

    @property
    def structured_content(self):
        """Dictionary of StructuredContentItem objects for this Event.

        The dictionary keys will be the key of the StructuredContentItem.
        """
        if self._structured_content is None:

            self._structured_content = {}

            si_dict = self._get_core_event_attr('structured_info')

            for key, item in si_dict.items():
                self._structured_content[key] = StructuredContentItem(
                    core_structured_info_item=item,
                )

        return self._structured_content

    def _build_avail_details(self):
        """Builds a list of AvailDetail objects
        """

        self._avail_details = []

        ad_attr = self._get_core_event_attr('avail_details')
        if ad_attr:
            for tt in ad_attr.get('ticket_types', []):
                for pb in tt.get('price_bands', []):
                    for ad in pb.get('avail_details', []):
                        self._avail_details.append(
                            avail_objs.AvailDetail(
                                core_avail_detail=ad,
                                ticket_type_code=tt['ticket_type_code'],
                                ticket_type_desc=tt['ticket_type_desc'],
                                price_band_code=pb['price_band_code'],
                                price_band_desc=pb['price_band_desc'],
                            )
                        )

    @property
    def avail_details(self):
        """Get detailed availability and pricing information for this event.
        """

        if self._avail_details is None:

            if (
                self._attr_request_map['avail_details'] not in
                self._requested_data
            ):
                self.get_details(request_avail_details=True)

            self._build_avail_details()

        return self._avail_details

    @property
    def avail_details_by_price(self):
        """Avail details sorted by combined price
        """

        return sorted(
            self.avail_details,
            key=attrgetter('price_combined_float')
        )

    @property
    def avail_details_by_cheapest_ticket_type(self):
        """Avail details sorted by cheapest ticket type then price. Avail
        details with the same ticket type and pricing will be combined to
        reduce duplicates.
        """
        order_dict = {}

        i = 0
        for ad in self.avail_details_by_price:
            if ad.ticket_type_desc not in order_dict:
                order_dict[ad.ticket_type_desc] = i
                i += 1

        ad_sorted = sorted(
            self.avail_details, key=lambda x: (
                order_dict[x.ticket_type_desc],
                x.price_combined_float
            )
        )

        # Combine rows for which the ticket type and pricing info is the same
        ad_final = []
        for ad in ad_sorted:
            if ad_final and ad.is_same_ticket_and_price(ad_final[-1]):
                ad_final[-1] = ad.combine(ad_final[-1])
            else:
                ad_final.append(ad)

        return ad_final

    @property
    def is_meta_event(self):
        if self.event_type == 'meta_event':
            return True
        return False

    @property
    def component_events(self):
        if self._component_events is None:

            self._component_events = []

            for sub_event in self._get_core_event_attr('component_events'):
                self._component_events.append(
                    Event(
                        event_id=sub_event.event_token,
                        core_event=sub_event,
                        **self._internal_settings()
                    )
                )

        return self._component_events


class Video(object):
    """Object representing a TSW video iframe element."""

    def __init__(
        self,
        core_video_iframe,
    ):
        self._core_video_iframe = core_video_iframe

    @property
    def height(self):
        return to_int_or_none(
            self._core_video_iframe.video_iframe_height
        )

    @property
    def width(self):
        return to_int_or_none(
            self._core_video_iframe.video_iframe_width
        )

    @property
    def host(self):
        return self._core_video_iframe.video_iframe_host

    @property
    def path(self):
        return self._core_video_iframe.video_iframe_path

    @property
    def supports_https(self):
        """Boolean flag indicating HTTPS support."""
        return resolve_boolean(
            self._core_video_iframe.video_iframe_supports_https
        )

    @property
    def secure_url(self):

        if self._core_video_iframe.video_iframe_url_when_secure:
            return self._core_video_iframe.video_iframe_url_when_secure

        else:
            "https://{host}{path}".format(
                host=self.host, path=self.path
            )

    @property
    def insecure_url(self):

        if self._core_video_iframe.video_iframe_url_when_insecure:
            return self._core_video_iframe.video_iframe_url_when_insecure

        else:
            "http://{host}{path}".format(
                host=self.host, path=self.path
            )


class Review(object):
    """Object representing a TSW event review.

    Attributes:
        is_user_review (boolean): Indicates if it is a user review,
            otherwise it is a critic review.
    """

    def __init__(
        self,
        core_review=None,
        is_user_review=None
    ):
        self._core_review = core_review
        self.is_user_review = is_user_review

        if core_review is not None:
            self._set_datetime(
                date_yyyymmdd=core_review.review_date_yyyymmdd,
                time_hhmmss=core_review.review_time_hhmmss
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

    @property
    def title(self):
        return self._core_review.review_title

    @property
    def body(self):
        return self._core_review.review_body

    @property
    def author(self):
        return self._core_review.review_author

    @property
    def date_desc(self):
        return self._core_review.review_date_desc

    @property
    def time_desc(self):
        return self._core_review.review_time_desc

    @property
    def star_rating(self):
        return to_int_or_none(
            self._core_review.star_rating
        )
