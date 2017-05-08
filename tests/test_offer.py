from pyticketswitch.offer import Offer


class TestOffer:

    def test_from_api_data(self):
        data = {
            "absolute_saving": 9,
            "percentage_saving": 11,
            "full_seatprice": 75,
            "full_surcharge": 5,
            "offer_seatprice": 68,
            "offer_surcharge": 3,
        }
        offer = Offer.from_api_data(data)

        assert offer.absolute_saving == 9
        assert offer.percentage_saving == 11
        assert offer.original_seatprice == 75
        assert offer.original_surcharge == 5
        assert offer.seatprice == 68
        assert offer.surcharge == 3
