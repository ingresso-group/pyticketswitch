from pyticketswitch.event import Event
from pyticketswitch.performance import Performance
from pyticketswitch.seat import Seat
from pyticketswitch.mixins import JSONMixin


class TicketOrder(JSONMixin, object):

    def __init__(self, code, seats=None, number_of_seats=None, description=None,
                 seatprice=None, surcharge=None, total_seatprice=None,
                 total_surcharge=None, disallowed_mask=None):
        self.code = code
        self.seats = seats
        self.description = description
        self.number_of_seats = number_of_seats
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.total_seatprice = total_seatprice
        self.total_surcharge = total_surcharge
        self.disallowed_mask = disallowed_mask

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'code': data.get('discount_code'),
            'number_of_seats': data.get('no_of_seats'),
            'description': data.get('discount_desc'),
            'disallowed_mask': data.get('discount_disallowed_seat_no_bitmask'),
        }

        # Below we are explicital checking for not None because we want to
        # differentiate between situtations where a value is 0 and a value is
        # missing from the response.
        raw_seatprice = data.get('sale_seatprice')
        if raw_seatprice is not None:
            kwargs.update(seatprice=float(raw_seatprice))

        raw_surcharge = data.get('sale_surcharge')
        if raw_surcharge is not None:
            kwargs.update(surcharge=float(raw_surcharge))

        raw_total_seatprice = data.get('total_sale_seatprice')
        if raw_total_seatprice is not None:
            kwargs.update(total_seatprice=float(raw_total_seatprice))

        raw_total_surcharge = data.get('total_sale_surcharge')
        if raw_total_surcharge is not None:
            kwargs.update(total_surcharge=float(raw_total_surcharge))

        seats_data = data.get('seats')
        if seats_data:
            seats = [
                Seat.from_api_data(seat)
                for seat in seats_data
            ]
            kwargs.update(seats=seats)

        return cls(**kwargs)

    def __repr__(self):
        return u'<TicketOrder {}>'.format(self.code)


class Order(JSONMixin, object):

    def __init__(self, item, event=None, performance=None, price_band_code=None,
                 ticket_type_code=None, ticket_type_description=None,
                 ticket_orders=None, number_of_seats=None,
                 total_seatprice=None, total_surcharge=None,
                 seat_request_status=None, requested_seats=None):
        self.item = item
        self.event = event
        self.performance = performance
        self.price_band_code = price_band_code
        self.ticket_type_code = ticket_type_code
        self.ticket_type_description = ticket_type_description
        self.ticket_orders = ticket_orders
        self.number_of_seats = number_of_seats
        self.total_seatprice = total_seatprice
        self.total_surcharge = total_surcharge
        self.seat_request_status = seat_request_status
        self.requested_seats = requested_seats

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'item': data.get('item_number'),
            'number_of_seats': data.get('total_no_of_seats'),
            'price_band_code': data.get('price_band_code'),
            'ticket_type_code': data.get('ticket_type_code'),
            'ticket_type_description': data.get('ticket_type_desc'),
            'seat_request_status': data.get('seat_request_status'),
        }

        raw_event = data.get('event')
        if raw_event:
            event = Event.from_api_data(raw_event)
            kwargs.update(event=event)

        raw_performance = data.get('performance')
        if raw_performance:
            performance = Performance.from_api_data(raw_performance)
            kwargs.update(performance=performance)

        raw_ticket_orders = data.get('ticket_orders', {}).get('ticket_order')
        if raw_ticket_orders:
            ticket_orders = [
                TicketOrder.from_api_data(ticket_order)
                for ticket_order in raw_ticket_orders
            ]
            kwargs.update(ticket_orders=ticket_orders)

        raw_total_seatprice = data.get('total_sale_seatprice')
        if raw_total_seatprice is not None:
            kwargs.update(total_seatprice=float(raw_total_seatprice))

        raw_total_surcharge = data.get('total_sale_surcharge')
        if raw_total_surcharge is not None:
            kwargs.update(total_surcharge=float(raw_total_surcharge))

        raw_requested_seats = data.get('requested_seats')
        if raw_requested_seats:
            requested_seats = [
                Seat.from_api_data(seat)
                for seat in raw_requested_seats
            ]
            kwargs.update(requested_seats=requested_seats)

        return cls(**kwargs)

    def get_seats(self):
        if not self.ticket_orders:
            return []

        return [
            seat
            for ticket_order in self.ticket_orders
            for seat in ticket_order.seats
            if ticket_order.seats
        ]

    def __repr__(self):
        return u'<Order {}>'.format(self.item)
