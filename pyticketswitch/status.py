from pyticketswitch.trolley import Trolley
from pyticketswitch.user import User
from pyticketswitch.utils import isostr_to_datetime
from pyticketswitch.mixins import JSONMixin


class Status(JSONMixin, object):
    """Describes the current state of a transaction

    Attributes:
        status (str): the currency status of the transaction.
        reserved_at (datetime.datetime): the date and time when the transaction
            was reserved.
        purchased_at (datetime.datetime): the date and time when the transaction
            was purchased.
        trolley (:class:`Trolley <pyticketswitch.trolley.Trolley>`): the
            contents of the transactions trolley.
        external_sale_page (str): the page that was rendered to the customer
            after the transaction was completed. This is only available if
            it was passed into the API at purchase time.
        languages (list): list of IETF language tags relevant to the
            transaction.
        remote_site (str): the remote site the transaction was reserved and
            purchased under.
        reserve_user (:class:`User <pyticketswitch.user.User>`): the user that
            was used to reserve the transaction.

    """

    def __init__(self, status=None, reserved_at=None, trolley=None,
                 purchased_at=None, external_sale_page=None,
                 languages=None, remote_site=None, reserve_user=None):
        self.status = status
        self.reserved_at = reserved_at
        self.purchased_at = purchased_at
        self.trolley = trolley
        self.external_sale_page = external_sale_page
        self.languages = languages
        self.remote_site = remote_site
        self.reserve_user = reserve_user

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Status object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a transactions state.

        Returns:
            :class:`Status <pyticketswitch.status.Status>`: a new
            :class:`Status <pyticketswitch.status.Status>` object
            populated with the data from the api.

        """
        kwargs = {
            'status': data.get('transaction_status'),
            'trolley': Trolley.from_api_data(data),
            'remote_site': data.get('remote_site'),
        }

        reserved_raw = data.get('reserve_iso8601_date_and_time')
        if reserved_raw:
            kwargs.update(reserved_at=isostr_to_datetime(reserved_raw))

        purchased_raw = data.get('purchase_iso8601_date_and_time')
        if purchased_raw:
            kwargs.update(purchased_at=isostr_to_datetime(purchased_raw))

        external_sale_page_raw = data.get('external_sale_page_raw')
        if external_sale_page_raw:
            raise NotImplemented("don't know what this looks like yet")

        reserve_user_data = data.get('reserve_user')
        if reserve_user_data:
            reserve_user = User.from_api_data(reserve_user_data)
            kwargs.update(reserve_user=reserve_user)

        languages_raw = data.get('language_list')
        if languages_raw:
            kwargs.update(languages=languages_raw.split(','))

        return cls(**kwargs)
