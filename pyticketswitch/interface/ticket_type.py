from pyticketswitch.interface.price_band import PriceBand


class TicketType(object):

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