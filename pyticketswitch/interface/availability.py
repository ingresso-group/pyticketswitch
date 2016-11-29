import datetime
from pyticketswitch.utils import bitmask_to_numbered_list
from pyticketswitch.interface.currency import Currency


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
        self._weekday_mask = weekday_mask
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
                        month[:3]: mask
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
