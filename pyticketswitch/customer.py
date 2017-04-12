from pyticketswitch.mixins import JSONMixin
from pyticketswitch import utils


class Customer (JSONMixin, object):
    """Describes a cutomer to ticketswitch.

    Attributes:
        first_name (str): customers first name.
        last_name (str): customers last name.
        address_lines (list): list of address lines, at least one address line
            is required.
        country_code (str): ISO 3166-1 country code that the customer is living
            in.
        title (str): customer title.
        initials (str): customer initials.
        suffix (str): customer name suffix.
        email (str): email address for contacting the customer.
        post_code (str): post or ZIP code for the customers address.
        town (str): town for the customers address.
        county (str): the county or region of the customers address.
        country (str): the country as a string for the customers address.
        phone (str): a contact phone number for the user.
        home_phone (str): the customers home phone number.
        work_phone (str): the customers work phone number.
        agent_reference (str): agent reference for the customer.
        supplier_can_use_data (bool): indicates that the supplier of the
            tickets is allowed to access and use this data.
        user_can_use_data (bool): indicates that the user (you) can access and
            use this data.
        world_can_use_data (bool): indicates that pretty much anyone is allowed
            to access and use this data.
        first_name_latin (str): **first name** in latin characters.
        last_name_latin (str): **last name** in latin characters.
        address_lines_latin (list): list of :obj:`str` address lines in latin
            characters.
        title_latin (str): **title** in latin characters
        initials_latin (str): **initials** in latin characters.
        suffix_latin (str): **suffix** in latin characters.
        post_code_latin (str): **post_code** in latin characters.
        town_latin (str): **town** in latin characters.
        county_latin (str): **county** in latin characters.
        country_latin (str): **country** in latin characters.
        kwargs (dict): arbitrary keyword arguments to store along with this
            customer object.

    """

    def __init__(self, first_name, last_name, address_lines, country_code,
                 title=None, initials=None, suffix=None, email=None,
                 post_code=None, town=None, county=None, country=None,
                 phone=None, home_phone=None, work_phone=None,
                 agent_reference=None, supplier_can_use_data=False,
                 user_can_use_data=False, world_can_use_data=False,
                 first_name_latin=None, last_name_latin=None,
                 address_lines_latin=None, title_latin=None,
                 initials_latin=None, suffix_latin=None, post_code_latin=None,
                 town_latin=None, county_latin=None, country_latin=None,
                 **kwargs):

        self.first_name = first_name
        self.first_name_latin = first_name_latin

        self.last_name = last_name
        self.last_name_latin = last_name_latin

        self.address_lines = address_lines
        self.address_lines_latin = address_lines_latin

        self.title = title
        self.title_latin = title_latin
        self.initials = initials
        self.initials_latin = initials_latin
        self.suffix = suffix
        self.suffix_latin = suffix_latin

        self.country_code = country_code
        self.post_code = post_code
        self.post_code_latin = post_code_latin
        self.town = town
        self.town_latin = town_latin
        self.county = county
        self.county_latin = county_latin
        self.country = country
        self.country_latin = country_latin

        self.email = email
        self.phone = phone
        self.home_phone = home_phone
        self.work_phone = work_phone

        self.agent_reference = agent_reference

        self.supplier_can_use_data = supplier_can_use_data
        self.user_can_use_data = user_can_use_data
        self.world_can_use_data = world_can_use_data
        self.kwargs = kwargs

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Customer object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a customer.

        Returns:
            :class:`Customer <pyticketswitch.customer.Customer>`: a new
            :class:`Customer <pyticketswitch.customer.Customer>` object
            populated with the data from the api.

        """
        kwargs = {
            'first_name': data.get('first_name'),
            'first_name_latin': data.get('first_name_latin'),
            'last_name': data.get('last_name'),
            'last_name_latin': data.get('last_name_latin'),
            'title': data.get('title'),
            'title_latin': data.get('title_latin'),
            'initials': data.get('initials'),
            'initials_latin': data.get('initials_latin'),
            'suffix': data.get('suffix'),
            'suffix_latin': data.get('suffix_latin'),
            'country_code': data.get('country_code'),
            'post_code': data.get('postcode'),
            'post_code_latin': data.get('postcode_latin'),
            'town': data.get('town'),
            'town_latin': data.get('town_latin'),
            'county': data.get('county'),
            'county_latin': data.get('county_latin'),
            'country': data.get('country'),
            'country_latin': data.get('country_latin'),
            'email': data.get('email_addr'),
            'phone': data.get('phone'),
            'home_phone': data.get('home_phone'),
            'work_phone': data.get('work_phone'),
            'agent_reference': data.get('agent_ref'),
            'supplier_can_use_data': data.get('dp_supplier'),
            'user_can_use_data': data.get('dp_user'),
            'world_can_use_data': data.get('dp_world'),
        }

        address_line_one = data.get('addr_line_one')
        address_line_two = data.get('addr_line_two')

        address_line_one_latin = data.get('addr_line_one_latin')
        address_line_two_latin = data.get('addr_line_two_latin')

        address_lines = []

        if address_line_one:
            address_lines.append(address_line_one)

        if address_line_two:
            address_lines.append(address_line_two)

        address_lines_latin = []

        if address_line_one_latin:
            address_lines_latin.append(address_line_one_latin)

        if address_line_two_latin:
            address_lines_latin.append(address_line_two_latin)

        kwargs.update(
            address_lines=address_lines,
            address_lines_latin=address_lines_latin
        )

        return cls(**kwargs)

    def as_api_parameters(self):
        """Generates a dictionary of parameters to be passed back to the API.

        Returns:
            dict: a set of parameters describing the customer to the API.

        .. note:: the ``latin_*`` attributes are not passed to the API
                   as they are generated internally. As such there is no need
                   to provided them when creating a
                   :class:`Customer <pyticketswitch.customer.Customer>` for
                   API consumption.

        """

        params = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'country_code': self.country_code,
            'title': self.title,
            'initials': self.initials,
            'suffix': self.suffix,
            'postcode': self.post_code,
            'town': self.town,
            'county': self.county,
            'email_address': self.email,
            'phone': self.phone,
            'work_phone': self.work_phone,
            'home_phone': self.home_phone,
            'agent_ref': self.agent_reference,
            'supplier_can_use_customer_data': self.supplier_can_use_data,
            'user_can_use_customer_data': self.user_can_use_data,
            'world_can_use_customer_data': self.world_can_use_data,
        }

        if self.address_lines and len(self.address_lines) == 1:
            params.update(address_line_one=self.address_lines[0])

        if self.address_lines and len(self.address_lines) > 1:
            params.update(
                address_line_one=self.address_lines[0],
                address_line_two=self.address_lines[1],
            )

        params = utils.filter_none_from_parameters(params)
        return params
