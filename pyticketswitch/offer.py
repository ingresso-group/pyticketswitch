class Offer(object):

    def __init__(self, absolute_saving=0, percentage_saving=0,
                 original_seatprice=0, original_surcharge=0,
                 seatprice=0, surcharge=0):

        self.absolute_saving = absolute_saving
        self.percentage_saving = percentage_saving
        self.original_surcharge = original_surcharge
        self.original_seatprice = original_seatprice
        self.seatprice = seatprice
        self.surcharge = surcharge

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'absolute_saving': data.get('absolute_saving', 0),
            'percentage_saving': data.get('percentage_saving', 0),
            'original_seatprice': data.get('original_seatprice', 0),
            'original_surcharge': data.get('original_surcharge', 0),
            'seatprice': data.get('seatprice', 0),
            'surcharge': data.get('surcharge', 0),
        }
        return cls(**kwargs)
