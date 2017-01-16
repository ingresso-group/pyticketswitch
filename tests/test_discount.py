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

    def test_init_with_no_non_offer_prices(self):
        discount = Discount('foo', seatprice=123.45, surcharge=6.78)
        assert discount.non_offer_seatprice == 123.45
        assert discount.non_offer_surcharge == 6.78

    def test_combined_price(self):

        discount = Discount('foo', seatprice=123.45, surcharge=6.78)

        assert discount.combined_price() == 130.23

    def test_non_offer_combined_price(self):

        discount = Discount('foo', non_offer_seatprice=123.45,
                            non_offer_surcharge=6.78)

        assert discount.non_offer_combined_price() == 130.23
