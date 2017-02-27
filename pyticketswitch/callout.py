from pyticketswitch.mixins import JSONMixin


class Integration(JSONMixin, object):
    """Information to use when integrating payment methods into clients.

    Attributes:
        type (str): the debitor type.
        amount (float): the amount to be debited.
        amount_base (int): the precise amount. see currency for places.
        currency (str): the currency code.
        data (dict): debitor specific information.

    """

    def __init__(self, typ, amount=None, base_amount=None, currency=None,
                 data=None):
        self.type = typ
        self.amount = amount
        self.base_amount = base_amount
        self.currency = currency
        self.data = data

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Integration object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns the integration.

        Returns:
            :class:`Integration <pyticketswitch.callout.Integration>`: a new
            :class:`Integration <pyticketswitch.callout.Integration>` object
            populated with the data from the api.

        """

        kwargs = {
            'typ': data.get('debitor_type'),
            'amount': data.get('debit_amount'),
            'base_amount': data.get('debit_base_amount'),
            'currency': data.get('debit_currency'),
            'data': data.get('debitor_specific_data'),
        }

        return cls(**kwargs)


class Callout(JSONMixin, object):
    """Information about a redirection required by a 3rd party the payment provider.

    Attributes:
        html (str): a blob of HTML that can be rendered to produce either the
            required redirect or the form to continue with the transaction.
        integration (:class:`Integration <pyticketswitch.callout.Integration>`):
            data relevant to the debitor that the customer will be redirected
            to.

    """

    def __init__(self, html=None, integration=None):

        self.html = html
        self.integration = integration

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Callout object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a callout.

        Returns:
            :class:`Callout <pyticketswitch.callout.Callout>`: a new
            :class:`Callout <pyticketswitch.callout.Callout>` object
            populated with the data from the api.

        """

        kwargs = {
            'html': data.get('redirect_html_page_data')
        }

        integration = data.get('debitor_integration_data')

        if integration:
            kwargs.update(integration=Integration.from_api_data(integration))

        return cls(**kwargs)
