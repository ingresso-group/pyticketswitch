from pyticketswitch.mixins import JSONMixin


class Commission(JSONMixin, object):
    """Commission payable to the user on the sale of a specfic order.

    Attributes:
       including_vat (float): the amount payable including value added tax.
       excluding_vat (float): the amount payable excluding value added tax.
       currency_code (str): the currency code the commission is priced in.
    """

    def __init__(self, including_vat, excluding_vat, currency_code):
        self.including_vat = including_vat
        self.excluding_vat = excluding_vat
        self.currency_code = currency_code

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Commission object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a commission payable to the user.

        Returns:
            :class:`Commission <pyticketswitch.commission.Commission>`: a new
            :class:`Commission <pyticketswitch.commission.Commission>` object
            populated with the data from the api.

        """

        kwargs = {
            'including_vat': data.get('amount_including_vat'),
            'excluding_vat': data.get('amount_excluding_vat'),
            'currency_code': data.get('commission_currency_code'),
        }

        return cls(**kwargs)
