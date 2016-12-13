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


class CostRangeDetails(object):

    def __init__(self, ticket_type, price_band, cost_range,
                 ticket_type_description=None, price_band_description=None,
                 cost_range_no_singles=None, **kwargs):

        self.ticket_type = ticket_type
        self.price_band = price_band
        self.cost_range = cost_range
        self.cost_range_no_singles = cost_range_no_singles
        self.ticket_type_description = ticket_type_description
        self.price_band_description = price_band_description

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

                cost_range = price_band.get('cost_range')

                if not cost_range:
                    continue

                kwargs.update(
                    cost_range=CostRange.from_api_data(cost_range)
                )

                no_singles = cost_range.get('no_singles_cost_range')

                if no_singles:
                    kwargs.update(
                        cost_range_no_singles=CostRange.from_api_data(no_singles)
                    )

                details.append(cls(**kwargs))

        return details
