from pyticketswitch.interface.currency import Currency
from pyticketswitch.utils import bitmask_to_numbered_list


class CostRange(object):

    def __init__(self, valid_quantities=None, max_surcharge=None, max_seatprice=None,
                 min_surcharge=None, min_seatprice=None, allows_singles=True,
                 currency=None):

        self.valid_quantities = valid_quantities
        self.max_seatprice = max_seatprice
        self.max_surcharge = max_surcharge
        self.min_seatprice = min_seatprice
        self.min_surcharge = min_surcharge
        self.currency = currency

    @classmethod
    def from_api_data(cls, data):

        quantity_options = data.get('quantity_options', {})
        currency = Currency.from_api_data(data.get('range_currency', {}))
        kwargs = {
            'valid_quantities': bitmask_to_numbered_list(
                quantity_options.get('valid_quantity_mask', 0)
            ),
            'min_surcharge': float(data.get('min_surcharge', 0)),
            'min_seatprice': float(data.get('min_seatprice', 0)),
            'max_surcharge': float(data.get('max_surcharge', 0)),
            'max_seatprice': float(data.get('max_seatprice', 0)),
            'allows_singles': data.get('singles', True),
            'currency': currency,
        }
        return cls(**kwargs)
