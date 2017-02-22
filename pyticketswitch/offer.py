from pyticketswitch.mixins import JSONMixin


class Offer(JSONMixin, object):

    def __init__(self, absolute_saving=None, percentage_saving=None,
                 original_seatprice=None, original_surcharge=None,
                 seatprice=None, surcharge=None):

        self.absolute_saving = absolute_saving
        self.percentage_saving = percentage_saving
        self.original_surcharge = original_surcharge
        self.original_seatprice = original_seatprice
        self.seatprice = seatprice
        self.surcharge = surcharge

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'absolute_saving': data.get('absolute_saving'),
            'percentage_saving': data.get('percentage_saving'),
            'original_seatprice': data.get('full_seatprice'),
            'original_surcharge': data.get('full_surcharge'),
            'seatprice': data.get('offer_seatprice'),
            'surcharge': data.get('offer_surcharge'),
        }
        return cls(**kwargs)
