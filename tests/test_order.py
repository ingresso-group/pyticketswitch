from pyticketswitch.event import Event
from pyticketswitch.performance import Performance
from pyticketswitch.order import TicketOrder, Order


class TestTicketOrder:

    def test_from_api_data(self):
        data = {
            'discount_code': 'ADULT',
            'discount_desc': 'Adult standard',
            'discount_disallowed_seat_no_bitmask': 123,
            'no_of_seats': 2,
            'sale_seatprice': 25,
            'sale_surcharge': 2.50,
            'total_sale_seatprice': 50,
            'total_sale_surcharge': 5,
        }

        ticket_order = TicketOrder.from_api_data(data)

        assert ticket_order.code == 'ADULT'
        assert ticket_order.seats == 2
        assert ticket_order.description == 'Adult standard'
        assert isinstance(ticket_order.seatprice, float)
        assert ticket_order.seatprice == 25.0
        assert isinstance(ticket_order.surcharge, float)
        assert ticket_order.surcharge == 2.5
        assert isinstance(ticket_order.total_seatprice, float)
        assert ticket_order.total_seatprice == 50.0
        assert isinstance(ticket_order.total_surcharge, float)
        assert ticket_order.total_surcharge == 5.0
        assert ticket_order.disallowed_mask == 123


class TestOrder:

    def test_from_api_data(self):

        data = {
            "event": {
                "event_id": "6IF",
            },
            "item_number": 1,
            "performance": {
                "perf_id": "6IF-A7N",
            },
            "price_band_code": "C/pool",
            "seat_request_status": "not_requested",
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
        }

        order = Order.from_api_data(data)

        assert order.item == 1
        assert order.price_band_code == 'C/pool'
        assert order.ticket_type_code == 'CIRCLE'
        assert order.ticket_type_description == 'Upper circle'
        assert order.seats == 3
        assert order.total_seatprice == 51
        assert order.total_surcharge == 5.40
        assert order.seat_request_status == 'not_requested'

        assert isinstance(order.event, Event)
        assert order.event.event_id == '6IF'
        assert isinstance(order.performance, Performance)
        assert order.performance.performance_id == '6IF-A7N'

        assert len(order.ticket_orders) == 2
        assert order.ticket_orders[0].code == 'ADULT'
        assert order.ticket_orders[1].code == 'CHILD'
