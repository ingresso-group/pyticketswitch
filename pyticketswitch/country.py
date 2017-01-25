from pyticketswitch.mixins import JSONMixin


class Country(JSONMixin, object):

    def __init__(self, code, description=None):
        self.code = code
        self.description = description

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'code': data.get('country_code'),
            'description': data.get('country_desc'),
        }

        return cls(**kwargs)
