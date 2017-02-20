from pyticketswitch.mixins import JSONMixin


class Integration(JSONMixin, object):

    def __init__(self, typ, amount=None, base_amount=None, currency=None,
                 data=None):
        self.type = typ
        self.amount = amount
        self.base_amount = base_amount
        self.currency = currency
        self.data = data

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'typ': data.get('debitor_type'),
            'amount': data.get('debit_amount'),
            'base_amount': data.get('debit_base_amount'),
            'currency': data.get('debit_currency'),
            'data': data.get('debitor_specific_data'),
        }

        return cls(**kwargs)


class Callout(JSONMixin, object):

    def __init__(self, html=None, integration=None):

        self.html = html
        self.integration = integration

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'html': data.get('redirect_html_page_data')
        }

        integration = data.get('debitor_integration_data')

        if integration:
            kwargs.update(integration=Integration.from_api_data(integration))

        return cls(**kwargs)
