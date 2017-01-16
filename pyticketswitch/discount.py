class Discount(object):

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

    def is_available(self, no_of_tickets=None, seat_number=None):

        if no_of_tickets and no_of_tickets > self.available:
            return False

        if seat_number and bool(self.disallowed_mask >> seat_number & 1):
            return False

        return True

    def combined_price(self):
        return self.seatprice + self.surcharge

    def non_offer_combined_price(self):
        return self.non_offer_seatprice + self.non_offer_surcharge
