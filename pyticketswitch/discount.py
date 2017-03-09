from pyticketswitch.mixins import JSONMixin


class Discount(JSONMixin, object):
    """Represents a set of prices for a price band.

    Attributes:
        code (str): the identifier for the discount.
        description (str): a human readable description for the discount.
        price_band_code (str): identifier for the related price band.
        is_offer (bool): indicates that the discount is an offer.
        seatprice (float): the price per seat/ticket.
        surcharge (float): additional charges per seat/ticket.
        non_offer_seatprice (float): the original price per seat/ticket when
            not on offer.
        non_offer_surcharge (float): the original additional charges per
            seat/ticket when not on offer.
        availability (int): the number tickets available with this discount.
        percentage_saving (float): the amount saved compared to when this
            discount is not on offer, as a percentage or the non offer price.
        absolute_saving (float): the amount saved compared to when this
            discount is not on offer.

    """

    def __init__(self, code, description=None, price_band_code=None,
                 seatprice=None, surcharge=None, is_offer=False,
                 non_offer_seatprice=None, non_offer_surcharge=None,
                 availability=None, percentage_saving=0, absolute_saving=0):

        self.code = code
        self.description = description
        self.price_band_code = price_band_code
        self.is_offer = is_offer
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.non_offer_seatprice = non_offer_seatprice
        self.non_offer_surcharge = non_offer_surcharge
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

        return cls(**kwargs)

    def combined_price(self):
        """Returns the combined seatprice and surcharge.

        This method assumes that we have both a seatprice and surcharge.
        In the situation where are missing either a seatprice or a surcharge
        then we don't have all the information to be able provide this
        information.

        Returns:
            float: the discount seatprice and surcharge

        Raises:
            AssertionError: It might seem like the obvious thing to do would be
                to assume the missing data was in fact zero and simply allow the
                addition to continue. However that would be somewhat dangerous when
                we are talking about prices, and it's better to actually raise an
                exception to indicate that there was a problem with the objects
                data, than to inform a customer that the tickets are free or have
                no booking fees

        """
        assert self.seatprice is not None, 'seatprice data missing'
        assert self.surcharge is not None, 'surcharge data missing'
        return self.seatprice + self.surcharge

    def non_offer_combined_price(self):
        """Returns the combined non offer seatprice and surcharge.

        This method assumes that we have both a seatprice and surcharge.
        In the situation where are missing either a seatprice or a surcharge
        then we don't have all the information to be able provide this
        information.

        Returns:
            float: the discount seatprice and surcharge

        Raises:
            AssertionError: It might seem like the obvious thing to do would be
                to assume the missing data was in fact zero and simply allow the
                addition to continue. However that would be somewhat dangerous when
                we are talking about prices, and it's better to actually raise an
                exception to indicate that there was a problem with the objects
                data, than to inform a customer that the tickets are free or have
                no booking fees

        """
        assert self.non_offer_seatprice is not None, 'non_offer_seatprice data missing'
        assert self.non_offer_surcharge is not None, 'non_offer_surcharge data missing'
        return self.non_offer_seatprice + self.non_offer_surcharge

    def __repr__(self):
        return u'<Discount {}:{}>'.format(
            self.code, self.description.encode('ascii', 'ignore'))
