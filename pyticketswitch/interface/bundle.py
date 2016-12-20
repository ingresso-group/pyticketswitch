from pyticketswitch.interface.currency import Currency
from pyticketswitch.interface.order import Order


class Bundle(object):

    def __init__(self, source_code, orders=None, description=None,
                 total_seatprice=None, total_surcharge=None,
                 total_send_cost=None, total=None, currency=None):
        self.source_code = source_code
        self.orders = orders
        self.description = description
        self.total_seatprice = total_seatprice
        self.total_surcharge = total_surcharge
        self.total_send_cost = total_send_cost
        self.total = total
        self.currency = currency

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'source_code': data.get('bundle_source_code'),
            'description': data.get('bundle_source_desc'),
        }

        raw_currency = data.get('currency')
        if raw_currency:
            currency = Currency.from_api_data(raw_currency)
            kwargs.update(currency=currency)

        raw_orders = data.get('order')
        if raw_orders:
            orders = [Order.from_api_data(order) for order in raw_orders]
            kwargs.update(orders=orders)

        # Below we are explicital checking for not None because we want to
        # differentiate between situtations where a value is 0 and a value is
        # missing from the response.
        total_seatprice = data.get('bundle_total_seatprice')
        if total_seatprice is not None:
            kwargs.update(total_seatprice=float(total_seatprice))

        total_surcharge = data.get('bundle_total_surcharge')
        if total_surcharge is not None:
            kwargs.update(total_surcharge=float(total_surcharge))

        total_send_cost = data.get('bundle_total_send_cost')
        if total_send_cost is not None:
            kwargs.update(total_send_cost=float(total_send_cost))

        total = data.get('bundle_total_cost')
        if total is not None:
            kwargs.update(total=float(total))

        return cls(**kwargs)
