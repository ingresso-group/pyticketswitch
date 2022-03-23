from pyticketswitch.price_band import PriceBand
from pyticketswitch.discount import Discount
from pyticketswitch.seat import SeatBlock, Seat


class TestPriceBand:

    def test_from_api_data(self):

        data = {
            'price_band_desc': 'Cheap Seats',
            'cost_range': {
                'quantity_options': {
                    'valid_quantity_mask': 2046
                },
                'max_surcharge': 11.65,
                'max_seatprice': 59.5,
                'range_currency': {
                    'currency_factor': 100,
                    'currency_places': 2,
                    'currency_post_symbol': '',
                    'currency_number': 826,
                    'currency_pre_symbol': '\xa3',
                    'currency_code': 'gbp'
                },
                'min_surcharge': 11.25,
                'no_singles_cost_range': {
                    'quantity_options': {
                        'valid_quantity_mask': 2046
                    },
                    'max_surcharge': 11.65,
                    'max_seatprice': 59.5,
                    'range_currency': {
                        'currency_factor': 100,
                        'currency_places': 2,
                        'currency_post_symbol': '',
                        'currency_number': 826,
                        'currency_pre_symbol': '\xa3',
                        'currency_code': 'gbp'
                    },
                    'min_surcharge': 11.25,
                    'min_seatprice': 57.5
                },
                'min_seatprice': 57.5
            },
            'price_band_code': 'B',
            'discount_code': 'ABC123',
            'allows_leaving_single_seats': 'always',
            'example_seats': [
                {'full_id': 'ZZ-TOP'},
                {'full_id': 'ZZ-BOTTOM'},
            ],
            'example_seats_are_real': False,
            'free_seat_blocks': {
                'blocks_by_row': {
                    'A': [['A1', 'A2'], ['A4', 'A5']],
                    'B': [['B-1', 'B-2'], ['B-4', 'B-5']],
                },
                'separators_by_row': {
                    'A': '',
                    'B': '-',
                },
                'seats_by_text_message': {
                    'Death Trap': ['A1', 'B-2'],
                },
                'restricted_view_seats': ['A1', 'B-2'],
            },
            "predicted_user_commission": {
                "amount_excluding_vat": 2.93,
            },
            "possible_discounts": {
                "discount": [
                    {
                        "discount_code": "ADULT",
                    },
                    {
                        "discount_code": "CHILD",
                    },
                ]
            },
            "number_available": 40,
            'sale_seatprice': 160,
            'sale_surcharge': 5.5,
            'non_offer_sale_seatprice': 200,
            'non_offer_sale_surcharge': 6.5,
            "percentage_saving": 20,
            "is_offer": True,
            'sale_combined_tax_component': 50
        }

        price_band = PriceBand.from_api_data(data)

        assert price_band.code == 'B'
        assert price_band.description == 'Cheap Seats'
        assert price_band.default_discount.code == 'ABC123'
        assert price_band.allows_leaving_single_seats == 'always'

        assert len(price_band.example_seats) == 2
        assert price_band.example_seats[0].id == 'ZZ-TOP'
        assert price_band.example_seats[1].id == 'ZZ-BOTTOM'
        assert price_band.example_seats_are_real is False

        assert len(price_band.seat_blocks) == 4
        assert price_band.seat_blocks[0].length == 2

        assert price_band.user_commission.excluding_vat == 2.93

        assert len(price_band.discounts) == 2
        assert price_band.discounts[0].code == 'ADULT'
        assert price_band.discounts[1].code == 'CHILD'

        assert price_band.availability == 40

        assert price_band.seatprice == 160.00
        assert price_band.surcharge == 5.5
        assert price_band.non_offer_seatprice == 200
        assert price_band.non_offer_surcharge == 6.5
        assert price_band.percentage_saving == 20
        assert price_band.is_offer is True
        assert price_band.tax_component == 50

    def test_get_seats(self):

        price_band = PriceBand(
            'A/pool',
            Discount('ADULT'),
            allows_leaving_single_seats='always',
            seat_blocks=[
                SeatBlock(
                    2,
                    seats=[
                        Seat(id_='A1'),
                        Seat(id_='A2'),
                    ]
                ),
                SeatBlock(
                    3,
                    seats=[
                        Seat(id_='B1'),
                        Seat(id_='B2'),
                        Seat(id_='B3'),
                    ]
                ),
            ]
        )

        seats = price_band.get_seats()

        assert seats[0].id == 'A1'
        assert seats[1].id == 'A2'
        assert seats[2].id == 'B1'
        assert seats[3].id == 'B2'
        assert seats[4].id == 'B3'

    def test_get_seats_with_seatblocks_without_seats(self):

        price_band = PriceBand(
            'A/pool',
            Discount('ADULT'),
            allows_leaving_single_seats='always',
            seat_blocks=[
                SeatBlock(
                    2,
                    seats=None
                ),
                SeatBlock(
                    3,
                    seats=[
                        Seat(id_='B1'),
                        Seat(id_='B2'),
                        Seat(id_='B3'),
                    ]
                ),
            ]
        )

        seats = price_band.get_seats()

        assert seats[0].id == 'B1'
        assert seats[1].id == 'B2'
        assert seats[2].id == 'B3'

    def test_get_seats_without_seatblocks(self):

        price_band = PriceBand(
            'A/pool',
            Discount('ADULT'),
            seat_blocks=None,
            allows_leaving_single_seats='always',
        )

        seats = price_band.get_seats()

        assert seats == []
