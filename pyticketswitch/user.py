from pyticketswitch.mixins import JSONMixin


class User(JSONMixin, object):
    """Describes a user of the API

    Attributes:
        id (str): the user identifier.
        name (str): human readable name.
        country (str): ISO 3166-1 country code.
        sub_user (str): the identifier of the sub user.
        is_b2b (bool): indicates that the account is a b2b account.
        statement_descriptor (str): what will appear on a customers bank
            statement when ingresso takes the payment.
        backend_group (str): what product group a user belongs to. Users in
            the same backend_group will see the same products.
        content_group (str): what content group a user belongs to. Users in
            the same content_group will see the same textual and graphical
            content.

    """
    def __init__(self, id_, name=None, country=None, sub_user=None,
                 is_b2b=False, statement_descriptor=None,
                 backend_group=None, content_group=None):

        self.id = id_
        self.name = name
        self.country = country
        self.sub_user = sub_user
        self.is_b2b = is_b2b
        self.statement_descriptor = statement_descriptor
        self.backend_group = backend_group
        self.content_group = content_group

    @classmethod
    def from_api_data(cls, data):
        """Creates a new User object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a user.

        Returns:
            :class:`User <pyticketswitch.user.User>`: a new
            :class:`User <pyticketswitch.user.User>` object
            populated with the data from the api.

        """
        return cls(
            data.get('user_id'),
            name=data.get('real_name'),
            country=data.get('default_country_code'),
            sub_user=data.get('sub_user'),
            is_b2b=data.get('is_b2b'),
            statement_descriptor=data.get('statement_descriptor'),
            backend_group=data.get('backend_group'),
            content_group=data.get('content_group'),
        )
