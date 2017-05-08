from pyticketswitch.mixins import JSONMixin


class Offer(JSONMixin, object):
    """Describes a reduction in price.

    Attributes:
        seatprice (float): the price per seat/ticket.
        surcharge (float): the additional charges per seat/ticket.
        original_seatprice (float): the original price per seat/ticket.
        original_surcharge (float): the original additional charges per
            seat/ticket.
        absolute_saving (float): the amount of money saved by this offer.
        percentage_saving (float): the amount of money saved by this offer, as
            a percentage of the original price.

    """
    def __init__(self, seatprice=None, surcharge=None, original_seatprice=None,
                 original_surcharge=None, absolute_saving=None,
                 percentage_saving=None):

        self.seatprice = seatprice
        self.surcharge = surcharge
        self.original_surcharge = original_surcharge
        self.original_seatprice = original_seatprice
        self.absolute_saving = absolute_saving
        self.percentage_saving = percentage_saving

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Offer object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns an offer.

        Returns:
            :class:`Offer <pyticketswitch.offer.Offer>`: a new
            :class:`Offer <pyticketswitch.offer.Offer>` object
            populated with the data from the api.

        """
        kwargs = {
            'seatprice': data.get('offer_seatprice'),
            'surcharge': data.get('offer_surcharge'),
            'original_seatprice': data.get('full_seatprice'),
            'original_surcharge': data.get('full_surcharge'),
            'absolute_saving': data.get('absolute_saving'),
            'percentage_saving': data.get('percentage_saving'),
        }
        return cls(**kwargs)
