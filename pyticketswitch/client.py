import requests
import logging
from pyticketswitch import exceptions, utils
from pyticketswitch.interface.event import Event
from pyticketswitch.interface.performance import Performance

logger = logging.getLogger(__name__)


class Client(object):
    DEFAULT_ROOT_URL = "https://api.ticketswitch.com/cgi-bin"
    END_POINTS = {
        'events': 'json_events.exe',
        'performances': 'json_performances.exe',
    }

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

    def get_end_point(self, method):
        if method not in self.END_POINTS:
            raise exceptions.EndPointMissingError(
                'no endpoint for method `{}`'.format(method),
                method,
            )

        end_point = '/{}'.format(self.END_POINTS[method])
        return end_point

    def get_url(self, method):
        user_path = self.get_user_path()
        end_point = self.get_end_point(method)
        url = "{url}{end_point}{user_path}/".format(
            url=self.url,
            user_path=user_path,
            end_point=end_point,
        )
        return url

    def get_password(self):
        """
        This is here so that it can be overwritten for differing auth methods
        """
        return self.password

    def make_request(self, method, params):
        url = self.get_url(method)
        params.update(user_passwd=self.get_password())
        response = requests.get(url, params=params)
        return response

    def get_events(self, keywords=None, start_date=None, end_date=None,
                   country_code=None, city=None, latitude=None, longitude=None,
                   radius=None, include_dead=False, include_non_live=False,
                   availability=False, availability_with_performances=False,
                   extra_info=False, reviews=False, media=False,
                   cost_range=False, best_value_offer=False,
                   max_saving_offer=False, min_cost_offer=False,
                   top_price_offer=False, no_singles_data=False,
                   cost_range_details=False, meta_components=False,
                   order_by_popular=False, event_ids=None, page=0,
                   page_length=0, **kwargs):

        """
        Search for events with the given parameters
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

        if event_ids:
            params.update(event_id_list=','.join(event_ids))

        if page > 0:
            params.update(page_no=page)
        if page_length > 0:
            params.update(page_len=page_length)

        params.update(kwargs)

        response = self.make_request('events', params)

        if not response.status_code == 200:
            raise exceptions.InvalidResponseError(
                "got status code `{}` from {}".format(
                    response.status_code,
                    self.END_POINTS['events'],
                )
            )

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

    def get_performances(self, event_id, availability=False,
                         cost_range=False, best_value_offer=False,
                         max_saving_offer=False, min_cost_offer=False,
                         top_price_offer=False, no_singles_data=False,
                         performance_ids=None, page_length=0, page=0,
                         **kwargs):
        """
        Get performances for a specified event


        json_performances returns a list of performances and a list of events
        that they belong to. This is due to meta events, where an event is a
        composite of a collection of other events. As such this method parses
        both the performance and event list, and maps each performance to it's
        relevant event

        TODO: Workout if we should be returning the event list as well.
        """
        params = {'event_id': event_id}

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

        if availability:
            params.update(req_avail_details=True)

        params.update(kwargs)

        response = self.make_request('performances', params)

        if not response.status_code == 200:
            raise exceptions.InvalidResponseError(
                "got status code `{}` from {}".format(
                    response.status_code,
                    self.END_POINTS['performances'],
                )
            )

        contents = response.json()

        if 'results' not in contents:
            raise exceptions.InvalidResponseError(
                "got no results key in json response"
            )

        result = contents.get('results', {})

        raw_events = result.get('events_by_id', {})
        events = {
            event_id: Event.from_api_data(event.get('event'))
            for event_id, event in raw_events.items()
            if event.get('event')
        }

        raw_performances = result.get('performance', [])
        performances = [
            Performance.from_api_data(
                data,
                events.get(data.get('event_id'))
            )
            for data in raw_performances
        ]

        return performances


