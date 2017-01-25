from pyticketswitch.price_band import PriceBand
from pyticketswitch.mixins import JSONMixin


class TicketType(JSONMixin, object):

    def __init__(self, code=None, description=None, price_bands=None):

        self.code = code
        self.description = description
        self.price_bands = price_bands

    @classmethod
    def from_api_data(cls, data):

        price_bands = []
        api_price_bands = data.get('price_band', [])
        for single_band in api_price_bands:
            price_bands.append(PriceBand.from_api_data(single_band))

        kwargs = {
            'code': data.get('ticket_type_code', None),
            'description': data.get('ticket_type_desc', None),
            'price_bands': price_bands,
        }

        return cls(**kwargs)

    def get_seats(self):

        if not self.price_bands:
            return []

        return [
            seat
            for price_band in self.price_bands
            for seat in price_band.get_seats()
        ]
