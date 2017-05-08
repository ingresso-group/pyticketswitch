from pyticketswitch.ticket_type import TicketType
from pyticketswitch.price_band import PriceBand
from pyticketswitch.discount import Discount
from pyticketswitch.seat import SeatBlock, Seat


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

    def test_get_seats(self):

        ticket_type = TicketType(
            'STALLS',
            price_bands=[
                PriceBand(
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
                ),
                PriceBand(
                    'B/pool',
                    Discount('ADULT'),
                    allows_leaving_single_seats='always',
                    seat_blocks=[
                        SeatBlock(
                            1,
                            seats=[
                                Seat(id_='C1'),
                            ]
                        ),
                        SeatBlock(
                            2,
                            seats=[
                                Seat(id_='D1'),
                                Seat(id_='D2'),
                            ]
                        ),
                    ]
                ),
            ]
        )

        seats = ticket_type.get_seats()

        assert seats[0].id == 'A1'
        assert seats[1].id == 'A2'
        assert seats[2].id == 'B1'
        assert seats[3].id == 'B2'
        assert seats[4].id == 'B3'
        assert seats[5].id == 'C1'
        assert seats[6].id == 'D1'
        assert seats[7].id == 'D2'

    def test_get_seats_with_no_price_bands(self):

        ticket_type = TicketType(
            'STALLS',
            price_bands=None
        )

        seats = ticket_type.get_seats()

        assert seats == []
