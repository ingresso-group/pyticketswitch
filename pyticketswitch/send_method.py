from pyticketswitch.country import Country
from pyticketswitch.mixins import JSONMixin


class SendMethod(JSONMixin, object):
    """Describes a method of sending tickets to a customer.

    Attributes:
        code (str): identifier for the send method.
        cost (float): additional cost to the customer for this send method.
        description (str): human readable description of the send method.
        type (str): indicates the type of the send method.
        permitted_countries (list): list of
            :class:`Countries <pyticketswitch.country.Country>` in which the
            customer lives where this send method is permitted.

    """

    def __init__(self, code, cost=None, description=None, typ=None,
                 permitted_countries=None):
        self.code = code
        self.cost = cost
        self.description = description
        self.type = typ
        self.permitted_countries = permitted_countries

    @classmethod
    def from_api_data(cls, data):
        """Creates a new SendMethod object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a send method.

        Returns:
            :class:`SendMethod <pyticketswitch.send_method.SendMethod>`: a new
            :class:`SendMethod <pyticketswitch.send_method.SendMethod>` object
            populated with the data from the api.

        """
        kwargs = {
            'code': data.get('send_code'),
            'description': data.get('send_desc'),
            'typ': data.get('send_type'),
        }

        cost = data.get('send_cost', 0.0)
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

    def __repr__(self):
        return u'<SendMethod {}:{}>'.format(
            self.code, self.description.encode('ascii', 'ignore'))
