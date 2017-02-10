import requests
import logging
import six
from pyticketswitch import exceptions, utils
from pyticketswitch.event import Event
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


logger = logging.getLogger(__name__)

POST = 'post'
GET = 'get'
DEFAULT_ROOT_URL = "https://api.ticketswitch.com"


class Client(object):
    """Client wraps the ticketswitch f13 API.

    Client contains auth details and provides helper methods for calling
    the f13 endpoints.

    Args:
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
        **kwargs: Additional arbitary key word arguments to keep with the
            object.

    Attributes:
        user (str): user id used to connect to the api.
        password (str): Password for the user used to connect to the api.
        url (str): Root url for the API.
        sub_user (str): the sub user is used to idicate a
        language (str): prefered IETF language tag
        kwargs: Additional arbitary key word arguments.

    """

    def __init__(self, user, password, url=DEFAULT_ROOT_URL, sub_user=None,
                 language=None, **kwargs):
        self.user = user
        self.password = password
        self.url = url
        self.sub_user = sub_user
        self.language = language
        self.kwargs = kwargs

    def get_user_path(self):
        """Creates the user path for use in the url from client attributes

        Returns:
            str: the user path

            Takes the format of "/user/subuser/language"

        """
        if not self.user:
            raise exceptions.AuthenticationError("no user provided")

        user_path = '/{}'.format(self.user)

        if self.sub_user and not self.language:
            user_path = '/{}/{}'.format(self.user, self.sub_user)

        if self.sub_user and self.language:
            user_path = '/{}/{}/{}'.format(
                self.user, self.sub_user, self.language)

        if self.language and not self.sub_user:
            user_path = '/{}/-/{}'.format(self.user, self.language)

        return user_path

    def get_url(self, end_point):
        """Get the url for a given endpoint

        Args:
            end_point (str): the target api end point, for example events.v1 or
                performances.v1

        Returns:
            str: the full url for the given endpoint, contains the base url,
                user path and endpoint

        """

        user_path = self.get_user_path()
        url = "{url}/f13/{end_point}{user_path}/".format(
            url=self.url,
            end_point=end_point,
            user_path=user_path,
        )
        return url

    def get_auth_params(self):
        """Get the authentication parameters for inclusion in requests.

        This this method is intended to be overwritten if
        additional/alternative auth params need to be provided

        Returns:
            dict: auth params that passed to requests

        """
        return {'user_passwd': self.password}

    def make_request(self, endpoint, params, method=GET):
        """Makes actual requests to the API

        Args:
            endpoint (str): target API endpoint
            params (dict): parameters to provide to requests
            method (:obj:`str`, optional): HTTP method to make the request with
                valid values are ``post`` and ``get``. Defaults to ``get``.

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
        params.update(self.get_auth_params())

        logger.debug(u'url: %s; endpoint: %s; params: %s', self.url, endpoint, params)

        if method == POST:
            response = requests.post(url, params=params)
        else:
            response = requests.get(url, params=params)

        logger.debug(six.u(response.content))

        if not response.status_code == 200:

            contents = response.json()

            if 'error_code' in contents:

                if contents['error_code'] == 3:
                    raise exceptions.AuthenticationError(
                        contents['error_desc'],
                        contents['error_code'],
                        response,
                    )

                raise exceptions.APIError(
                    contents['error_desc'],
                    contents['error_code'],
                    response,
                )

            raise exceptions.InvalidResponseError(
                "got status code `{}` from {}".format(
                    response.status_code,
                    endpoint,
                )
            )

        return response.json()

    def test(self):
        """Test the connection

        calls /f13/test.v1

        will return the running user on sucess and will raise an exception
        if the authentication details are invalid.

        This call is not required, but may be useful for validating auth
        credentials, or checking on the health of the ticketswitch API.

        Returns:
            :obj:`pyticketswitch.user.User`: details about the user calling the
                API

        Example:.
            >>> from pyticketswitch import Client
            >>> client = Client('demo', 'demopass')
            >>> client.test()
            <User: demo>

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
                            cost_range_details=False, meta_components=False,
                            **kwargs):
        """Adds additional arguments to the requests.

        All client methods will take several optional arguments that will
        extend the data returned with addtional information about the returned
        objects.

        Generally these are applicable to objects that return events, however
        some arguments will also augment performances such as ``availability``
        and ``cost_range``.

        Args:
            params (dict): The parameters dictionary into which any additional
                paramters will be added
            availability (:obj:`bool`, optional): Includes general information
                about availability of events and performances.
            availability_with_performances (:obj:`bool`, optional): Includes
                detailed information about avilability of events and includes
                performance information.
            extra_info (:obj:`bool`, optional): Includes additional event
                textual content.
            reviews (:obj:`bool`, optional): Includes event reviews when
                available.
            media (:obj:`bool`, optional): Includes any media assets associated
                with an event.
            cost_range (:obj:`bool`): Include price range estimates

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

        if meta_components:
            params.update(req_meta_components=True)

        params.update(kwargs)

    def list_events(self, keywords=None, start_date=None, end_date=None,
                    country_code=None, city_code=None, latitude=None,
                    longitude=None, radius=None, include_dead=False,
                    sort_order=None, page=0, page_length=0, **kwargs):

        """List events with the given parameters

        Called with out arugments this method will return all live events
        available to the user.

        Args:
            keywords (list, optional): list of keyword strings. For example:
                ``keywords=['sadlers', 'nutcracker']``. Defaults to
                :obj:`None`.
            start_date (datetime.datetime, optional): only show events that
                have a performance after this date. Defaults to :obj:`None`.
            end_date (datetime.datetime, optional): only show events that have
                a performance before this date. Defaults to :obj:`None`.
            country_code (string, optional): only show events in this country.
                the country is specified by it's ISO 3166-1 country code.
                Defaults to :obj:`None`.
            city_code: (string, optional): specified by the internal city code. As
                a rule of thumb this is the lowercase city name followed by
                a hyphen followed by the ISO 3166-1 country code. For example:
                ``london-uk``, ``new_york-us``, ``berlin-de``.  Defaults to
                :obj:`None`.
            latitude (float, optional): only show events near this latitude.
                valid only in combination with longitude and radius. Defaults
                to :obj:`None`.
            latitude (float, optional): only show events near this longitude.
                valid only in combination with latitude and radius. Defaults
                to :obj:`None`.
            latitude (float, optional): only show events inside this radius
                relative to the provided coordinates (latitude & longitude
                above). Units are kilometers. Defaults to :obj:`None`.
            include_dead (bool, optional): when true results will include all
                events even if they are dead (are unavailable to purchase
                from). Defaults to :obj:`False`.
            sort_order (string, optional): order the returned events by the
                specified metric. See
                :ref:`sorting search results <sorting_search_results>`.
                Defaults to :obj:`None`
            page (int, optional): the page of a paginated response.
            page_length (int, optional): how many performances are
                returned per page.
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            list: a list of :class:`Events <pyticketswitch.event.Event>`
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
            raise exceptions.InvalidGeoData(
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
        return events

    def get_events(self, event_ids, **kwargs):
        """
        Get events with the given id's
        """
        params = {}

        if event_ids:
            params.update(event_id_list=','.join(event_ids))

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('events_by_id.v1', params)

        if 'events_by_id' not in response:
            raise exceptions.InvalidResponseError(
                "got no events_by_id key in json response"
            )

        events_by_id = response.get('events_by_id', {})
        events = {
            event_id: Event.from_events_by_id_data(raw_event)
            for event_id, raw_event in events_by_id.items()
        }
        return events

    def get_event(self, event_id, **kwargs):
        events = self.get_events([event_id], **kwargs)
        if events:
            return events[event_id]

    def get_months(self, event_id, **kwargs):
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

        Args:
            event_id (str): identifier for the event.
            start_date (datetime.datetime, optional):
                list performances only if they occur after this date.
            end_date (datetime.datetime, optional):
                list performances only if they occur before this date.
            page (int, optional): the page of a paginated response.
            page_length (int, optional): how many performances are
                returned per page.
            **kwargs: see :meth:`add_optional_kwargs <pyticketswitch.client.Client.add_optional_kwargs>`
                for more info.

        Returns:
            list, :class:`PerformanceMeta <pyticketswitch.performance.PerformanceMeta>`:
                a list of :class:`Performances <pyticketswitch.performance.Performance>`
                for the given event and meta information about the performances.

        """
        params = {'event_id': event_id}

        if page > 0:
            params.update(page_no=page)

        if page_length > 0:
            params.update(page_len=page_length)

        if start_date or end_date:
            params.update(s_dates=utils.date_range_str(start_date, end_date))

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
        """
        Get performances retrieves performances with the specific given id's
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

        return performances

    def get_performance(self, performance_id, **kwargs):
        performances = self.get_performances([performance_id], **kwargs)
        return performances.get(performance_id)

    def get_availability(self, performance_id, number_of_seats=None,
                         discounts=False, example_seats=False,
                         seat_blocks=False, user_commission=False, **kwargs):
        """
        Fetch available tickets and prices for a given performance
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
            params.update(add_user_commission=True)

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('availability.v1', params)

        if response.get('backend_is_broken'):
            raise exceptions.BackendBrokenError(
                'Error returned from upstream backend system'
            )

        if response.get('backend_is_down'):
            raise exceptions.BackendDownError(
                'Unable to contact upstream backend system'
            )

        if response.get('backend_throttle_failed'):
            raise exceptions.BackendThrottleError(
                'The call timed out while being queued for throttling'
            )

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

    def get_send_methods(self, performance_id):

        params = {'perf_id': performance_id}
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

    def get_discounts(self, performance_id, ticket_type_code, price_band_code):
        params = {
            'perf_id': performance_id,
            'ticket_type_code': ticket_type_code,
            'price_band_code': price_band_code,
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

    def trolley_params(self, token=None, number_of_seats=None, discounts=None,
                       seats=None, send_codes=None, ticket_type_code=None,
                       performance_id=None, price_band_code=None,
                       item_numbers_to_remove=None, **kwargs):
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

        params.update(kwargs)

        return params

    def get_trolley(self, token=None, number_of_seats=None, discounts=None,
                    seats=None, send_codes=None, ticket_type_code=None,
                    performance_id=None, price_band_code=None,
                    item_numbers_to_remove=None, **kwargs):

        """
        The resource that is being retrieved here is primarily a trolley token.
        Along with that we also get information about what that trolley token
        contains, and we reutrn that as a Trolley object.

        The trolley.v1 endpoint isn't really a resource GET in the same way as
        as you might think of a GET request in a REST API. There is no state on
        the server side that we are retrieving. Instead this endpoint will
        consistantly generate a token based on the arugments given. If a
        trolley token is provided and additional arguments are given then the
        server will mutate the passed in token as if alterations have been made
        to a trolley's state, again no state has acutally changed and this
        mutation should be consistantly repeatable

        It looks odd and the phrasing around this is inconsistant with the rest
        of this wrapper so far. I would welcome suggestions on improving this.
        """

        params = self.trolley_params(
            token=token, number_of_seats=number_of_seats, discounts=discounts,
            seats=seats, send_codes=send_codes,
            ticket_type_code=ticket_type_code, performance_id=performance_id,
            price_band_code=price_band_code,
            item_numbers_to_remove=item_numbers_to_remove, **kwargs)

        response = self.make_request('trolley.v1', params)

        trolley = Trolley.from_api_data(response)

        return trolley

    def make_reservation(self, token=None, number_of_seats=None, discounts=None,
                         seats=None, send_codes=None, ticket_type_code=None,
                         performance_id=None, price_band_code=None,
                         item_numbers_to_remove=None, **kwargs):

        """
        This call takes the same arguments as the `get_trolley` call and returns
        a `Trolley` object. However this method actually attempts to
        reserve the tickets in the backend system, and it's results are immutable.
        TODO: check if results are actually immutable.
        """

        params = self.trolley_params(
            token=token, number_of_seats=number_of_seats, discounts=discounts,
            seats=seats, send_codes=send_codes,
            ticket_type_code=ticket_type_code, performance_id=performance_id,
            price_band_code=price_band_code,
            item_numbers_to_remove=item_numbers_to_remove, **kwargs)

        response = self.make_request('reserve.v1', params, method=POST)

        trolley = Reservation.from_api_data(response)

        return trolley

    def release_reservation(self, transaction_uuid):
        params = {'transaction_uuid': transaction_uuid}
        response = self.make_request('release.v1', params, method=POST)

        return response.get('released_ok', False)

    def get_status(self, transaction_uuid, customer=False,
                   external_sale_page=False):
        params = {
            'transaction_uuid': transaction_uuid,
        }

        if customer:
            params.update(add_customer=True)

        if external_sale_page:
            params.update(add_external_sale_page=True)

        response = self.make_request('status.v1', params)

        status = Status.from_api_data(response)

        return status
