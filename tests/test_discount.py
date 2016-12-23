from pyticketswitch.discount import Discount


class TestDiscount:

    def test_from_api_data(self):
        data = {
            'discount_code': 'ADULT',
            'discount_desc': 'Adult standard',
            'price_band_code': 'A/pool',
            'sale_seatprice': 160,
            'sale_surcharge': 5.5,
            'is_offer': True,
            'non_offer_sale_seatprice': 200,
            'non_offer_sale_surcharge': 5.5,
            'absolute_saving': 40,
            'percentage_saving': 20,
            'number_available': 6,
            'discount_disallowed_seat_no_bitmask': 126,
        }

        discount = Discount.from_api_data(data)

        assert discount.code == 'ADULT'
        assert discount.description == 'Adult standard'
        assert discount.price_band == 'A/pool'
        assert discount.seatprice == 160.0
        assert discount.surcharge == 5.5
        assert discount.is_offer is True
        assert discount.non_offer_seatprice == 200
        assert discount.non_offer_surcharge == 5.5
        assert discount.availability == 6
        assert discount.disallowed_mask == 126
