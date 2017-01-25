from pyticketswitch.country import Country
from pyticketswitch.mixins import JSONMixin


class SendMethod(JSONMixin, object):

    def __init__(self, code, cost=None, description=None, typ=None,
                 permitted_countries=None):
        self.code = code
        self.cost = cost
        self.description = description
        self.typ = typ
        self.permitted_countries = permitted_countries

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'code': data.get('send_code'),
            'description': data.get('send_desc'),
            'typ': data.get('send_type'),
        }

        cost = data.get('send_cost')
        if cost:
            kwargs.update(cost=float(cost))

        permitted_countries_raw = data.get('permitted_countries', {})

        if permitted_countries_raw:
            permitted_countries_raw = permitted_countries_raw.get('country', [])

            permitted_countries = [
                Country.from_api_data(country)
                for country in permitted_countries_raw
            ]

            kwargs.update(permitted_countries=permitted_countries)

        return cls(**kwargs)
