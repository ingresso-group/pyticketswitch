from pyticketswitch.price_band import PriceBand
from pyticketswitch.mixins import JSONMixin


class TicketType(JSONMixin, object):
    """Describes a collection of tickets.

    Generally this represents a part of house in a venue, but may have other
    meanings in contexts outside theater and music.

    Attributes:
        code (str): identifier for the ticket type.
        description (str): human readable description of the ticket type.
        price_bands (list): list of
            :class:`PriceBands <pyticketswitch.price_band.PriceBand>` objects
            wich further subdivided available tickets/seats by price.

    """
    def __init__(self, code=None, description=None, price_bands=None):

        self.code = code
        self.description = description
        self.price_bands = price_bands

    @classmethod
    def from_api_data(cls, data):
        """Creates a new PriceBand object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a price band.

        Returns:
            :class:`PriceBand <pyticketswitch.price_band.PriceBand>`: a new
            :class:`PriceBand <pyticketswitch.price_band.PriceBand>` object
            populated with the data from the api.

        """
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
        """Get seats in the ticket type.

        Returns:
            list: list of :class:`Seats <pyticketswitch.seat.Seat>` objects.

        """
        if not self.price_bands:
            return []

        return [
            seat
            for price_band in self.price_bands
            for seat in price_band.get_seats()
        ]

    def __repr__(self):
        return u'<TicketType {}: {}>'.format(
            self.code, self.description.encode('ascii', 'ignore'))
