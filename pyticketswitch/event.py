from pyticketswitch.exceptions import IntegrityError
from pyticketswitch.cost_range import CostRange
from pyticketswitch.ticket_type import TicketType
from pyticketswitch.content import Content
from pyticketswitch.media import Media
from pyticketswitch.review import Review
from pyticketswitch.availability import AvailabilityDetails
from pyticketswitch.field import Field
from pyticketswitch.mixins import JSONMixin, PaginationMixin
from pyticketswitch.currency import CurrencyMeta


class Event(JSONMixin, object):
    """Describes a product in the ticketswitch system.

    Attributes:
        id (str): the identifier for the event.
        status (str): status of the event.
        description (str): human readable name for the event.
        source (str): the backend system from wich the event originates.
        source_code (str): the internal code for the backend system.
        event_type (str): the type of the event.
        venue (str): a human readable description of the venue.
        classes (dict): a dictionary of class descriptions that the event
            belongs to keyed on class identifier.
        filters (list): a list of filters that the event belongs to.
        postcode (str): venue post code.
        city (str): human readable venue city.
        city_code (str): venue city code
        country (str): human readable country name.
        country_code (str): ISO 3166-1 country code.
        latitude (float): latitude of the venue.
        longitude (float): longitude of the venue.
        max_running_time (int): maximum running time of a performance in
            minutes.
        min_running_time (int): minimum running time of a performance in
            minutes.
        show_performance_time (bool): indicates that the performance time
            for this event is relevant and should be shown.
        has_performances (bool): indicates that the event has performances.
        is_seated (bool): indicates the event is seated.
        needs_departure_date (bool): indicates that ticket purchases for this
            event will require a departure date.
        needs_duration (bool): indicates that ticket purchases for this
            event will require a duration.
        needs_performance (bool): indicates that you should ask your customer
            what date/time they want to attend this event on.
            See :ref:`Events that don't need performance selection
            <events_that_dont_need_performance_selection>` for more
            information.
        upsell_list (list): list of event id's.
        cost_range (:class:`CostRange <pyticketswitch.cost_range.CostRange>`):
            pricing summary from cached availability. Only present when
            requested.
        no_singles_cost_range (:class:`CostRange <pyticketswitch.cost_range.CostRange>`):
            pricining summary from cached availability. Only present when
            requested.
        cost_range_details (:class:`CostRangeDetails <pyticketswitch.cost_range.CostRangeDetails>`):
            summary pricing information broken down by availability. This is
            cached data. Only present when requested.
        content (dict): dictionary of
            :class:`Content <pyticketswitch.content.Content>` objects
            indexed on content name. Only present when requested.
        fields (dict): dictionary of
            :class:`Field <pyticketswitch.content.Content>` objects
            indexed on field name. Only present when requested.
        event_info (str): event info in plain text. Only present when
            requested.
        event_info_html (str): event info as HTML. Only present when requested.
        venue_addr (str): venue address in plain text. Only present when
            requested.
        venue_addr_html (str): venue address as HTML. Only present when requested.
        venue_info (str): venue info in plain text. Only present when
            requested.
        venue_info_html (str): venue info as HTML. Only present when requested.
        media (dict): dictionary of :class:`Media <pyticketswitch.media.Media>`
            objects indexed on media name. Only present when requested.
        reviews (list): list of :class:`Reviews <pyticketswitch.review.Review>`
            objects. Only present when requested.
        critic_review_percent (float): summary of critic review star rating.
            rated from 1 (lowest) to 5 (highest).
        availability_details (:class:`AvailabilityDetails <pyticketswitch.availability.AvailabilityDetails>`):
            summary of availability details from cached data. Only present when
            requested.
        component_events (list): list of :class:`Events <pyticketswitch.event.Event>`
            objects that comprise a meta event.
        valid_quantities (list): list of valid quanities available for
            purchase. from cached data, only available when requested by
            **get_events** or **get_event**.
        raw (dict): the raw data used to generate the object.
        is_addon (bool): indicates that the event is an addon.
        area_code (str): the internal code for the area. This is for internal
            use only.
        venue_code (str): the internal code for the venue. This is for internal
            use only.
        venue_is_enforced (bool): indicates if the venue is enforced. This is
            for internal use only.
        lingo_code (str): a code for the type of event, e.g. theatre or
            attraction. This is for internal use only.
    """

    def __init__(self, id_, status=None, event_type=None, source=None,
                 source_code=None, venue=None, description=None, postcode=None,
                 classes=None, filters=None, upsell_list=None, city=None,
                 city_code=None, country=None, country_code=None,
                 latitude=None, longitude=None, needs_departure_date=False,
                 needs_duration=False, addon_events=None, upsell_events=None,
                 needs_performance=False, has_performances=False,
                 is_seated=False, show_performance_time=False,
                 min_running_time=None, max_running_time=None, cost_range=None,
                 no_singles_cost_range=None, cost_range_details=None,
                 content=None, event_info_html=None, event_info=None,
                 venue_addr_html=None, venue_addr=None, venue_info=None,
                 venue_info_html=None, media=None, reviews=None,
                 critic_review_percent=None, availability_details=None,
                 component_events=None, valid_quantities=None, fields=None,
                 raw=None, is_add_on=None, area_code=None, venue_code=None,
                 venue_is_enforced=None, lingo_code=None):

        self.id = id_
        self.status = status
        self.description = description
        self.source = source
        self.source_code = source_code
        self.event_type = event_type
        self.venue = venue

        self.classes = classes
        self.filters = filters

        self.postcode = postcode
        self.city = city
        self.city_code = city_code
        self.country = country
        self.country_code = country_code
        self.latitude = latitude
        self.longitude = longitude

        self.max_running_time = max_running_time
        self.min_running_time = min_running_time

        self.show_performance_time = show_performance_time
        self.has_performances = has_performances
        self.is_seated = is_seated
        self.needs_departure_date = needs_departure_date
        self.needs_duration = needs_duration
        self.needs_performance = needs_performance

        self.addon_events = addon_events
        self.upsell_events = upsell_events
        # TODO This will be removed from the API soon
        self.upsell_list = upsell_list

        self.cost_range = cost_range
        self.no_singles_cost_range = no_singles_cost_range
        self.cost_range_details = cost_range_details

        self.content = content
        self.fields = fields
        self.event_info = event_info
        self.event_info_html = event_info_html
        self.venue_addr = venue_addr
        self.venue_addr_html = venue_addr_html
        self.venue_info = venue_info
        self.venue_info_html = venue_info_html

        self.media = media
        self.reviews = reviews
        self.critic_review_percent = critic_review_percent

        self.availability_details = availability_details

        self.component_events = component_events

        self.valid_quantities = valid_quantities
        self.raw = raw

        self.is_add_on = is_add_on

        self.venue_code = venue_code
        self.area_code = area_code
        self.venue_is_enforced = venue_is_enforced
        self.lingo_code = lingo_code

    @classmethod
    def class_dict_from_api_data(cls, data):
        """Creates a dict of Event data from a raw ticketswitch API call

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a event.

        Returns:
            dict: a new dict populated with the data from the api for creating
            an :class:`Event <pyticketswitch.event.Event>` object

        """

        id_ = data.get('event_id')

        if not id_:
            raise IntegrityError("event_id not found in event data", data=data)

        geo_data = data.get('geo_data', {})

        # the raw field 'has_no_perfs' is a negative flag, so I'm inverting it
        has_performances = not data.get('has_no_perfs', False)

        api_cost_range = data.get('cost_range', {})
        api_no_singles_cost_range = api_cost_range.get('no_singles_cost_range', {})
        cost_range = None
        no_singles_cost_range = None

        if api_cost_range:
            api_cost_range['singles'] = True
            cost_range = CostRange.from_api_data(api_cost_range)

        if api_no_singles_cost_range:
            api_no_singles_cost_range['singles'] = False
            no_singles_cost_range = CostRange.from_api_data(
                api_no_singles_cost_range)

        api_cost_range_details = data.get('cost_range_details', {})
        ticket_type_list = api_cost_range_details.get('ticket_type', [])
        cost_range_details = [
            TicketType.from_api_data(ticket_type)
            for ticket_type in ticket_type_list
        ]

        api_content = data.get('structured_info', {})
        content = {
            key: Content.from_api_data(value)
            for key, value in api_content.items()
        }

        fields = {
            field.get('custom_field_name'): Field.from_api_data(field)
            for field in data.get('custom_fields', {})
        }

        media = {}
        api_media = data.get('media', {})
        for asset in api_media.get('media_asset', []):
            new_media = Media.from_api_data(asset)
            media[new_media.name] = new_media

        api_video = data.get('video_iframe')
        if api_video:
            kwargs = {
                'secure_complete_url': api_video.get('video_iframe_url_when_secure'),
                'insecure_complete_url': api_video.get('video_iframe_url_when_insecure'),
                'caption': api_video.get('video_iframe_caption'),
                'caption_html': api_video.get('video_iframe_caption_html'),
                'width': api_video.get('video_iframe_width'),
                'height': api_video.get('video_iframe_height'),
                'name': 'video',
            }
            new_video = Media.from_api_data(kwargs)
            media['video'] = new_video

        api_reviews = data.get('reviews', {})
        reviews = [
            Review.from_api_data(api_review)
            for api_review in api_reviews.get('review', [])
        ]

        availability_details = AvailabilityDetails.from_api_data(
            data.get('avail_details', {}))
        api_component_events = data.get('meta_event_component_events', {})
        component_events = [
            Event.from_api_data(meta_event)
            for meta_event in api_component_events.get('event', [])
        ]

        lingo_code = None
        raw_lingo_data = data.get('lingo_data')
        if raw_lingo_data:
            lingo_code = raw_lingo_data.get('lingo_code')

        kwargs = {
            'id_': id_,
            'description': data.get('event_desc', None),
            'status': data.get('event_status'),
            'event_type': data.get('event_type'),
            'source_code': data.get('source_code'),
            'source': data.get('source_desc'),
            'venue': data.get('venue_desc'),

            'classes': data.get('classes'),
            #TODO: don't actually know what filters look like yet...
            'filters': data.get('custom_filter', []),
            'fields': fields,

            'postcode': data.get('postcode'),
            'city': data.get('city_desc'),
            'city_code': data.get('city_code'),
            'country': data.get('country_desc'),
            'country_code': data.get('country_code'),

            'latitude': geo_data.get('latitude'),
            'longitude': geo_data.get('longitude'),

            'max_running_time': data.get('max_running_time'),
            'min_running_time': data.get('min_running_time'),

            'has_performances': has_performances,
            'show_performance_time': data.get('show_perf_time', False),
            'is_seated': data.get('is_seated', False),
            'needs_departure_date': data.get('need_departure_date', False),
            'needs_duration': data.get('need_duration', False),
            'needs_performance': data.get('need_performance', False),

            'upsell_list': data.get('event_upsell_list', {}).get('event_id', []),

            'cost_range': cost_range,
            'no_singles_cost_range': no_singles_cost_range,
            'cost_range_details': cost_range_details,

            # extra info
            'event_info_html': data.get('event_info_html'),
            'event_info': data.get('event_info'),
            'venue_addr_html': data.get('venue_addr_html'),
            'venue_addr': data.get('venue_addr'),
            'venue_info': data.get('venue_info'),
            'venue_info_html': data.get('venue_info_html'),
            'content': content,

            'media': media,
            'reviews': reviews,
            'critic_review_percent': data.get('critic_review_percent'),

            'availability_details': availability_details,
            'component_events': component_events,
            'valid_quantities': data.get('valid_quantities'),
            'raw': data,
            'is_add_on': data.get('is_add_on'),
            'venue_code': data.get('venue_code'),
            'area_code': data.get('area_code'),
            'lingo_code': lingo_code,
        }

        return kwargs

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Event object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a event.

        Returns:
            :class:`Event <pyticketswitch.event.Event>`: a new
            :class:`Event <pyticketswitch.event.Event>` object
            populated with the data from the api.

        """

        kwargs = cls.class_dict_from_api_data(data)
        return cls(**kwargs)

    @classmethod
    def from_events_by_id_api_data(cls, data):
        """Creates a new Event object from API data from the events_by_id call.

        Args:
            data (dict): the part of the response from the ticketswitch
                `events_by_id` API call containing events and other data.

        Returns:
            :class:`Event <pyticketswitch.event.Event>`: a new
            :class:`Event <pyticketswitch.event.EVent>` object populated with
            the data from the API.

        """

        kwargs = cls.class_dict_from_api_data(data.get('event'))

        if data.get('add_ons'):
            addons=[
                Event.from_api_data(raw_addon)
                for raw_addon in data.get('add_ons')
            ]
            kwargs.update(addon_events=addons)

        if data.get('upsells'):
            upsells=[
                Event.from_api_data(raw_upsell)
                for raw_upsell in data.get('upsells')
            ]
            kwargs.update(upsell_events=upsells)

        if data.get('venue_is_enforced') is not None:
            kwargs.update(venue_is_enforced=data.get('venue_is_enforced'))

        return cls(**kwargs)

    def __repr__(self):
        return u'<Event {}:{}>'.format(
            self.id, self.description.encode('ascii', 'ignore'))


class EventMeta(PaginationMixin, CurrencyMeta):
    """Meta information about a set of events

    Attributes:
        currencies (dict): dictionary of
            :class:`Currency <pytickectswitch.currency.Currency>`) objects
            indexed on currency code.
        default_currency_code (str): unless other wise specified all prices in
            the related response will be in this currency.
        desired_currency_code (str):
            the currency that the user account is expecting. Useful for
            conversions.
        page_length (int): the number of items per page.
        page_number (int): the current page.
        pages_remaining (int): the number of pages remaining.
        results_remaining (int): the total number of remaining results after
            the current page.
        total_results (int): the total number of results.
    """
    pass
