import datetime
from pyticketswitch.interface.currency import Currency


class Availability(object):

    def __init__(self, valid_quantity_mask=0, day_mask=0, currency=None,
                 first_date=None, last_date=None, seatprice=0,
                 surcharge=0):

        self.valid_quantity_mask = valid_quantity_mask
        self.day_mask = day_mask
        self.first_date = first_date
        self.last_date = last_date
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.currency = currency

    @classmethod
    def from_api_data(cls, data):

        quantity = data.get('quantity_options', {})

        currency = Currency.from_api_data(data.get('avail_currency', {}))

        dates = data.get('available_dates', {})
        api_first_date = dates.get('first_yyyymmdd', None)
        api_last_date = dates.get('last_yyyymmdd', None)
        first_date = None
        last_date = None

        if api_first_date:
            first_date = datetime.datetime.strptime(api_first_date, '%Y%m%d').date()
        if api_last_date:
            last_date = datetime.datetime.strptime(api_last_date, '%Y%m%d').date()

        kwargs = {
            'valid_quantity_mask': quantity.get('valid_quantity_mask', 0),
            'day_mask': data.get('day_mask', 0),
            'currency': currency,
            'first_date': first_date,
            'last_date': last_date,
            'seatprice': data.get('seatprice', 0),
            'surcharge': data.get('surcharge', 0),
        }

        return cls(**kwargs)
