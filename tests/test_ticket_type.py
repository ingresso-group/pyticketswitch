from pyticketswitch.ticket_type import TicketType


class TestTicketType:

    def test_from_api_data(self):

        data = {
            'ticket_type_desc': 'Grand Circle',
            'price_band': [
                {
                    'price_band_desc': '',
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
                    'price_band_code': 'B'
                },
            ],
            'ticket_type_code': 'GRA'
        }
        ticket_type = TicketType.from_api_data(data)
        assert ticket_type.code == 'GRA'
        assert ticket_type.description == 'Grand Circle'
        assert len(ticket_type.price_bands) == 1
