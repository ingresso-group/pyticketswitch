from pyticketswitch.mixins import JSONMixin


class Discount(JSONMixin, object):

    def __init__(self, code, description=None, price_band=None, seatprice=None,
                 surcharge=None, is_offer=False, non_offer_seatprice=None,
                 non_offer_surcharge=None, availability=None,
                 percentage_saving=0, absolute_saving=0, disallowed_mask=0):

        self.code = code
        self.description = description
        self.price_band = price_band
        self.is_offer = is_offer
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.non_offer_seatprice = non_offer_seatprice
        self.non_offer_surcharge = non_offer_surcharge
        self.availability = availability
        self.percentage_saving = percentage_saving
        self.absolute_saving = absolute_saving
        self.disallowed_mask = disallowed_mask

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'code': data.get('discount_code'),
            'description': data.get('discount_desc'),
            'price_band': data.get('price_band_code'),
            'is_offer': data.get('is_offer', False),
            'seatprice': data.get('sale_seatprice'),
            'surcharge': data.get('sale_surcharge'),
            'non_offer_seatprice': data.get('non_offer_sale_seatprice'),
            'non_offer_surcharge': data.get('non_offer_sale_surcharge'),
            'availability': data.get('number_available'),
            'percentage_saving': data.get('percentage_saving'),
            'absolute_saving': data.get('absolute_saving'),
            'disallowed_mask': data.get('discount_disallowed_seat_no_bitmask'),
        }

        return cls(**kwargs)

    def combined_price(self):
        """
        This method assumes that we have both a seatprice and surcharge.
        in the situation where are missing either a seatprice or a surcharge
        then we don't have all the information to be able provide this
        information.

        It might seem like the obvious thing to do would be to assume the
        missing data was in fact zero and simply allow the addition to
        continue. However that would be somewhat dangerous when we are talking
        about prices, and it's better to actually raise an exception to
        indicate that there was a problem with the objects data, than to inform
        a customer that the tickets are free or have no booking fees
        """
        assert self.seatprice is not None, 'seatprice data missing'
        assert self.surcharge is not None, 'surcharge data missing'
        return self.seatprice + self.surcharge

    def non_offer_combined_price(self):
        """
        See combined_price()
        """
        assert self.non_offer_seatprice is not None, 'non_offer_seatprice data missing'
        assert self.non_offer_surcharge is not None, 'non_offer_surcharge data missing'
        return self.non_offer_seatprice + self.non_offer_surcharge

    def __repr__(self):
        return u'<Discount {}:{}>'.format(self.code, self.description)
