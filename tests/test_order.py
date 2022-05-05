from decimal import Decimal
from pyticketswitch.event import Event
from pyticketswitch.performance import Performance
from pyticketswitch.order import TicketOrder, Order
from pyticketswitch.seat import Seat
from pyticketswitch.commission import Commission


class TestTicketOrder:

    def test_from_api_data(self):
        data = {
            'discount_code': 'ADULT',
            'discount_desc': 'Adult standard',
            'no_of_seats': 2,
            'sale_seatprice': 25,
            'sale_surcharge': 2.50,
            'total_sale_seatprice': 50,
            'total_sale_surcharge': 5,
            'seats': [
                {'full_id': 'ABC123'},
                {'full_id': 'DEF456'},
            ],
            "total_sale_combined": 55.0,
            'sale_combined_tax_component': 35.0,
            'sale_surcharge_tax_sub_component': 0.0,
            'total_sale_combined_tax_component': 35.0,
            'total_sale_surcharge_tax_sub_component': 0.0,
        }

        ticket_order = TicketOrder.from_api_data(data)

        assert ticket_order.code == 'ADULT'
        assert ticket_order.number_of_seats == 2
        assert ticket_order.description == 'Adult standard'
        assert isinstance(ticket_order.seatprice, (int, float))
        assert ticket_order.seatprice == 25.0
        assert isinstance(ticket_order.surcharge, (int, float))
        assert ticket_order.surcharge == 2.5
        assert isinstance(ticket_order.total_seatprice, (int, float))
        assert ticket_order.total_seatprice == 50.0
        assert isinstance(ticket_order.total_surcharge, (int, float))
        assert ticket_order.total_surcharge == 5.0
        assert len(ticket_order.seats) == 2
        assert ticket_order.seats[0].id == 'ABC123'
        assert ticket_order.seats[1].id == 'DEF456'

        assert isinstance(ticket_order.raw_combined_tax_component, (int, float))
        assert ticket_order.raw_combined_tax_component == 35.0
        assert isinstance(ticket_order.raw_surcharge_tax_sub_component, (int, float))
        assert ticket_order.raw_surcharge_tax_sub_component == 0.0
        assert isinstance(ticket_order.raw_total_combined_tax_component, (int, float))
        assert ticket_order.raw_total_combined_tax_component == 35.0
        assert isinstance(ticket_order.raw_total_surcharge_tax_sub_component, (int, float))
        assert ticket_order.raw_total_surcharge_tax_sub_component == 0.0
        assert isinstance(ticket_order.total_sale_combined, (int, float))
        assert ticket_order.total_sale_combined == 55.0

    def test_from_api_data_with_decimal(self):
        data = {
            'discount_code': 'ADULT',
            'discount_desc': 'Adult standard',
            'no_of_seats': 2,
            'sale_seatprice': 25,
            'sale_surcharge': Decimal('2.50'),
            'total_sale_seatprice': 50,
            'total_sale_surcharge': Decimal('5.00'),
            'seats': [
                {'full_id': 'ABC123'},
                {'full_id': 'DEF456'},
            ],
            'total_sale_combined': Decimal('55.0'),
            'sale_combined_tax_component': Decimal('35.0'),
            'sale_surcharge_tax_sub_component': Decimal('0.0'),
            'total_sale_combined_tax_component': Decimal('35.0'),
            'total_sale_surcharge_tax_sub_component': Decimal('0.0'),
        }

        ticket_order = TicketOrder.from_api_data(data)

        assert ticket_order.code == 'ADULT'
        assert ticket_order.number_of_seats == 2
        assert ticket_order.description == 'Adult standard'
        assert isinstance(ticket_order.seatprice, (int, Decimal))
        assert ticket_order.seatprice == Decimal('25.0')
        assert isinstance(ticket_order.surcharge, (int, Decimal))
        assert ticket_order.surcharge == Decimal('2.5')
        assert isinstance(ticket_order.total_seatprice, (int, Decimal))
        assert ticket_order.total_seatprice == Decimal('50.0')
        assert isinstance(ticket_order.total_surcharge, (int, Decimal))
        assert ticket_order.total_surcharge == Decimal('5.0')
        assert len(ticket_order.seats) == 2
        assert ticket_order.seats[0].id == 'ABC123'
        assert ticket_order.seats[1].id == 'DEF456'

        assert isinstance(ticket_order.raw_combined_tax_component, (int, Decimal))
        assert ticket_order.raw_combined_tax_component == Decimal('35.0')
        assert isinstance(ticket_order.raw_surcharge_tax_sub_component, (int, Decimal))
        assert ticket_order.raw_surcharge_tax_sub_component == Decimal('0.0')
        assert isinstance(ticket_order.raw_total_combined_tax_component, (int, Decimal))
        assert ticket_order.raw_total_combined_tax_component == Decimal('35.0')
        assert isinstance(ticket_order.raw_total_surcharge_tax_sub_component, (int, Decimal))
        assert ticket_order.raw_total_surcharge_tax_sub_component == Decimal('0.0')
        assert isinstance(ticket_order.total_sale_combined, (int, Decimal))
        assert ticket_order.total_sale_combined == Decimal('55.0')

    def test_repr(self):
        ticket_order = TicketOrder('abc123')
        assert repr(ticket_order) == '<TicketOrder abc123>'

    def test_combined_price(self):
        data = {
            'discount_code': 'ADULT',
            'discount_desc': 'Adult standard',
            'no_of_seats': 2,
            'sale_seatprice': 25,
            'sale_surcharge': 2.50,
            'total_sale_seatprice': 50,
            'total_sale_surcharge': 5,
            'seats': [
                {'full_id': 'ABC123'},
                {'full_id': 'DEF456'},
            ]
        }
        ticket_order = TicketOrder.from_api_data(data)
        assert ticket_order.combined_price() == 27.50

    def test_total_combined_price(self):
        data = {
            'discount_code': 'ADULT',
            'discount_desc': 'Adult standard',
            'no_of_seats': 2,
            'sale_seatprice': 25,
            'sale_surcharge': 2.50,
            'total_sale_seatprice': 50,
            'total_sale_surcharge': 5,
            'seats': [
                {'full_id': 'ABC123'},
                {'full_id': 'DEF456'},
            ]
        }
        ticket_order = TicketOrder.from_api_data(data)
        assert ticket_order.total_combined_price() == 55.0


