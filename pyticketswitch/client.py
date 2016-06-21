import requests
from pyticketswitch import exceptions, utils, interface


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
            user_path = '/{}/{}/{}'.format(self.user, self.sub_user, self.language)

        if self.language and not self.sub_user:
            user_path = '/{}/-/{}'.format(self.user, self.language)

        return user_path

    def get_end_point(self, method):
        if method not in self.END_POINTS:
            raise exceptions.EndPointMissingError(
                'no endpoint for method `{}`'.format(method)
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

    def search_events(self, keywords=None, start_date=None, end_date=None,
                      country_code=None, page=0, page_length=50,
                      dead_events=False, non_live=False):

        params = {}

        if keywords:
            params.update(s_keys=keywords)

        if start_date or end_date:
            params.update(s_dates=utils.date_range_str(start_date, end_date))

        if country_code:
            params.update(s_coco=country_code)

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
            interface.Event.from_json(data)
            for data in raw_events
        ]

        return events
