import requests
import logging
from pyticketswitch import exceptions, utils
from pyticketswitch.event import Event
from pyticketswitch.performance import Performance
from pyticketswitch.availability import AvailabilityMeta
from pyticketswitch.ticket_type import TicketType
from pyticketswitch.send_method import SendMethod
from pyticketswitch.month import Month
from pyticketswitch.discount import Discount
from pyticketswitch.trolley import Trolley


logger = logging.getLogger(__name__)

POST = 'post'
GET = 'get'


class Client(object):
    DEFAULT_ROOT_URL = "https://api.ticketswitch.com/f13"

    def __init__(self, user, password, url=DEFAULT_ROOT_URL, sub_user=None,
                 language=None, domain=None, ip=None):
        self.user = user
        self.password = password
        self.url = url
        self.sub_user = sub_user
        self.language = language

    def get_user_path(self):
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
        user_path = self.get_user_path()
        url = "{url}/{end_point}{user_path}/".format(
            url=self.url,
            end_point=end_point,
            user_path=user_path,
        )
        return url

    def get_password(self):
        """
        This is here so that it can be overwritten for differing auth methods
        """
        return self.password

    def make_request(self, endpoint, params, method=GET):
        url = self.get_url(endpoint)
        params.update(user_passwd=self.get_password())

        if method == POST:
            response = requests.post(url, params=params)
        else:
            response = requests.get(url, params=params)

        if not response.status_code == 200:

            contents = response.json()

            if 'error_code' in contents:
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

        return response

    def add_optional_kwargs(self, params, availability=False,
                            availability_with_performances=False,
                            extra_info=False, reviews=False, media=False,
                            cost_range=False, best_value_offer=False,
                            max_saving_offer=False, min_cost_offer=False,
                            top_price_offer=False, no_singles_data=False,
                            cost_range_details=False, meta_components=False,
                            **kwargs):

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
            params.update(req_avail_details_with_perfs=True)

        if meta_components:
            params.update(req_meta_components=True)

        params.update(kwargs)

    def list_events(self, keywords=None, start_date=None, end_date=None,
                    country_code=None, city=None, latitude=None,
                    longitude=None, radius=None, include_dead=False,
                    include_non_live=False, order_by_popular=False, page=0,
                    page_length=0, **kwargs):

        """
        list events with the given parameters
        """

        params = {}

        if keywords:
            params.update(s_keys=','.join(keywords))

        if start_date or end_date:
            params.update(s_dates=utils.date_range_str(start_date, end_date))

        if country_code:
            params.update(s_coco=country_code)

        if city:
            params.update(s_city=city)

        if all([latitude, longitude, radius]):
            params.update(s_geo='{lat}:{lon}:{rad}'.format(
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

        if include_non_live:
            params.update(include_non_live=True)

        if order_by_popular:
            params.update(s_top=True)

        if page > 0:
            params.update(page_no=page)
        if page_length > 0:
            params.update(page_len=page_length)

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('events.v1', params)

        contents = response.json()

        if 'results' not in contents:
            raise exceptions.InvalidResponseError(
                "got no results key in json response"
            )

        result = contents.get('results', {})
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

        contents = response.json()

        if 'events_by_id' not in contents:
            raise exceptions.InvalidResponseError(
                "got no events_by_id key in json response"
            )

        events_by_id = contents.get('events_by_id', {})
        events = {
            event_id: Event.from_api_data(raw_event.get('event'))
            for event_id, raw_event in events_by_id.items()
        }
        return events

    def get_months(self, event_id, **kwargs):
        params = {'event_id': event_id}

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('months.v1', params)

        contents = response.json()

        if 'results' not in contents:
            raise exceptions.InvalidResponseError(
                "got no results key in json response"
            )

        result = contents.get('results', {})
        raw_months = result.get('month', [])

        months = [
            Month.from_api_data(data)
            for data in raw_months
        ]

        return months

    def list_performances(self, event_id, page_length=0, page=0, **kwargs):
        """
        List performances for a specified event
        """
        params = {'event_id': event_id}

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('performances.v1', params)

        contents = response.json()

        if 'results' not in contents:
            raise exceptions.InvalidResponseError(
                "got no results key in json response"
            )

        result = contents.get('results', {})

        raw_performances = result.get('performance', [])
        performances = [
            Performance.from_api_data(data)
            for data in raw_performances
        ]

        return performances

    def get_performances(self, performance_ids, **kwargs):
        """
        Get performances retrieves performances with the specific given id's
        """

        params = {
            'perf_id_list': ','.join(performance_ids),
        }

        self.add_optional_kwargs(params, **kwargs)

        response = self.make_request('performances_by_id.v1', params)

        contents = response.json()

        if 'performances_by_id' not in contents:
            raise exceptions.InvalidResponseError(
                "got no performances_by_id key in json response"
            )

        raw_performances = contents.get('performances_by_id', {})
        performances = {
            performance_id: Performance.from_api_data(data.get('performance'))
            for performance_id, data in raw_performances.items()
        }

        return performances

    def get_availability(self, performance_id, discounts=False,
                         example_seats=False, seat_blocks=False,
                         user_commission=False, **kwargs):
        """
        Fetch available tickets and prices for a given performance
        """
        params = {'perf_id': performance_id}

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

        contents = response.json()

        if contents.get('backend_is_broken'):
            raise exceptions.BackendBrokenError(
                'Error returned from upstream backend system'
            )

        if contents.get('backend_is_down'):
            raise exceptions.BackendDownError(
                'Unable to contact upstream backend system'
            )

        if contents.get('backend_throttle_failed'):
            raise exceptions.BackendThrottleError(
                'The call timed out while being queued for throttling'
            )

        if 'availability' not in contents:
            raise exceptions.InvalidResponseError(
                "got no availability key in json response"
            )

        meta = AvailabilityMeta.from_api_data(contents)

        raw_availability = contents.get('availability', {})

        availability = [
            TicketType.from_api_data(data)
            for data in raw_availability.get('ticket_type', [])
        ]

        return availability, meta

    def get_send_methods(self, performance_id):

        params = {'perf_id': performance_id}
        response = self.make_request('send_methods.v1', params)

        contents = response.json()

        if 'send_methods' not in contents:
            raise exceptions.InvalidResponseError(
                "got no send_methods key in json response"
            )

        raw_send_methods = contents.get('send_methods', {})

        send_methods = [
            SendMethod.from_api_data(data)
            for data in raw_send_methods.get('send_method', [])
        ]

        return send_methods

    def get_discounts(self, performance_id, ticket_type_code, price_band_code):
        params = {
            'perf_id': performance_id,
            'ticket_type_code': ticket_type_code,
            'price_band_code': price_band_code,
        }

        response = self.make_request('discounts.v1', params)

        contents = response.json()

        if 'discounts' not in contents:
            raise exceptions.InvalidResponseError(
                "got no discounts key in json response"
            )

        raw_discounts = contents.get('discounts', {})

        discounts = [
            Discount.from_api_data(data)
            for data in raw_discounts.get('discount', [])
        ]

        return discounts

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

        contents = response.json()

        trolley = Trolley.from_api_data(contents)

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

        contents = response.json()

        trolley = Trolley.from_api_data(contents)

        return trolley
