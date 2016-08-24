from pyticketswitch import utils
from pyticketswitch.interface.currency import Currency


class Availability(object):

    def __init__(self, valid_quantity_flags=None, available_weekdays=None, currency=None,
                 first_date=None, last_date=None, specific_dates=None,
                 seatprice=0, surcharge=0):

        self.valid_quantity_flags = valid_quantity_flags
        self.available_weekdays = available_weekdays
        self.first_date = first_date
        self.last_date = last_date
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.currency = currency
        self.specific_dates = specific_dates

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
            first_date = utils.yyyymmdd_to_date(api_first_date)
        if api_last_date:
            last_date = utils.yyyymmdd_to_date(api_last_date)

        specific_dates = utils.specific_dates_from_api_data(dates)

        kwargs = {
            'valid_quantity_flags': quantity.get('valid_quantity_flags', None),
            'available_weekdays': data.get('available_weekdays', None),
            'specific_dates': specific_dates,
            'currency': currency,
            'first_date': first_date,
            'last_date': last_date,
            'seatprice': data.get('seatprice', 0),
            'surcharge': data.get('surcharge', 0),
        }

        return cls(**kwargs)
