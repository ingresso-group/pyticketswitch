from pyticketswitch.mixins import JSONMixin, SeatPricingMixin


class Discount(SeatPricingMixin, JSONMixin, object):
    """Represents a set of prices for a price band.

    Attributes:
        code (str): the identifier for the discount.
        description (str): a human readable description for the discount.
        price_band_code (str): identifier for the related price band.
        is_offer (bool): indicates that the discount is an offer.
        availability (int): the number tickets available with this discount.
        percentage_saving (float): the amount saved compared to when this
            discount is not on offer, as a percentage or the non offer price.
        absolute_saving (float): the amount saved compared to when this
            discount is not on offer.

    """

    def __init__(self, code, description=None, price_band_code=None,
                 availability=None, is_offer=False, percentage_saving=0,
                 absolute_saving=0, *args, **kwargs):
        super(Discount, self).__init__(*args, **kwargs)
        self.code = code
        self.description = description
        self.price_band_code = price_band_code
        self.is_offer = is_offer
        self.availability = availability
        self.percentage_saving = percentage_saving
        self.absolute_saving = absolute_saving

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Discount object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a discount.

        Returns:
            :class:`Discount <pyticketswitch.discount.Discount>`: a new
            :class:`Discount <pyticketswitch.discount.Discount>` object
            populated with the data from the api.

        """

        kwargs = {
            'code': data.get('discount_code'),
            'description': data.get('discount_desc'),
            'price_band_code': data.get('price_band_code'),
            'is_offer': data.get('is_offer', False),
            'seatprice': data.get('sale_seatprice'),
            'surcharge': data.get('sale_surcharge'),
            'non_offer_seatprice': data.get('non_offer_sale_seatprice'),
            'non_offer_surcharge': data.get('non_offer_sale_surcharge'),
            'availability': data.get('number_available'),
            'percentage_saving': data.get('percentage_saving'),
            'absolute_saving': data.get('absolute_saving'),
        }
        kwargs.update(SeatPricingMixin.kwargs_from_api_data(data))

        return cls(**kwargs)

    def __repr__(self):
        return u'<Discount {}:{}>'.format(
            self.code, self.description.encode('ascii', 'ignore'))