class TestOrder:

    def test_from_api_data(self):

        data = {
            "backend_purchase_reference": 'GHI098',
            "backend_cancellation_reference": 'GHI098-cancelled',
            "external_management_url": 'www.example.com/some-more-decisions',
            "cancellation_status": "possible",
            "cancellation_comment": "",
            "event": {
                "event_id": "6IF",
            },
            "item_number": 1,
            "performance": {
                "perf_id": "6IF-A7N",
            },
            "price_band_code": "C/pool",
            "price_band_desc": "Band C",
            "seat_request_status": "got_all",
            "ticket_orders": {
                "ticket_order": [
                    {"discount_code": "ADULT"},
                    {"discount_code": "CHILD"},
                ]
            },
            "ticket_type_code": "CIRCLE",
            "ticket_type_desc": "Upper circle",
            "total_no_of_seats": 3,
            "total_sale_seatprice": 51,
            "total_sale_surcharge": 5.40,
            "requested_seat_ids": [
                'ABC123',
                'DEF456',
            ],
            'send_method': {
                'send_code': 'POST',
                'send_cost': 3.5,
                'send_desc': 'Post (UK & Ireland only)',
                'send_type': 'post',
                'permitted_countries': {
                    'country': [
                        {
                            'country_code': 'ie',
                            'country_desc': 'Ireland'
                        },
                        {
                            'country_code': 'uk',
                            'country_desc': 'United Kingdom'
                        }
                    ]
                }
            },
            'predicted_gross_commission': {
                'amount_including_vat': 4.0,
                'amount_excluding_vat': 4.5,
                'commission_currency_code': 'gbp',
            },
            'predicted_user_commission': {
                'amount_including_vat': 2.0,
                'amount_excluding_vat': 2.1,
                'commission_currency_code': 'gbp',
            },
            "total_sale_combined_tax_component": 35.0,
            "total_sale_surcharge_tax_sub_component": 0.0,
            "total_sale_combined": 56.40
        }

        order = Order.from_api_data(data)

        assert order.item == 1
        assert order.price_band_code == 'C/pool'
        assert order.price_band_description == 'Band C'
        assert order.ticket_type_code == 'CIRCLE'
        assert order.ticket_type_description == 'Upper circle'
        assert order.number_of_seats == 3
        assert order.total_seatprice == 51
        assert order.total_surcharge == 5.40
        assert order.seat_request_status == "got_all"
        assert order.backend_purchase_reference == 'GHI098'
        assert order.backend_cancellation_reference == 'GHI098-cancelled'
        assert order.cancellation_status == "possible"
        assert order.cancellation_comment == ""
        assert order.external_management_url == 'www.example.com/some-more-decisions'

        assert isinstance(order.event, Event)
        assert order.event.id == '6IF'
        assert isinstance(order.performance, Performance)
        assert order.performance.id == '6IF-A7N'

        assert len(order.ticket_orders) == 2
        assert order.ticket_orders[0].code == 'ADULT'
        assert order.ticket_orders[1].code == 'CHILD'

        assert len(order.requested_seat_ids) == 2
        assert order.requested_seat_ids[0] == 'ABC123'
        assert order.requested_seat_ids[1] == 'DEF456'

        assert order.total_including_send_cost() == (51 + 5.40 + 3.5)

        assert isinstance(order.gross_commission, Commission)
        assert order.gross_commission.including_vat == 4.0
        assert order.gross_commission.excluding_vat == 4.5
        assert order.gross_commission.currency_code == 'gbp'
        assert isinstance(order.user_commission, Commission)
        assert order.user_commission.including_vat == 2.0
        assert order.user_commission.excluding_vat == 2.1
        assert order.user_commission.currency_code == 'gbp'

        assert order.total_sale_combined_tax_component == 35.0
        assert order.total_sale_surcharge_tax_sub_component == 0.0
        assert order.total_sale_combined == 56.40

    def test_from_api_data_with_decimal(self):

        data = {
            "backend_purchase_reference": 'GHI098',
            "event": {
                "event_id": "6IF",
            },
            "item_number": 1,
            "performance": {
                "perf_id": "6IF-A7N",
            },
            "price_band_code": "C/pool",
            "price_band_desc": "Band C",
            "seat_request_status": "got_all",
            "ticket_orders": {
                "ticket_order": [
                    {"discount_code": "ADULT"},
                    {"discount_code": "CHILD"},
                ]
            },
            "ticket_type_code": "CIRCLE",
            "ticket_type_desc": "Upper circle",
            "total_no_of_seats": 3,
            "total_sale_seatprice": 51,
            "total_sale_surcharge": Decimal('5.40'),
            "requested_seat_ids": [
                'ABC123',
                'DEF456',
            ],
            'send_method': {
                'send_code': 'POST',
                'send_cost': Decimal('3.5'),
                'send_desc': 'Post (UK & Ireland only)',
                'send_type': 'post',
                'permitted_countries': {
                    'country': [
                        {
                            'country_code': 'ie',
                            'country_desc': 'Ireland'
                        },
                        {
                            'country_code': 'uk',
                            'country_desc': 'United Kingdom'
                        }
                    ]
                }
            },
            'predicted_gross_commission': {
                'amount_including_vat': Decimal('4.0'),
                'amount_excluding_vat': Decimal('4.5'),
                'commission_currency_code': 'gbp',
            },
            'predicted_user_commission': {
                'amount_including_vat': Decimal('2.0'),
                'amount_excluding_vat': Decimal('2.1'),
                'commission_currency_code': 'gbp',
            },
            "total_sale_combined_tax_component": Decimal('35.0'),
            "total_sale_surcharge_tax_sub_component": Decimal('0.0'),
            "total_sale_combined": Decimal("56.40")
        }

        order = Order.from_api_data(data)

        assert order.item == 1
        assert order.price_band_code == 'C/pool'
        assert order.price_band_description == 'Band C'
        assert order.ticket_type_code == 'CIRCLE'
        assert order.ticket_type_description == 'Upper circle'
        assert order.number_of_seats == 3
        assert order.total_seatprice == 51
        assert order.total_surcharge == Decimal('5.40')

        assert len(order.ticket_orders) == 2

        assert len(order.requested_seat_ids) == 2

        assert order.total_including_send_cost() == (51 + Decimal('5.40') + Decimal('3.5'))

        assert isinstance(order.gross_commission, Commission)
        assert order.gross_commission.including_vat == Decimal('4.0')
        assert order.gross_commission.excluding_vat == Decimal('4.5')
        assert order.gross_commission.currency_code == 'gbp'
        assert isinstance(order.user_commission, Commission)
        assert order.user_commission.including_vat == Decimal('2.0')
        assert order.user_commission.excluding_vat == Decimal('2.1')
        assert order.user_commission.currency_code == 'gbp'

        assert order.total_sale_combined_tax_component == Decimal('35.0')
        assert order.total_sale_surcharge_tax_sub_component == Decimal('0.0')
        assert order.total_sale_combined == Decimal('56.40')

    def test_from_api_data_with_send_method(self):

        data = {
            'item_number': 1,
            "send_method": {
                "send_code": "COBO",
            },
        }

        order = Order.from_api_data(data)

        assert order.send_method.code == 'COBO'

    def test_get_seats(self):
        ticket_order_one = TicketOrder('a', seats=[
            Seat('A1'), Seat('A2'), Seat('A3'),
        ])

        ticket_order_two = TicketOrder('b', seats=[
            Seat('B1'), Seat('B2'), Seat('B3'),
        ])

        order = Order(1, ticket_orders=[ticket_order_one, ticket_order_two])

        seats = order.get_seats()
        assert [seat.id for seat in seats] == [
            'A1', 'A2', 'A3', 'B1', 'B2', 'B3',
        ]

    def test_get_seat_ids(self):
        ticket_order_one = TicketOrder('a', seats=[
            Seat('A1'), Seat('A2'), Seat('A3'),
        ])

        ticket_order_two = TicketOrder('b', seats=[
            Seat('B1'), Seat('B2'), Seat('B3'),
        ])

        order = Order(1, ticket_orders=[ticket_order_one, ticket_order_two])

        seat_ids = order.get_seat_ids()
        assert seat_ids == ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

    def test_get_seat_ids_where_ids_are_missing(self):
        ticket_order_one = TicketOrder('a', seats=[
            Seat('A1'), Seat('A2'), Seat(None),
        ])

        ticket_order_two = TicketOrder('b', seats=[
            Seat('B1'), Seat(None), Seat('B3'),
        ])

        order = Order(1, ticket_orders=[ticket_order_one, ticket_order_two])

        seat_ids = order.get_seat_ids()
        assert seat_ids == ['A1', 'A2', 'B1', 'B3']

    def test_unique_seat_text(self):
        ticket_order_one = TicketOrder('a', seats=[
            Seat('A1', seat_text='Hell bad'), Seat('A2'), Seat('A3'),
        ])

        ticket_order_two = TicketOrder('b', seats=[
            Seat('B1', seat_text='Hell good'), Seat('B2'), Seat('B3'),
        ])

        order = Order(1, ticket_orders=[ticket_order_one, ticket_order_two])

        seat_text = order.unique_seat_text()
        assert 'Hell bad' in seat_text
        assert 'Hell good' in seat_text

    def test_get_seats_with_no_ticket_orders(self):
        order = Order(1, ticket_orders=[])
        assert order.get_seats() == []

    def test_repr(self):
        order = Order(1, ticket_orders=[])
        assert repr(order) == '<Order 1>'

    def test_from_api_data_without_commission(self):
        data = {
            'item_number': 1,
            "send_method": {
                "send_code": "COBO",
            },
        }

        order = Order.from_api_data(data)

        assert order.gross_commission is None
        assert order.user_commission is None

    def test_from_api_data_with_actual_commission(self):
        data = {
            "gross_commission": {
                "amount_excluding_vat": 18.75,
                "amount_including_vat": 22.5,
                "commission_currency_code": "gbp"
            },
            "item_number": 1,
            "user_commission": {
                "amount_excluding_vat": 12.5,
                "amount_including_vat": 15,
                "commission_currency_code": "gbp"
            }
        }
        order = Order.from_api_data(data)

        assert type(order.user_commission) is Commission
        assert order.user_commission.including_vat == 15
        assert order.user_commission.excluding_vat == 12.5
        assert order.user_commission.currency_code == "gbp"

        assert type(order.gross_commission) is Commission
        assert order.gross_commission.including_vat == 22.5
        assert order.gross_commission.excluding_vat == 18.75
        assert order.gross_commission.currency_code == "gbp"

