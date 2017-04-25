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
            }
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
