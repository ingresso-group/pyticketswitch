from pyticketswitch.offer import Offer
from pyticketswitch.mixins import JSONMixin


class CostRange(JSONMixin, object):
    """CostRange gives summarizes pricing for events and performances.

    This information is returned from cached data collected when making actual
    calls to the backend system, and should not be considered accurate.

    Attributes:
        valid_quantities (list): list of valid quanities available for
            purchase.
        min_seatprice (float): the minimum cost per seat the customer might be
            expected to pay.
        max_seatprice (float): the maximum cost per seat the customer might be
            expected to pay.
        min_surcharge (float): the minimum surcharge per seat the customer
            might be expected to pay.
        max_surcharge (float): the maximum surcharge per seat the customer
            might be expected to pay.
        currency (str): currency the cost range and offer prices are in.
        best_value_offer (:class:`Offer <pyticketswitch.offer.Offer>`): offer
            with the highest percentage saving.
        max_saving_offer (:class:`Offer <pyticketswitch.offer.Offer>`): offer
            with the highest absolute saving.
        max_cost_offer (:class:`Offer <pyticketswitch.offer.Offer>`): offer
            with the lowest cost.
        top_price_offer (:class:`Offer <pyticketswitch.offer.Offer>`): offer
            with the top price.

    """

    def __init__(self, valid_quantities=None, max_surcharge=None, max_seatprice=None,
                 min_surcharge=None, min_seatprice=None, allows_singles=True,
                 currency=None, best_value_offer=None, max_saving_offer=None,
                 min_cost_offer=None, top_price_offer=None):

        self.valid_quantities = valid_quantities
        self.max_seatprice = max_seatprice
        self.max_surcharge = max_surcharge
        self.min_seatprice = min_seatprice
        self.min_surcharge = min_surcharge
        self.currency = currency
        self.best_value_offer = best_value_offer
        self.max_saving_offer = max_saving_offer
        self.min_cost_offer = min_cost_offer
        self.top_price_offer = top_price_offer

    @classmethod
    def from_api_data(cls, data):

        api_best_value_offer = data.get('best_value_offer')
        best_value_offer = None

        if api_best_value_offer:
            best_value_offer = Offer.from_api_data(api_best_value_offer)

        api_max_saving_offer = data.get('max_saving_offer')
        max_saving_offer = None

        if api_max_saving_offer:
            max_saving_offer = Offer.from_api_data(api_max_saving_offer)

        api_min_cost_offer = data.get('min_cost_offer')
        min_cost_offer = None

        if api_min_cost_offer:
            min_cost_offer = Offer.from_api_data(api_min_cost_offer)

        api_top_price_offer = data.get('top_price_offer')
        top_price_offer = None

        if api_top_price_offer:
            top_price_offer = Offer.from_api_data(api_top_price_offer)

        min_seatprice = data.get('min_seatprice')
        min_surcharge = data.get('min_surcharge')
        max_seatprice = data.get('max_seatprice')
        max_surcharge = data.get('max_surcharge')

        # checking explictly for is not none, as zero is a legit value.
        if min_seatprice is not None:
            min_seatprice = float(min_seatprice)
        if max_seatprice is not None:
            max_seatprice = float(max_seatprice)
        if min_surcharge is not None:
            min_surcharge = float(min_surcharge)
        if max_surcharge is not None:
            max_surcharge = float(max_surcharge)

        kwargs = {
            'valid_quantities': data.get('valid_quantities'),
            'min_surcharge': min_surcharge,
            'min_seatprice': min_seatprice,
            'max_surcharge': max_surcharge,
            'max_seatprice': max_seatprice,
            'allows_singles': data.get('singles', True),
            'currency': data.get('range_currency_code'),
            'best_value_offer': best_value_offer,
            'max_saving_offer': max_saving_offer,
            'min_cost_offer': min_cost_offer,
            'top_price_offer': top_price_offer,
        }
        return cls(**kwargs)

    def has_offer(self):
        return any([
            self.best_value_offer,
            self.max_saving_offer,
            self.min_cost_offer,
            self.top_price_offer
        ])

    def get_min_combined_price(self):
        return self.min_surcharge + self.min_seatprice

    def get_max_combined_price(self):
        return self.max_surcharge + self.max_seatprice


class CostRangeDetails(JSONMixin, object):
    """Summarizes pricing by ticket types and price bands for an event/performance

    This information is returned from cached data collected when making actual
    calls to the backend system, and should not be considered accurate.

    Attributes:
        ticket_type_code (str): identifier for the ticket type.
        price_band_code (str): identifier for the price band.
        cost_range (:class:`CostRange <pyticketswitch.cost_range.CostRange>`):
            summary of pricing distribution for this ticket type/price band.
        cost_range_no_singles (:class:`CostRange <pyticketswitch.cost_range.CostRange>`):
            summary of pricing distribution for this ticket type/price band
            when not leaving any singles.
        ticket_type_description (str): description of the ticket type.
        price_band_description (str): description of the price band.

    """

    def __init__(self, ticket_type_code, price_band_code, cost_range,
                 ticket_type_description=None, price_band_description=None,
                 cost_range_no_singles=None, **kwargs):

        self.ticket_type_code = ticket_type_code
        self.price_band_code = price_band_code
        self.cost_range = cost_range
        self.cost_range_no_singles = cost_range_no_singles
        self.ticket_type_description = ticket_type_description
        self.price_band_description = price_band_description

    @classmethod
    def from_api_data(cls, data):
        details = []
        for ticket_type in data.get('ticket_type', []):
            kwargs = {
                'ticket_type_code': ticket_type.get('ticket_type_code'),
                'ticket_type_description': ticket_type.get('ticket_type_desc'),
            }
            for price_band in ticket_type.get('price_band', []):
                kwargs.update(
                    price_band_code=price_band.get('price_band_code'),
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
