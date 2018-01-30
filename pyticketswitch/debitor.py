from pyticketswitch.mixins import JSONMixin


class Debitor(JSONMixin, object):
    """Information about a 3rd party that will take payment from your customer.

    This information is primarily used for bypassing callouts an integrating
    directly with payment providers on the front end.

    When your account is set up to sell on credit (i.e. you are always taking
    payment from the customer in your application directly), this information
    will not be present, and it should not be relevant.

    When the source system is taking payment this information will not be
    present.

    When debitor information is not present or you are not front end
    integrating you should refer to the
    :attr:`Reservation.needs_payment_card
    <pyticketswitch.reservation.Reservation.needs_payment_card>`,
    :attr:`Reservation.needs_email_address
    <pyticketswitch.reservation.Reservation.needs_email_address>`, and
    :attr:`Reservation.needs_agent_reference
    <pyticketswitch.reservation.Reservation.needs_agent_reference>` attributes
    as to what information you need to pass back to the API for purchasing
    tickets.

    Regardless of the debitor it's advisable to implement the full
    purchase/callout/callback process in the event that your front end
    integration goes awry.

    :ref:`See front end integrations for more information
    <frontend_integrations>`

    Attributes:
        type (str): all debitors with the same type can be assumed to integrate
            in the same manor, however their parameters and integration data
            might be different.
        name (str): name of the specific implementation of the debitor.
        description (str): human readable description of the debitor.
        integration_data (dict): data used to do front end integrations. For
            the format of this data please consult :ref:`the documentation for
            the relevant debitor type <frontend_integrations>`.
        aggregation_key (str): a key used to identify if debitors are the same
            for purposes of payment aggregation between bundles
    """

    def __init__(self, typ=None, name=None, description=None,
                 integration_data=None, aggregation_key=None):
        self.type = typ
        self.name = name
        self.description = description
        self.integration_data = integration_data
        self.aggregation_key = aggregation_key

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'typ': data.get('debitor_type'),
            'name': data.get('debitor_name'),
            'description': data.get('debitor_desc'),
            'integration_data': data.get('debitor_integration_data', {}),
            'aggregation_key': data.get('debitor_aggregation_key'),
        }

        return cls(**kwargs)

    def __repr__(self):
        return u'<Debitor {}:{}>'.format(self.type, self.name)
