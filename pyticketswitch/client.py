import decimal
import requests
import logging
import six
import pyticketswitch
from pyticketswitch import exceptions, utils
from pyticketswitch.event import Event, EventMeta
from pyticketswitch.performance import Performance, PerformanceMeta
from pyticketswitch.availability import AvailabilityMeta
from pyticketswitch.ticket_type import TicketType
from pyticketswitch.send_method import SendMethod
from pyticketswitch.month import Month
from pyticketswitch.discount import Discount
from pyticketswitch.trolley import Trolley
from pyticketswitch.reservation import Reservation
from pyticketswitch.status import Status
from pyticketswitch.user import User
from pyticketswitch.currency import CurrencyMeta
from pyticketswitch.callout import Callout


logger = logging.getLogger(__name__)

POST = 'post'
GET = 'get'
DEFAULT_ROOT_URL = "https://api.ticketswitch.com"


class Client(object):
    """Client wraps the ticketswitch f13 API.

    Client contains auth details and provides helper methods for calling
    the f13 endpoints.

    Attributes:
        user (str): user id used to connect to the api.
        password (str): Password for the user used to connect to the api.
        url (:obj:`str`, optional): Root url for the API.
            Defaults to https://api.ticketswitch.com.
        sub_user (:obj:`str`, optional): the sub user is used to idicate a
            specific agent of the holder of the main users account requests
            is being made for. For example a travel agent might hold the main
            account but an agent in the london office might specify `london` as
            their sub user, whereas an agent in belfast might specify `belfast`
            or even something more specific. Defaults to None
        language (:obj:`str`, optional): prefered IETF language tag. When
            available this will translate text to the specified language. When
            None language defaults to user's preference. Defaults to None.
        tracking_id (:obj:`str`, optional): a tracking ID to use with requests
        use_decimal (bool): parse JSON numbers as decimal. Default is `False`
            but this use is deprecated and decimals are recommended.
        **kwargs: Additional arbitrary key word arguments to keep with the
            object.

    """

    def __init__(self, user, password, url=DEFAULT_ROOT_URL, sub_user=None,
                 language=None, tracking_id=None, use_decimal=False, **kwargs):
        self.user = user
        self.password = password
        self.url = url
        self.sub_user = sub_user
        self.language = language
        self.tracking_id = tracking_id
        self.use_decimal = use_decimal
        self.kwargs = kwargs

    def get_url(self, end_point):
        """Get the url for a given endpoint

        Args:
            end_point (str): the target api end point, for example events.v1 or
                performances.v1

        Returns:
            str: the full url for the given endpoint, contains the base url and
            endpoint

        """

        url = "{url}/f13/{end_point}/".format(
            url=self.url,
            end_point=end_point,
        )
        return url

    @utils.deprecated
    def get_auth_params(self):
        """Get the authentication parameters for inclusion in requests.

        **This method is deprecated** - please use `get_extra_params` instead.

        This this method is intended to be overwritten if
        additional/alternative auth params need to be provided

        Returns:
            dict: auth params that passed to requests

        """
        return {}

    def get_extra_params(self):
        """Get additional parameters for inclusion in requests.

        This method is intended to be overwritten if additional/alternative
        parameters need to be provided in the query string or POST body.

        Returns:
            dict: parameters that will be included in the request
        """
        extra_params = {}
        # Call the deprecated method if it has been overridden
        if not hasattr(self.get_auth_params, 'is_deprecated'):
            utils.deprecation_warning(
                "Function get_auth_params() is deprecated and should not be used",
                stacklevel=3
            )
            extra_params.update(self.get_auth_params())
        elif self.sub_user:
            extra_params.update(sub_id=self.sub_user)

        return extra_params

    def get_auth(self):
        """Get the authentication parameter for the raw request

        This method is intended to be overwritten if required.

        Returns:
            :class:`requests.auth.AuthBase`: the authentication parameter
                accepted by the `requests` module
        """
        if self.user and self.password:
            return (self.user, self.password)

    def get_user_agent(self):
        """Get the user agent for the raw request

        This method is intended to be overwritten by subclasses that want
        a custom User-Agent header for the requests

        Returns:
            :str: the user agent string
        """
        return "pyticketswitch {}".format(pyticketswitch.__version__)

    def get_headers(self, headers):
        """Generate common headers to send with all requests

        Returns:
            dict: key value map of headers

        """
        if self.language:
            headers.update({'Accept-Language': self.language})

        # Modify user agent to report Pyticketswitch version
        headers.update({
            'User-Agent': self.get_user_agent()
        })

        return headers

    def get_tracking_params(self, custom_tracking_id=None):
        """
        Return current request's session tracking id
        or custom tracking id passed
        """
        tracking_id = custom_tracking_id or self.tracking_id
        if tracking_id:
            return {"tsw_session_track_id": tracking_id}
        return {}

    def get_session(self):
        """Get the requests.Session instance to use to make HTTP requests

        By default this method will create a new session for each request. This
        replicates the default behaviour of the requests library:
        https://github.com/kennethreitz/requests/blob/ead8fba84b12e7496c65272a07de47d553aa0ca0/requests/api.py#L57-L58

        A common modification to this class would be to overload this method to
        provide a single session instance across all calls to take advantage of
        keep-alive.

        .. note:: remember to also overload
                  :meth:`cleanup_session <pyticketswitch.client.Client.cleanup_session>`
                  as well or you connections/session might be unexpectedly killed.
        """
        return requests.Session()

    def cleanup_session(self, session):
        """Cleans up sessions so that we don't leave open sockets.

        If you want to add support for persistent connections, then you should
        noop this method so it does nothing.

        Args:
            session (:class:`requests.Session`): the http session to clean up.
        """
        logger.debug('requests session cleaning up')
        session.close()

    def make_request(self, endpoint, params, method=GET, headers={}, timeout=None):
        """Makes actual requests to the API

        Args:
            endpoint (str): target API endpoint
            params (dict): parameters to provide to requests
            method (str): HTTP method to make the request with
                valid values are ``post`` and ``get``. Defaults to ``get``.
            headers (dict): headers to include with the request
            timeout (int): timeout to include with the request. Defaults to ``None``.

        Returns:
            str: The body of the response after deserialising from JSON

        Raises:
            AuthenticationError: When authentication details provided are
                invalid
            InvalidResponseError: When the status code of the response is not
                200
            APIError: When any other explict errors are returned from the API
        """

        url = self.get_url(endpoint)
        params.update(self.get_extra_params())
        if not params.get('tsw_session_track_id'):
            params.update(self.get_tracking_params())

        logger.debug(u'url: %s; endpoint: %s; params: %s', self.url, endpoint, params)

        raw_headers = self.get_headers(headers)

        auth = self.get_auth()

        session = self.get_session()

        if method == POST:
            response = session.post(url, auth=auth, data=params, headers=raw_headers, timeout=timeout)
        else:
            response = session.get(url, auth=auth, params=params, headers=raw_headers, timeout=timeout)

        logger.debug(six.u(response.content))

        self.cleanup_session(session)

        parse_float = decimal.Decimal if self.use_decimal else float

        try:
            contents = response.json(parse_float=parse_float)
        except ValueError:
            raise exceptions.InvalidResponseError(
                ("Unable to parse json data from {} response with status "
                 "code `{}`").format(
                    endpoint,
                    response.status_code,
                )
            )

        if 'error_code' in contents:

            if contents['error_code'] == 3:
                raise exceptions.AuthenticationError(
                    contents['error_desc'],
                    contents['error_code'],
                    response,
                )

            if response.status_code == 410:
                raise exceptions.CallbackGoneError(
                    contents['error_desc'],
                    contents['error_code'],
                    response,
                )

            raise exceptions.APIError(
                contents['error_desc'],
                contents['error_code'],
                response,
            )

        if response.status_code != 200:
            raise exceptions.InvalidResponseError(
                "got status code `{}` from {}".format(
                    response.status_code,
                    endpoint,
                )
            )

        return contents

    def test(self):
        """Test the connection

        Wraps `/f13/test.v1`_

        will return the running user on sucess and will raise an exception
        if the authentication details are invalid.

        This call is not required, but may be useful for validating auth
        credentials, or checking on the health of the ticketswitch API.

        Returns:
            :obj:`pyticketswitch.user.User`: details about the user calling the API

        .. _`/f13/test.v1`: http://docs.ingresso.co.uk/#test

        """
        response = self.make_request('test.v1', {})

        user = User.from_api_data(response)

        return user

    def add_optional_kwargs(self, params, availability=False,
                            availability_with_performances=False,
                            extra_info=False, reviews=False, media=False,
                            cost_range=False, best_value_offer=False,
                            max_saving_offer=False, min_cost_offer=False,
                            top_price_offer=False, no_singles_data=False,
                            cost_range_details=False, source_info=False,
                            tracking_id=None,
                            **kwargs):
        """Adds additional arguments to the requests.

        All client methods will take several optional arguments that will
        extend the data returned with addtional information about the returned
        objects.

        Generally these are applicable to objects that return events, however
        some arguments will also augment performances, cost ranges, and
        availability details.

        `See the main F13 documentation for more details.
        <http://docs.ingresso.co.uk/#additional-parameters>`_

        Args:
            params (dict): The parameters dictionary into which any additional
                paramters will be added
            availability (bool): Includes general information
                about availability of events and performances.
            availability_with_performances (bool): Includes
                detailed information about avilability of events and includes
                performance information.
            extra_info (bool): Includes additional event
                textual content. Defaults to :obj:`False`.
            reviews (bool): Includes event reviews when
                available. Defaults to :obj:`False`.
            media (bool): Includes any media assets associated
                with an event. Defaults to :obj:`False`.
            cost_range (bool): Include price range estimates.
                Defaults to :obj:`False`.
            best_value_offer (bool): requires **cost_range**.
                Includes the offer with the highest percentage saving in cost
                range information. Defaults to :obj:`False`.
            max_saving_offer (bool): requires **cost_range**.
                Includes the offer with the highest absolute saving in cost
                range information. Defaults to :obj:`False`.
            min_cost_offer (bool): requires **cost_range**.
                Includes the offer with the lowest cost in cost range
                information. Defaults to :obj:`False`.
            top_price_offer (bool): requires **cost_range**.
                Includes the offer with the highest cost in cost range
                information. Defaults to :obj:`False`.
            no_singles_data (bool): requires **cost_range**.
                This returns another cost range object that excludes
                availability with only one consecutive seat available.
                Defaults to :obj:`False`.
            cost_range_details (bool): Cost range information for
                each available price band.  Defaults to :obj:`False`.
            cost_range_details (bool): Cost range information for
                each available price band.  Defaults to :obj:`False`.
            source_info (bool): includes information on the source
                system. defaults to :obj:`false`.
            tracking_id (string): Add custom tracking id to the request
            **kwargs: Additional or override parameters to send with the
                request.
        """

        if extra_info:
            params.update(req_extra_info=True)

        if reviews:
            params.update(req_reviews=True)

        if media:
            params.update({
                'req_media_triplet_one': True,
                'req_media_triplet_two': True,
                'req_media_triplet_three': True,
                'req_media_triplet_four': True,
                'req_media_triplet_five': True,
                'req_media_seating_plan': True,
                'req_media_square': True,
                'req_media_landscape': True,
                'req_media_marquee': True,
                'req_video_iframe': True,
            })

        if cost_range:
            params.update(req_cost_range=True)

        if best_value_offer:
            params.update(req_cost_range_best_value_offer=True,
                          req_cost_range=True)

        if max_saving_offer:
            params.update(req_cost_range_max_saving_offer=True,
                          req_cost_range=True)

        if min_cost_offer:
            params.update(req_cost_range_min_cost_offer=True,
                          req_cost_range=True)

        if top_price_offer:
            params.update(req_cost_range_top_price_offer=True,
                          req_cost_range=True)

        if no_singles_data:
            params.update(req_cost_range_no_singles_data=True,
                          req_cost_range=True)

        if cost_range_details:
            params.update(req_cost_range_details=True)

        if availability:
            params.update(req_avail_details=True)

        if availability_with_performances:
            params.update(req_avail_details=True,
                          req_avail_details_with_perfs=True)

        if tracking_id:
            params.update(self.get_tracking_params(
                custom_tracking_id=tracking_id))

        if source_info:
            params.update(req_src_info=True)
        params.update(kwargs)

    def list_events(self, keywords=None, start_date=None, end_date=None,
                    country_code=None, city_code=None, latitude=None,
                    longitude=None, radius=None, include_dead=False,
                    sort_order=None, page=0, page_length=0, **kwargs):

        """List events with the given parameters

        Wraps `/f13/events.v1`_

        Called with out arguments this method will return all live events
        available to the user.

        Args:
            keywords (list): list of keyword strings. For example:
                ``keywords=['sadlers', 'nutcracker']``. Defaults to
                :obj:`None`.
            start_date (datetime.datetime): only show events that
                have a performance after this date. Defaults to :obj:`None`.
            end_date (datetime.datetime): only show events that have
                a performance before this date. Defaults to :obj:`None`.
            country_code (string): only show events in this country.
                the country is specified by it's ISO 3166-1 country code.
                Defaults to :obj:`None`.
            city_code: (string): specified by the internal city code. As
                a rule of thumb this is the lowercase city name followed by
                a hyphen followed by the ISO 3166-1 country code. For example:
                ``london-uk``, ``new_york-us``, ``berlin-de``.  Defaults to
                :obj:`None`.
            latitude (float): only show events near this latitude.
                valid only in combination with longitude and radius. Defaults
                to :obj:`None`.
            longitude (float): only show events near this longitude.
                valid only in combination with latitude and radius. Defaults
                to :obj:`None`.
            radius (float): only show events inside this radius
                relative to the provided coordinates (latitude & longitude
                above). Units are kilometers. Defaults to :obj:`None`.
            include_dead (bool): when true results will include all
                events even if they are dead (are unavailable to purchase
                from). Defaults to :obj:`False`.
            sort_order (string): order the returned events by the
                specified metric. See
                :ref:`sorting search results <sorting_search_results>`.
                Defaults to :obj:`None`
            page (int): the page of a paginated response.
            page_length (int): how many performances are
                returned per page.
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            list, :class:`EventMeta <pyticketswitch.event.EventMeta>`: a list
            of :class:`Events <pyticketswitch.event.Event>` objects and meta
            information for those events.

        Raises:
            InvalidGeoParameters: when latitude, longitude, or radius is
                specified without the rest of the required geographic
                parameters.
            InvalidResponse: when the response is in an unexpected format

        .. _`/f13/events.v1`: http://docs.ingresso.co.uk/#events-list

        """

        params = {}

        if keywords:
            params.update(keywords=','.join(keywords))

        if start_date or end_date:
            params.update(date_range=utils.date_range_str(start_date, end_date))

        if country_code:
            params.update(country_code=country_code)

        if city_code:
            params.update(city_code=city_code)

        if all([latitude, longitude, radius]):
            params.update(circle='{lat}:{lon}:{rad}'.format(
                lat=latitude,
                lon=longitude,
                rad=radius,
            ))
        elif any([latitude, longitude, radius]):
            raise exceptions.InvalidGeoParameters(
                'Geo data must include latitude, longitude, and radius',
            )

        if include_dead:
            params.update(include_dead=True)

        if sort_order:
            params.update(sort_order=sort_order)

        if page > 0:
            params.update(page_no=page)
        if page_length > 0:
            params.update(page_len=page_length)

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('events.v1', params)

        if 'results' not in response:
            raise exceptions.InvalidResponseError(
                "got no results key in json response"
            )

        result = response.get('results', {})
        raw_events = result.get('event', [])
        events = [
            Event.from_api_data(data)
            for data in raw_events
        ]

        meta = EventMeta.from_api_data(response)
        return events, meta

    def get_events(self, event_ids,
                   with_addons=False, with_upsells=False, **kwargs):
        """Get events with the given id's

        Wraps `/f13/events_by_id.v1`_

        Args:
            event_ids (list): list of event IDs
            with_addons (bool): include add-on events
            with_upsells (bool): include upsell events
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            dict, :class:`EventMeta <pyticketswitch.event.EventMeta>`:
            :class:`Events <pyticketswitch.event.Event>` indexed by event
            ID and meta information for those events.

        Raises:
            InvalidResponse: when the response is in an unexpected format

        .. _`/f13/events_by_id.v1`: http://docs.ingresso.co.uk/#events-by-id

        """
        params = {}

        if event_ids:
            params.update(event_id_list=','.join(event_ids))

        self.add_optional_kwargs(params, **kwargs)

        if with_addons:
            params.update(add_add_ons=with_addons)

        if with_upsells:
            params.update(add_upsells=with_upsells)

        response = self.make_request('events_by_id.v1', params)

        if 'events_by_id' not in response:
            raise exceptions.InvalidResponseError(
                "got no events_by_id key in json response"
            )

        events_by_id = response.get('events_by_id', {})
        events = {
            event_id: Event.from_events_by_id_api_data(raw_event)
            for event_id, raw_event in events_by_id.items()
            if raw_event.get('event')
        }

        meta = EventMeta.from_api_data(response)
        return events, meta

    def get_event(self, event_id, **kwargs):
        """Get a specific event by id

        Helper method to avoid having to do something like this lots of times::

            >>> client.get_events(['6IF'])['6IF']
            <Event 6IF:Matthew Bourne's Nutcracker TEST>

        Instead this interface is much less stuttery::

            >>> client.get_event('6IF')
            <Event 6IF:Matthew Bourne's Nutcracker TEST>

        Args:
            event_id (str): ID of the event to retrieve
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            :class:`Event <pyticketswitch.event.Event>`, :class:`EventMeta <pyticketswitch.event.EventMeta>`:
            the target event and meta information about the event.

            will return :obj:`None` if the event does not exist.

        """
        events, meta = self.get_events([event_id], **kwargs)
        return events.get(event_id), meta

    def get_months(self, event_id, **kwargs):
        """Returns a summary of availability accross months.

        Wraps `/f13/months.v1`_

        Args:
            event_id (str): ID of the event to retrieve
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            list: :class:`Months <pyticketswitch.month.Month>` ordered chronologically

        Raises:
            InvalidResponse: when the response is in an unexpected format

        .. _`/f13/months.v1`: http://docs.ingresso.co.uk/#months

        """
        params = {'event_id': event_id}

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('months.v1', params)

        if 'results' not in response:
            raise exceptions.InvalidResponseError(
                "got no results key in json response"
            )

        result = response.get('results', {})
        raw_months = result.get('month', [])

        months = [
            Month.from_api_data(data)
            for data in raw_months
        ]

        return months

    def list_performances(self, event_id, start_date=None, end_date=None,
                          page_length=0, page=0, **kwargs):
        """List performances for a specified event

        Wraps `/f13/performances.v1`_

        Args:
            event_id (str): identifier for the event.
            start_date (datetime.datetime):
                list performances only if they occur after this date.
            end_date (datetime.datetime):
                list performances only if they occur before this date.
            page (int): the page of a paginated response.
            page_length (int): how many performances are
                returned per page.
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            list, :class:`PerformanceMeta <pyticketswitch.performance.PerformanceMeta>`:
            A list of
            :class:`Performances <pyticketswitch.performance.Performance>`
            for the given event and meta information about the performances.

        Raises:
            InvalidResponse: when the response is in an unexpected format

        .. _`/f13/performances.v1`: http://docs.ingresso.co.uk/#performances-list
        """
        params = {'event_id': event_id}

        if page > 0:
            params.update(page_no=page)

        if page_length > 0:
            params.update(page_len=page_length)

        if start_date or end_date:
            params.update(date_range=utils.date_range_str(start_date, end_date))

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('performances.v1', params)

        if 'results' not in response:
            raise exceptions.InvalidResponseError(
                "got no results key in json response"
            )

        result = response.get('results', {})

        raw_performances = result.get('performance', [])
        performances = [
            Performance.from_api_data(data)
            for data in raw_performances
        ]

        meta = PerformanceMeta.from_api_data(response)

        return performances, meta

    def get_performances(self, performance_ids, **kwargs):
        """Get performances with the given ID's

        Wraps `/f13/performances_by_id.v1`_

        Args:
            performance_ids (list): list of performance IDs to fetch.
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            dict, :class:`PerformanceMeta <pyticketswitch.performance.PerformanceMeta>`:
            :class:`Performances <pyticketswitch.performance.Performance>`
            indexed by performance ID and meta information about the
            performances.

        Raises:
            InvalidResponse: when the response is in an unexpected format.

        .. _`/f13/performances_by_id.v1`: http://docs.ingresso.co.uk/#performances-by-id

        """

        params = {
            'perf_id_list': ','.join(performance_ids),
        }

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('performances_by_id.v1', params)

        if 'performances_by_id' not in response:
            raise exceptions.InvalidResponseError(
                "got no performances_by_id key in json response"
            )

        raw_performances = response.get('performances_by_id', {})
        performances = {
            performance_id: Performance.from_api_data(data)
            for performance_id, data in raw_performances.items()
        }

        meta = PerformanceMeta.from_api_data(response)

        return performances, meta

    def get_performance(self, performance_id, **kwargs):
        """Get a specific performance by id

        Helper method to avoid having to do something like this lots of times::

            >>> client.get_performances(['6IF-B1H'])['6IF-B1H']
            <Performance 6IF-B1H: 2017-06-02T19:30:00+01:00>

        Instead this interface is much less stuttery::

            >>> client.get_performance('6IF-B1H')
            <Performance 6IF-B1H: 2017-06-02T19:30:00+01:00>

        Args:
            performance_id (str): ID of the performance to retrieve
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            :class:`Performance <pyticketswitch.event.Event>`, :class:`PerformanceMeta <pyticketswitch.performance.PerformanceMeta>`:
            the target Performance and meta information about the performance.

            will return :obj:`None` if the performance does not exist.

        """
        performances, meta = self.get_performances([performance_id], **kwargs)
        return performances.get(performance_id), meta

    def get_availability(self, performance_id, number_of_seats=None,
                         discounts=False, example_seats=False,
                         seat_blocks=False, user_commission=False, **kwargs):
        """Fetch available tickets and prices for a given performance

        Wraps `/f13/availability.v1`_

        Args:
            performance_id (string): identifier of the target performance.
            number_of_seats (int): number of seats that we after,
                Defaults to :obj:`None`.
            discounts (bool): request all discount options for all
                price bands in response. Defaults to :obj:`False`.

            example_seats (bool): request example seats for seated
                events. Defaults to :obj:`False`.
            seat_blocks (bool): request seating information if
                available. Defaults to :obj:`False`.
            user_commission (bool): request user commission for each
                price band/discount. Defaults to :obj:`False`
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        .. note:: setting **discounts** or the **user_commission** arguments to
                  :obj:`True` will increase the response time of your request.

        Returns:
           list, :class:`AvailabilityMeta <pyticketswitch.availability.AvailabilityMeta>`:
           a list of :class:`TicketTypes <pyticketswitch.ticket_type.TicketType>`
           and and meta data about the response.

        Raises:
            BackendBrokenError: when the backend system is responding but
                may be under heavy load
            BackendDownError: when the backend system is not responding
            BackendThrottleError: when your call got throttled and timed out
                while waiting for a response.
            InvalidResponse: when the response is in an unexpected format.

        .. _`/f13/availability.v1`: http://docs.ingresso.co.uk/#availability
        """
        params = {'perf_id': performance_id}

        if number_of_seats:
            params.update(no_of_seats=number_of_seats)

        if discounts:
            params.update(add_discounts=True)

        if example_seats:
            params.update(add_example_seats=True)

        if seat_blocks:
            params.update(add_seat_blocks=True)

        if user_commission:
            params.update(req_predicted_commission=True)

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('availability.v1', params)

        if 'availability' not in response:
            raise exceptions.InvalidResponseError(
                "got no availability key in json response"
            )

        meta = AvailabilityMeta.from_api_data(response)

        raw_availability = response.get('availability', {})

        availability = [
            TicketType.from_api_data(data)
            for data in raw_availability.get('ticket_type', [])
        ]

        return availability, meta

    def get_send_methods(self, performance_id, **kwargs):
        """Fetch available delivery methods for a given performance

        Wraps `/f13/send_methods.v1`_

        Args:
            performance_id (string): identifier of the target performance.
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
           list, :class:`CurrencyMeta <pyticketswitch.currency.CurrencyMeta>`:
           a list of :class:`SendMethods <pyticketswitch.send_method.SendMethod>`
           and information about the currencies of the prices in the response

        Raises:
            InvalidResponse: when the response is in an unexpected format.

        .. _`/f13/send_methods.v1`: http://docs.ingresso.co.uk/#send-methods
        """
        params = {'perf_id': performance_id}
        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('send_methods.v1', params)

        if 'send_methods' not in response:
            raise exceptions.InvalidResponseError(
                "got no send_methods key in json response"
            )

        raw_send_methods = response.get('send_methods', {})

        send_methods = [
            SendMethod.from_api_data(data)
            for data in raw_send_methods.get('send_method', [])
        ]

        meta = CurrencyMeta.from_api_data(response)

        return send_methods, meta

    def get_discounts(self, performance_id, ticket_type_code, price_band_code, user_commission=False):
        """Fetch available discounts for a ticket_type/price band combination

        Wraps `/f13/discounts.v1`_

        Args:
            performance_id (string): identifier of the target performance.
            ticket_type_code (string): code for the target ticket type.
            price_band_code (string): code for the target price band.
            user_commission (bool): if True then return the user_commission,
                otherwise do not return the user_commission. Defaults to False.

        Returns:
           list, :class:`CurrencyMeta <pyticketswitch.currency.CurrencyMeta>`:
           a list of :class:`Discounts <pyticketswitch.discount.Discount>`
           and information about the currencies of the prices in the response.

        Raises:
            InvalidResponse: when the response is in an unexpected format.

        .. _`/f13/discounts.v1`: http://docs.ingresso.co.uk/#discounts
        """
        params = {
            'perf_id': performance_id,
            'ticket_type_code': ticket_type_code,
            'price_band_code': price_band_code,
            'req_predicted_commission': user_commission,
        }

        response = self.make_request('discounts.v1', params)

        if 'discounts' not in response:
            raise exceptions.InvalidResponseError(
                "got no discounts key in json response"
            )

        raw_discounts = response.get('discounts', {})

        discounts = [
            Discount.from_api_data(data)
            for data in raw_discounts.get('discount', [])
        ]

        meta = CurrencyMeta.from_api_data(response)

        return discounts, meta

    def _trolley_params(self, token=None, number_of_seats=None, discounts=None,
                        seats=None, send_codes=None, ticket_type_code=None,
                        performance_id=None, price_band_code=None,
                        item_numbers_to_remove=None, **kwargs):
        """Handle arguments common to the
        :meth:`Client.get_trolley <pyticketswitch.client.Client.get_trolley>`
        and the
        :meth:`Client.make_reservation <pyticketswitch.client.Client.make_reservation>`
        methods.

        These two methods accept identical arguments and these resolve
        to identical parameters.

        Args:
            token (string): trolley token from a previous trolley
                call.
            number_of_seats (int): number of seats to add to the
                trolley.
            discounts (list): list containing discount codes for each
                requested seat.
            seats (list): list of seat IDs.
            send_codes (dict): send codes indexed on backend source
                code.
            ticket_type_code: (string): code of ticket type to add to
                the trolley.
            performance_id: (string): id of the performance to add to
                the trolley.
            price_band_code: (string): code of price band to add to
                the trolley
            item_numbers_to_remove: (list): list of item numbers to
                remove from trolley.
            **kwargs: arbitary additional raw keyword arguments to add the
                parameters.

        Raises:
            InvalidParametersError: when there is an issue with the provided
                parameters.

        """

        params = {}

        if token:
            params.update(trolley_token=token)

        if performance_id:
            params.update(perf_id=performance_id)

        # TODO: check if 0 is a legit number to be passing in here.
        # for the moment I'm assuming that it isn't
        if number_of_seats:
            params.update(no_of_seats=number_of_seats)

        if ticket_type_code:
            params.update(ticket_type_code=ticket_type_code)

        if price_band_code:
            params.update(price_band_code=price_band_code)

        if item_numbers_to_remove and not token:
            raise exceptions.InvalidParametersError(
                'got item_numbers_to_remove but no token specified'
            )
        if item_numbers_to_remove:
            params.update(
                remove_items_list=','.join(
                    [str(item) for item in item_numbers_to_remove]
                )
            )

        if seats:
            params.update({
                'seat{}'.format(i): seat
                for i, seat in enumerate(seats)
            })

        if discounts:
            params.update({
                'disc{}'.format(i): discount
                for i, discount in enumerate(discounts)
            })

        if send_codes and not isinstance(send_codes, dict):
            raise exceptions.InvalidParametersError(
                'send_codes should be a dictionary in the format of `{source_code: send_code}`'
            )

        if send_codes:
            params.update({
                '{}_send_code'.format(source_code): send_code
                for source_code, send_code in send_codes.items()
            })

        self.add_optional_kwargs(params, **kwargs)

        return params

    def get_trolley(self, token=None, number_of_seats=None, discounts=None,
                    seats=None, send_codes=None, ticket_type_code=None,
                    performance_id=None, price_band_code=None,
                    item_numbers_to_remove=None,
                    raise_on_unavailable_order=False, **kwargs):

        """Retrieve the contents of a trolley from the API.

        Wraps `/f13/trolley.v1`_

        Args:
            token (string): trolley token from a previous trolley
                call.
            number_of_seats (int): number of seats to add to the
                trolley.
            discounts (list): list containing discount codes for each
                requested seat.
            seats (list): list of seat IDs.
            send_codes (dict): send codes indexed on backend source
                code.
            ticket_type_code (string): code of ticket type to add to
                the trolley.
            performance_id (string): id of the performance to add to
                the trolley.
            price_band_code (string): code of price band to add to
                the trolley.
            item_numbers_to_remove (list): list of item numbers to
                remove from trolley.
            raise_on_unavailable_order (bool): When set to ``True`` this method
                will raise an exception when the API was not able to add an
                order to the trolley as it was unavailable.
            **kwargs: arbitary additional raw keyword arguments to add the
                parameters.

        Returns:
            :class:`Trolley <pyticketswitch.trolley.Trolley>`, :class:`CurrencyMeta <pyticketswitch.currency.CurrencyMeta>`:
            the contents of the trolley and meta data associated with the
            trolley.

        Raises:
            InvalidParametersError: when there is an issue with the provided
                parameters.
            OrderUnavailableError: when ``raise_on_unavailable_order`` is set
                to ``True`` and the requested addition to a trolley was
                unavailable.

        .. _`/f13/trolley.v1`: http://docs.ingresso.co.uk/#trolley

        """

        params = self._trolley_params(
            token=token, number_of_seats=number_of_seats, discounts=discounts,
            seats=seats, send_codes=send_codes,
            ticket_type_code=ticket_type_code, performance_id=performance_id,
            price_band_code=price_band_code,
            item_numbers_to_remove=item_numbers_to_remove, **kwargs)

        response = self.make_request('trolley.v1', params)

        trolley = Trolley.from_api_data(response)
        meta = CurrencyMeta.from_api_data(response)

        if raise_on_unavailable_order:
            if trolley and trolley.input_contained_unavailable_order:
                raise exceptions.OrderUnavailableError(
                    "inputs contained unavailable order")

        return trolley, meta

    def get_upsells(self, token=None, number_of_seats=None, discounts=None,
                    seats=None, send_codes=None, ticket_type_code=None,
                    performance_id=None, price_band_code=None,
                    item_numbers_to_remove=None, **kwargs):

        """Retrieve a list of upsell events related to a trolley from the API.

        Upsell events are related to a main event but can be purchased
        separately. This call accepts a trolley token or any combination of
        parameters to create a valid trolley, but does not alter any existing
        trolley (it is idempotent).

        Wraps `/f13/upsells.v1`_

        Args:
            token (string): trolley token from a previous trolley
                call.
            number_of_seats (int): trolley with number of seats added.
            discounts (list): list containing discount codes for each
                requested seat.
            seats (list): trolley with added list of seat IDs.
            send_codes (dict): send codes indexed on backend source
                code.
            ticket_type_code: (string): trolley with tickets of
                ticket type added.
            performance_id: (string): trolley with tickets from the
                specified performance added.
            price_band_code: (string): trolley with tickets from a
                specified price band added.
            item_numbers_to_remove: (list): trolley with a list of
                item numbers removed.
            **kwargs: arbitary additional raw keyword arguments to add the
                parameters.

        Returns:
            list, :class:`EventMeta <pyticketswitch.event.EventMeta>`:
            a list of :class:`Events <pyticketswitch.event.Event>` of related upsell
            events

        Raises:
            InvalidParametersError: when there is an issue with the provided
                parameters.
            InvalidResponse: when the response is in an unexpected format.

        .. _`/f13/upsells.v1`: http://docs.ingresso.co.uk/#related-events
        """

        params = self._trolley_params(
            token=token, number_of_seats=number_of_seats, discounts=discounts,
            seats=seats, send_codes=send_codes,
            ticket_type_code=ticket_type_code, performance_id=performance_id,
            price_band_code=price_band_code,
            item_numbers_to_remove=item_numbers_to_remove, **kwargs)

        response = self.make_request('upsells.v1', params)

        if 'results' not in response:
            raise exceptions.InvalidResponseError(
                "got no results key in JSON response"
            )

        results = response.get('results', {})

        raw_upsell_events = results.get('event', [])
        upsell_events = [
            Event.from_api_data(data)
            for data in raw_upsell_events
        ]

        upsell_meta = EventMeta.from_api_data(response)

        return (upsell_events, upsell_meta)

    def get_addons(self, token=None, number_of_seats=None, discounts=None,
                   seats=None, send_codes=None, ticket_type_code=None,
                   performance_id=None, price_band_code=None,
                   item_numbers_to_remove=None, **kwargs):

        """Retrieve a list of add-on events from the API.

        Wraps `/f13/add_ons.v1`_

        Args:
            token (string): trolley token from a previous trolley
                call.
            number_of_seats (int): trolley with number of seats added.
            discounts (list): list containing discount codes for each
                requested seat.
            seats (list): trolley with added list of seat IDs.
            send_codes (dict): send codes indexed on backend source
                code.
            ticket_type_code: (string): trolley with tickets of
                ticket type added.
            performance_id: (string): trolley with tickets from the
                specified performance added.
            price_band_code: (string): trolley with tickets from a
                specified price band added.
            item_numbers_to_remove: (list): trolley with a list of
                item numbers removed.
            **kwargs: arbitrary additional raw keyword arguments to add to the
                parameters.

        Returns:
            list, :class:`EventMeta <pyticketswitch.event.EventMeta>`:
            a list of :class:`Events <pyticketswitch.event.Event>` of add-on events

        Raises:
            InvalidParametersError: when there is an issue with the provided
                parameters.
            InvalidResponse: when the response is in an unexpected format.

        .. _`/f13/add_ons.v1`: http://docs.ingresso.co.uk/#add-ons
        """

        params = self._trolley_params(
            token=token, number_of_seats=number_of_seats, discounts=discounts,
            seats=seats, send_codes=send_codes,
            ticket_type_code=ticket_type_code, performance_id=performance_id,
            price_band_code=price_band_code,
            item_numbers_to_remove=item_numbers_to_remove, **kwargs)

        response = self.make_request('add_ons.v1', params)

        if 'results' not in response:
            raise exceptions.InvalidResponseError(
                "got no results key in json response"
            )

        add_on_results = response.get('results', {})

        raw_add_on_events = add_on_results.get('event', [])
        add_on_events = [
            Event.from_api_data(data)
            for data in raw_add_on_events
        ]

        add_on_meta = EventMeta.from_api_data(response)

        return (add_on_events, add_on_meta)

    def make_reservation(self, token=None, number_of_seats=None, discounts=None,
                         seats=None, send_codes=None, ticket_type_code=None,
                         performance_id=None, price_band_code=None,
                         item_numbers_to_remove=None,
                         raise_on_unavailable_order=False, **kwargs):

        """Attempt to reserve all the items in the given trolley

        Wraps `/f13/reserve.v1`_

        This method will take all the same arguments as
        :func:`get_trolley <pyticketswitch.client.Client.get_trolley>`. You can
        either build a trolley via the
        :func:`get_trolley <pyticketswitch.client.Client.get_trolley>` method
        and pass the returned trolley token into the reservation call, or
        alternatively you can provide the trolley parameters directly to this
        method.

        .. note:: If you are interested in bundling multiple orders into a
                  single purchase then see the :ref:`Bundling <bundling>`
                  documentation for more details.

        Args:
            token (string): trolley token from a previous trolley
                call.
            number_of_seats (int): number of seats to add to the
                trolley.
            discounts (list): list containing discount codes for each
                requested seat.
            seats (list): list of seat id's.
            send_codes (dict): send codes indexed on backend source
                code.
            ticket_type_code: (string): code of ticket type to add to
                the trolley.
            performance_id: (string): id of the performance to add to
                the trolley.
            price_band_code: (string): code of price band to add to
                the trolley
            item_numbers_to_remove: (list): list of item numbers to
                remove from trolley.
            raise_on_unavailable_order (bool): When set to ``True`` this method
                will raise an exception when the API was not able to add an
                order to the trolley as it was unavailable.
            **kwargs: arbitary additional raw keyword arguments to add the
                parameters.

        Returns:
            :class:`Reservation <pyticketswitch.reservation.Reservation>`, :class:`CurrencyMeta <pyticketswitch.currency.CurrencyMeta>`:
            Information about the reservation and meta data asscociated with
            the reservation.

        Raises:
            InvalidParametersError: when there is an issue with the provided
                parameters.
            OrderUnavailableError: when ``raise_on_unavailable_order`` is set
                to ``True`` and the requested addition to a trolley was
                unavailable.

        .. _`/f13/reserve.v1`: http://docs.ingresso.co.uk/#reserve

        """

        params = self._trolley_params(
            token=token, number_of_seats=number_of_seats, discounts=discounts,
            seats=seats, send_codes=send_codes,
            ticket_type_code=ticket_type_code, performance_id=performance_id,
            price_band_code=price_band_code,
            item_numbers_to_remove=item_numbers_to_remove, **kwargs)

        response = self.make_request('reserve.v1', params, method=POST)

        reservation = Reservation.from_api_data(response)
        meta = CurrencyMeta.from_api_data(response)

        if raise_on_unavailable_order:
            if reservation and reservation.input_contained_unavailable_order:
                raise exceptions.OrderUnavailableError(
                    "inputs contained unavailable order",
                    reservation=reservation,
                    meta=meta)

        return reservation, meta

    def release_reservation(self, transaction_uuid, **kwargs):
        """Release an existing reservation.

        Wraps `/f13/release.v1`_

        Args:
            transaction_uuid (str): the identifier of the reservaiton.
            **kwargs: arbitary additional raw keyword arguments to add the
                parameters.

        Returns:
            bool: :obj:`True` if the reservation was successfully released
            otherwise :obj:`False`.

        .. _`/f13/release.v1`: http://docs.ingresso.co.uk/#release

        """

        params = {'transaction_uuid': transaction_uuid}
        kwargs.update(params)
        response = self.make_request('release.v1', kwargs, method=POST)

        return response.get('released_ok', False)

    def get_status(self, transaction_uuid=None, transaction_id=None,
                   customer=False, external_sale_page=False, **kwargs):
        """Get the status of reservation, purchase or transaction.

        .. note:: The **transaction_id** field is for backwards compatability
            with the old XML API. You can use either **transaction_id** or
            **transaction_uuid**, however please use the **transaction_uuid** as
            **transaction_id** will be deprecated shortly.

        Wraps `/f13/status.v1`_

        Args:
            transaction_uuid (str): identifier for the transaction.
            transaction_id (str): identifier for the old transaction ids.
                Note: one of these two must be set.
            customer (bool): include customer information if
                available. Defaults to :obj:`False`.
            external_sale_page (bool): include the saved html of the
                sale/confirmation page if you asked us to save it for you.
                Defaults to :obj:`None`
            **kwargs: arbitary keyword parameters to pass directly to the API.

        Returns:
            :class:`Status <pyticketswitch.status.Status>`, :class:`CurrencyMeta <pyticketswitch.currency.CurrencyMeta>`:
            the current status of the transaction and acompanying meta
            information.

        .. _`/f13/status.v1`: http://docs.ingresso.co.uk/#status

        """
        params = {}

        if customer:
            params.update(add_customer=True)

        if external_sale_page:
            params.update(add_external_sale_page=True)

        self.add_optional_kwargs(params, **kwargs)

        if transaction_id:
            params.update(transaction_id=transaction_id)
            response = self.make_request('trans_id_status.v1', params)
        else:
            params.update(transaction_uuid=transaction_uuid)
            response = self.make_request('status.v1', params)

        status = Status.from_api_data(response)
        meta = CurrencyMeta.from_api_data(response)

        return status, meta

    def make_purchase(self, transaction_uuid, customer, payment_method=None,
                      send_confirmation_email=True, **kwargs):
        """Purchase tickets for an existing reservation.

        Wraps `/f13/purchase.v1`_

        Args:
            transaction_uuid (str): the identifier of the existing
                reservation/transaction
            customer: `Customer <pyticketswitch.customer.Customer>`
                information.
            payment_method: the customer's payment details. Can be
                :class:`CardDetails <pyticketswitch.payment_methods.CardDetails>`
                or
                :class:`RedirectionDetails <pyticketswitch.payment_methods.RedirectionDetails>`.
            send_confirmation_email (bool): on a successful purchase, when this
                parameter is :obj:`True`, then we will send the customer a
                confirmation email. If you would prefer to send your own
                confirmation email then you can set this parameter to
                :obj:`False`.
            **kwargs: arbitary keyword arguments to send with the request.

        Returns:
            :class:`Status <pyticketswitch.status.Status>`,
            :class:`Callout <pyticketswitch.callout.Callout>`: the current
            status of the transaction and/or a potential callout to redirect
            the customer to.

            This method should only ever return either a status or a callout,
            never both.

            If this method generates a
            :class:`Callout <pyticketswitch.callout.Callout>` then the customer
            should be redirected to the specified third party payment provider.

            See :ref:`Handling callouts <handling_callouts>` for more information.

        .. _`/f13/purchase.v1`: http://docs.ingresso.co.uk/#purchase

        """

        params = {'transaction_uuid': transaction_uuid}

        if send_confirmation_email:
            params.update(send_confirmation_email=True)

        customer_params = customer.as_api_parameters()

        if customer_params:
            params.update(customer_params)

        if payment_method:
            params.update(payment_method.as_api_parameters())

        params.update(kwargs)

        response = self.make_request('purchase.v1', params, method=POST)

        callout_data = response.get('callout')

        if callout_data:
            status = None
            callout = Callout.from_api_data(callout_data)
        else:
            callout = None
            status = Status.from_api_data(response)

        meta = CurrencyMeta.from_api_data(response)

        return status, callout, meta

    def next_callout(self, this_token, next_token, returned_data, **kwargs):
        """Gets the next callout in a callout chain.

        Wraps `/f13/callback.v1`_

        At the end of the callout chain the call will return the status of
        the transaction.

        See :ref:`Handling callouts <handling_callouts>` for more information.

        Args:
            this_token (str): the token for the current redirect.
            next_token (str): the token for the potential next redirect.
            returned_data (dict): dictionary of query string paramters appended
                to your return url.
            **kwargs: arbitary keyword arguments to send with the request.

        Returns:
            :class:`Status <pyticketswitch.status.Status>`,
            :class:`Callout <pyticketswitch.callout.Callout>`: the current
            status of the transaction and/or a potential callout to redirect
            the customer to.

            This method should only ever return either a status or a callout,
            never both.

        .. _`/f13/callback.v1`: http://docs.ingresso.co.uk/#purchasing-with-redirect

        """

        endpoint = "callback.v1/this.{}/next.{}".format(this_token, next_token)

        params = returned_data
        params.update(kwargs)

        response = self.make_request(endpoint, params, method=POST)

        callout_data = response.get('callout')

        if callout_data:
            status = None
            callout = Callout.from_api_data(callout_data)
        else:
            callout = None
            status = Status.from_api_data(response)

        meta = CurrencyMeta.from_api_data(response)

        return status, callout, meta
