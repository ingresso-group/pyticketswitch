class Discount(object):

    def __init__(self, code, description=None, seatprice=None, surcharge=None,
                 is_offer=False, non_offer_seatprice=None,
                 non_offer_surcharge=None, available=None,
                 percentage_saving=0, absolute_saving=0,
                 disallowed_mask=0):

        self.code = code
        self.description = description
        self.is_offer = is_offer
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.non_offer_seatprice = non_offer_seatprice
        self.non_offer_surcharge = non_offer_surcharge
        self.available = available
        self.percentage_saving = percentage_saving
        self.absolute_saving = absolute_saving
        self.disallowed_mask = disallowed_mask

    def is_available(self, no_of_tickets=None, seat_number=None):

        if no_of_tickets and no_of_tickets > self.available:
            return False

        if seat_number and bool(self.disallowed_mask >> seat_number & 1):
            return False

        return True
