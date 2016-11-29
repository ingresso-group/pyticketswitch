import datetime
from pyticketswitch.utils import bitmask_to_numbered_list
from pyticketswitch.interface.currency import Currency

MONTH_NUMBERS = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7,
    'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}


class AvailabilityMeta(object):

    def __init__(self, can_leave_singles=True,
                 contiguous_seat_selection_only=True,
                 currency=None, valid_quantities=None):
        self.can_leave_singles = can_leave_singles
        self.contiguous_seat_selection_only = contiguous_seat_selection_only
        self.currency = currency
        self.valid_quantities = valid_quantities

    @classmethod
    def from_api_data(cls, data):
        quantity_options = data.get('quantity_options', {})
        valid_quantity_flags = quantity_options.get('valid_quantity_flags', [])

        valid_quantities = [
            i+1 for i, flag in enumerate(valid_quantity_flags)
            if flag
        ]

        kwargs = {
            'can_leave_singles': data.get('can_leave_singles', True),
            'contiguous_seat_selection_only':
                data.get('contiguous_seat_selection_only', True),
            'valid_quantities': valid_quantities,
        }

        if 'currency' in data:
            currency = Currency.from_api_data(data.get('currency'))
            kwargs.update(currency=currency)

        return cls(**kwargs)


class AvailabilityDetails(object):

    def __init__(self, ticket_type=None, price_band=None,
                 ticket_type_description=None, price_band_description=None,
                 seatprice=None, surcharge=None, currency=None,
                 first_date=None, last_date=None, calendar_masks=None,
                 weekday_mask=None, valid_quanities=None):

        self.ticket_type = ticket_type
        self.ticket_type_description = ticket_type_description
        self.price_band = price_band
        self.price_band_description = price_band_description
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.currency = currency
        self.first_date = first_date
        self.last_date = last_date
        self._calendar_masks = calendar_masks
        self.weekday_mask = weekday_mask
        self.valid_quanities = valid_quanities

    @classmethod
    def from_api_data(cls, data):
        details = []

        for ticket_type in data.get('ticket_type', []):
            kwargs = {
                'ticket_type': ticket_type.get('ticket_type_code'),
                'ticket_type_description': ticket_type.get('ticket_type_desc'),
            }

            for price_band in ticket_type.get('price_band', []):
                kwargs.update(
                    price_band=price_band.get('price_band_code'),
                    price_band_description=price_band.get('price_band_desc'),
                )

                raw_details_list = price_band.get('avail_detail', [{}])
                raw_details = raw_details_list[0]

                if 'seatprice' in raw_details:
                    kwargs['seatprice'] = raw_details['seatprice']

                if 'surcharge' in raw_details:
                    kwargs['surcharge'] = raw_details['surcharge']

                if 'avail_currency' in raw_details:
                    kwargs['currency'] = Currency.from_api_data(
                        raw_details.get('avail_currency')
                    )

                available_dates = raw_details.get('available_dates', {})
                if 'first_yyyymmdd' in available_dates:
                    first = datetime.datetime.strptime(
                        available_dates['first_yyyymmdd'],
                        '%Y%m%d'
                    )
                    kwargs['first_date'] = first.date()

                if 'last_yyyymmdd' in available_dates:
                    last = datetime.datetime.strptime(
                        available_dates['last_yyyymmdd'],
                        '%Y%m%d'
                    )
                    kwargs['last_date'] = last.date()

                kwargs['calendar_masks'] = {
                    int(year[5:]): {
                        MONTH_NUMBERS[month[:3]]: mask
                        for month, mask in month_masks.items()
                    }
                    for year, month_masks in available_dates.items()
                    if year.startswith('year_')
                }

                if 'available_weekdays_bitmask' in raw_details:
                    kwargs['weekday_mask'] = raw_details['available_weekdays_bitmask']

                if 'valid_quantity_bitmask' in raw_details:
                    kwargs['valid_quanities'] = bitmask_to_numbered_list(
                        raw_details['valid_quantity_bitmask']
                    )

                details.append(AvailabilityDetails(**kwargs))

        return details

    def is_available(self, year, month=None, day=None):
        """
        Check if this combination of ticket_type and price band is available
        on a given year/month/day.
        """
        if day and not month:
            raise ValueError('a month must be specified to specify a day')

        if year not in self._calendar_masks:
            return False

        year_data = self._calendar_masks[year]

        if month and month not in year_data:
            return False

        month_mask = year_data.get(month)

        # the month mask is a 32 bit int where the right most bit is the first
        # day of the month. To find if we have availability on a specfic day,
        # we bit shift the mask by the zero indexed day and AND it by 1. If the
        # result is a 1 then this combo of ticket type and price band is
        # available on that day, otherwise it is not.
        if day and (month_mask >> (day - 1) & 1) == 0:
            return False

        return True

    def get_month_mask(self, year, month):
        """
        Retrieve the available days mask for a year and month. If a mask is not
        available then it will return 0
        """
        year_data = self._calendar_masks.get(year, {})
        return year_data.get(month, 0)

    def on_weekday(self, day):
        """
        Check if this combination of ticket_type and price band is available
        on a given day of the week, where 0 is monday and sunday is 6.

        NOTE: the api uses sunday as day 0 where as python uses monday. I've
        made a concious decision here to use the python numbers to keep it
        consistant with anything written against this. (also a sunday day 0 is
        silly)
        """

        adjusted_day = day + 1 if day < 6 else 0

        return bool(self.weekday_mask >> adjusted_day & 1)
