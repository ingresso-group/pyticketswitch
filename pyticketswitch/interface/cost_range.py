from pyticketswitch.interface.currency import Currency


class CostRange(object):

    def __init__(self, valid_quantity_mask=0, max_surcharge=0, max_seatprice=0,
                 min_surcharge=0, min_seatprice=0, allows_singles=True,
                 currency=None):

        self.valid_quantity_mask = valid_quantity_mask
        self.max_surcharge = max_surcharge
        self.max_seatprice = max_seatprice
        self.min_surcharge = min_surcharge
        self.min_seatprice = min_seatprice
        self.currency = currency

    @classmethod
    def from_api_data(cls, data):

        quantity_options = data.get('quantity_options', {})
        currency = Currency.from_api_data(data.get('range_currency', {}))
        kwargs = {
            'valid_quantity_mask': quantity_options.get('valid_quantity_mask', 0),
            'min_surcharge': data.get('min_surcharge', 0),
            'min_seatprice': data.get('min_seatprice', 0),
            'max_surcharge': data.get('max_surcharge', 0),
            'max_seatprice': data.get('max_seatprice', 0),
            'allows_singles': data.get('singles', True),
            'currency': currency,
        }
        return cls(**kwargs)
