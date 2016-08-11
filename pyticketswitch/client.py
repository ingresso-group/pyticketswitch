import requests
import logging
from pyticketswitch import exceptions, utils
from pyticketswitch.interface.event import Event

logger = logging.getLogger(__name__)


class TicketSwitch(object):
    DEFAULT_ROOT_URL = "https://api.ticketswitch.com/cgi-bin"
    END_POINTS = {
        'events': 'json_events.exe',
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

    def search_events(self, event_ids=None, keywords=None, start_date=None,
                      end_date=None, country_code=None, city_code=None,
                      geolocation=None, include_dead=False,
                      include_non_live=False, order_by_popular=False,
                      req_extra_info=False, req_reviews=False, req_media=False,
                      req_cost_range=False, req_cost_range_details=False,
                      req_avail_details=False,
                      req_avail_details_with_perfs=False,
                      req_meta_components=False, req_custom_fields=False,
                      page=0, page_length=50):

        params = {}

        if event_ids:
            params.update(event_id_list=event_ids)

        if keywords:
            params.update(s_keys=','.join(keywords))

        if start_date or end_date:
            params.update(s_dates=utils.date_range_str(start_date, end_date))

        if country_code:
            params.update(s_coco=country_code)

        if city_code:
            params.update(s_city=city_code)

        if geolocation:
            params.update(s_geo=geolocation)

        if include_dead:
            params.update(include_dead=True)

        if include_non_live:
            params.update(include_non_live=True)

        if order_by_popular:
            params.update(s_top=True)

        if req_extra_info:
            params.update(req_extra_info=True)

        if req_reviews:
            params.update(req_reviews=True)

        if req_media:
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
            })

        if req_cost_range:
            params.update(req_cost_range=True)

        if req_cost_range_details:
            params.update(req_cost_range_details=True)

        if req_avail_details:
            params.update(req_avail_details=True)

        if req_avail_details_with_perfs:
            params.update(req_avail_details_with_perfs=True)

        if req_meta_components:
            params.update(req_meta_components=True)

        if req_custom_fields:
            params.update(req_custom_fields=True)

        params.update({
            'page_no': page,
            'page_len': page_length,
        })

        response = self.make_request('events', params)

        if not response.status_code == 200:
            raise exceptions.InvalidResponseError(
                "got status code `{}` from event search".format(
                    response.status_code
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

    def get_performances(self, event_id):
        pass
