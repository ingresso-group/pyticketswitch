from pyticketswitch.price_band import PriceBand


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
            'example_seats': {
                'id_details': [
                    {'full_id': 'ZZ-TOP'},
                    {'full_id': 'ZZ-BOTTOM'},
                ]
            },
            'example_seats_are_real': False,
            'free_seat_blocks': {
                'seat_block': [
                    {'block_length': 10},
                    {'block_length': 20},
                ]
            }
        }

        price_band = PriceBand.from_api_data(data)

        assert price_band.code == 'B'
        assert price_band.description == 'Cheap Seats'
        assert price_band.default_discount.code == 'ABC123'

        assert len(price_band.example_seats) == 2
        assert price_band.example_seats[0].id == 'ZZ-TOP'
        assert price_band.example_seats[1].id == 'ZZ-BOTTOM'
        assert price_band.example_seats_are_real is False

        assert len(price_band.seat_blocks) == 2
        assert price_band.seat_blocks[0].length == 10
        assert price_band.seat_blocks[1].length == 20
