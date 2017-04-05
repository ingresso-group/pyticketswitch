from pyticketswitch.mixins import JSONMixin


class Address(JSONMixin, object):
    """A postal address.

    TODO: this is very similar the Customer object. consider combining them,
    or subclassing one from the other, or a base class of some sort.

    Attributes:
        lines (list): list of address lines.
        town (str): town for the address.
        county (str): the county or region of the address.
        country_code (str): ISO 3166-1 country code.
        post_code (str): post or ZIP code for the address.
        email (str): a contact email address.
        home_phone (str): a contact home phone number.
        work_phone (str): a contact work phone number.

    """

    def __init__(self, lines=None, country_code=None, county=None,
                 email=None, home_phone=None, post_code=None, town=None,
                 work_phone=None):

        self.lines = lines
        self.town = town
        self.county = county
        self.country_code = country_code
        self.post_code = post_code
        self.email = email
        self.home_phone = home_phone
        self.work_phone = work_phone

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Address object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns an address.

        Returns:
            :class:`Address <pyticketswitch.address.Address>`: a new
            :class:`Address <pyticketswitch.address.Address>` object
            populated with the data from the api.

        """
        kwargs = {
            'country_code': data.get('country_code'),
            'county': data.get('county'),
            'email': data.get('email_address'),
            'home_phone': data.get('home_phone'),
            'post_code': data.get('postcode'),
            'town': data.get('town'),
            'work_phone': data.get('work_phone'),
            'lines': [
                data.get('address_line_one'),
                data.get('address_line_two'),
            ]
        }

        return cls(**kwargs)

    def as_api_billing_address_parameters(self):

        params = {
            'billing_country_code': self.country_code,
            'billing_postcode': self.post_code,
            'billing_town': self.town,
            'billing_county': self.county,
        }

        if self.lines and len(self.lines) == 1:
            params.update(billing_address_line_one=self.lines[0])

        if self.lines and len(self.lines) > 1:
            params.update(
                billing_address_line_one=self.lines[0],
                billing_address_line_two=self.lines[1],
            )
        return params
