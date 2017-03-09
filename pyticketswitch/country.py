from pyticketswitch.mixins import JSONMixin


class Country(JSONMixin, object):
    """Represents a country

    Attributes:
        code (str):  ISO 3166-1 country code.
        description (str): a human readable name for the country.

    """

    def __init__(self, code, description=None):
        self.code = code
        self.description = description

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Country object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a country.

        Returns:
            :class:`Country <pyticketswitch.country.Country>`: a new
            :class:`Country <pyticketswitch.country.Country>` object
            populated with the data from the api.

        """

        kwargs = {
            'code': data.get('country_code'),
            'description': data.get('country_desc'),
        }

        return cls(**kwargs)

    def __repr__(self):
        return u'<Country {}:{}>'.format(
            self.code, self.description.encode('ascii', 'ignore'))
