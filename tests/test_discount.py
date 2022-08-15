from pyticketswitch.discount import Discount
from pyticketswitch.commission import Commission


class TestDiscount:

    def test_from_api_data(self):
        gross_commission_data = {
            'amount_including_vat': 2.8,
            'amount_excluding_vat': 3.0,
            'commission_currency_code': 'gbp',
        }
        user_commission_data = {
            'amount_including_vat': 0.8,
            'amount_excluding_vat': 1.0,
            'commission_currency_code': 'gbp',
        }

        data = {
            'discount_code': 'ADULT',
            'discount_desc': 'Adult standard',
            'discount_disallowed_seat_nos': [0, 2, 3, 4],
            'price_band_code': 'A/pool',
            'sale_seatprice': 160,
            'sale_surcharge': 5.5,
            'is_offer': True,
            'non_offer_sale_seatprice': 200,
            'non_offer_sale_surcharge': 6.5,
            'absolute_saving': 40,
            'percentage_saving': 20,
            'number_available': 6,
            'predicted_gross_commission': gross_commission_data,
            'predicted_user_commission': user_commission_data,
            'sale_combined_tax_component': 50,
            'discount_semantic_type': 'senior',
            'discount_minimum_eligible_age': 60,
            'discount_maximum_eligible_age': 80,
        }

        discount = Discount.from_api_data(data)

        assert discount.code == 'ADULT'
        assert discount.description == 'Adult standard'
        assert discount.disallowed_seat_nos == [0, 2, 3, 4]
        assert discount.price_band_code == 'A/pool'
        assert discount.seatprice == 160.0
        assert discount.surcharge == 5.5
        assert discount.is_offer is True
        assert discount.non_offer_seatprice == 200
        assert discount.non_offer_surcharge == 6.5
        assert discount.availability == 6
        assert isinstance(discount.gross_commission, Commission)
        assert discount.gross_commission.including_vat == gross_commission_data['amount_including_vat']
        assert discount.gross_commission.excluding_vat == gross_commission_data['amount_excluding_vat']
        assert discount.gross_commission.currency_code == gross_commission_data['commission_currency_code']
        assert isinstance(discount.user_commission, Commission)
        assert discount.user_commission.including_vat == user_commission_data['amount_including_vat']
        assert discount.user_commission.excluding_vat == user_commission_data['amount_excluding_vat']
        assert discount.user_commission.currency_code == user_commission_data['commission_currency_code']
        assert discount.tax_component == 50
        assert discount.semantic_type == 'senior'

    def test_from_api_data_without_commission(self):
        data = {
            'discount_code': 'ADULT',
            'discount_desc': 'Adult standard',
            'price_band_code': 'A/pool',
            'sale_seatprice': 160,
            'sale_surcharge': 5.5,
            'is_offer': True,
            'non_offer_sale_seatprice': 200,
            'non_offer_sale_surcharge': 6.5,
            'absolute_saving': 40,
            'percentage_saving': 20,
            'number_available': 6,
        }

        discount = Discount.from_api_data(data)

        assert discount.code == 'ADULT'
        assert discount.description == 'Adult standard'
        assert discount.price_band_code == 'A/pool'
        assert discount.seatprice == 160.0
        assert discount.surcharge == 5.5
        assert discount.is_offer is True
        assert discount.non_offer_seatprice == 200
        assert discount.non_offer_surcharge == 6.5
        assert discount.availability == 6
        assert discount.gross_commission is None
        assert discount.user_commission is None
