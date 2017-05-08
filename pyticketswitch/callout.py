from collections import OrderedDict
from pyticketswitch.mixins import JSONMixin
from pyticketswitch.debitor import Debitor


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
        code (str): the identifier for the source system of the
            bundle this callout will be paying for.
        description: the human readable description for the source
            system.
        total (float): the total amount of money that will be payable.
        type (str): the HTTP method that should be used to send the customer
            to the destination.
        destination (str): the destination url to send your user to.
        parameters (:py:class:`collections.OrderedDict`): dictionary of key
            value pairs that the 3rd party is expecting as query string
            parameters or form parameters.
        html (str): a blob of HTML that can be rendered to produce either the
            required redirect or the form to continue with the transaction.
        integration_data (dict):
            data relevant to the debitor that the customer will be redirected
            to. This *may* provide a opertunity to integrate directly. Consult
            documentation for more details.
        debitor (:class:`Debitor <pyticketswitch.debitor.Debitor>`): the debitor
            information that can be used for a front end integration.
        return_token (str): return token specified in the last purchase or
            callback call.
    """

    def __init__(self, code=None, description=None, total=None, typ=None,
                 destination=None, parameters=None, integration_data=None,
                 debitor=None, currency_code=None, return_token=None):

        self.code = code
        self.description = description
        self.total = total
        self.type = typ
        self.destination = destination
        self.parameters = parameters
        self.integration_data = integration_data
        self.debitor = debitor
        self.currency_code = currency_code
        self.return_token = return_token

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
            'code': data.get('bundle_source_code'),
            'description': data.get('bundle_source_desc'),
            'total': data.get('bundle_total_cost'),
            'destination': data.get('callout_destination_url'),
            'typ': data.get('callout_type'),
            'currency_code': data.get('currency_code'),
            'return_token': data.get('return_token'),
        }

        integration_data = data.get('callout_integration_data')

        if integration_data:
            kwargs.update(integration_data=integration_data)

        raw_debitor = data.get('debitor')
        if raw_debitor:
            debitor = Debitor.from_api_data(raw_debitor)
            kwargs.update(debitor=debitor)

        raw_parameters = data.get('callout_parameters')
        parameter_order = data.get('callout_parameters_order')

        if raw_parameters:
            if parameter_order:
                ordered_parameters = (
                    [key, raw_parameters[key]]
                    for key in parameter_order
                )
                parameters = OrderedDict(ordered_parameters)
            else:
                parameters = OrderedDict(raw_parameters.items())

            kwargs.update(parameters=parameters)

        return cls(**kwargs)

    def __repr__(self):
        return u'<Callout {}:{}>'.format(self.code, self.return_token)
