from pyticketswitch.event import Event
from pyticketswitch.performance import Performance
from pyticketswitch.seat import Seat
from pyticketswitch.mixins import JSONMixin


class TicketOrder(JSONMixin, object):
    """Describes a set of identical priced tickets.

    Args:
        code (str): the discount code.
        seats (list, optional): list of seat IDs. Defaults to :obj:`None`.
        number_of_seats (int, optional): number of seats of this type the ticket
            order represents. Defaults to :obj:`None`.
        description (str, optional): the discount description. Defaults to
            :obj:`None`.
        seatprice (float, optional): price of individual seat in this ticket
            order. Defaults to :obj:`None`.
        surcharge (float, optional): additional surcharge added per seat in this
            ticket order. Defaults to :obj:`None`.
        total_seatprice (float, optional): seatprice for all tickets in the
            ticket order. Defaults to :obj:`None`.
        total_seatprice (float, optional): seatprice for all tickets in the
            ticket order. Defaults to :obj:`None`.

    """

    def __init__(self, code, seats=None, number_of_seats=None, description=None,
                 seatprice=None, surcharge=None, total_seatprice=None,
                 total_surcharge=None):
        self.code = code
        self.seats = seats
        self.description = description
        self.number_of_seats = number_of_seats
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.total_seatprice = total_seatprice
        self.total_surcharge = total_surcharge

    @classmethod
    def from_api_data(cls, data):
        """Creates a new **TicketOrder** object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a ticket order.

        Returns:
            :class:`TicketOrder <pyticketswitch.order.TicketOrder>`: a new
            :class:`TicketOrder <pyticketswitch.order.TicketOrder>` object
            populated with the data from the api.

        """

        kwargs = {
            'code': data.get('discount_code'),
            'number_of_seats': data.get('no_of_seats'),
            'description': data.get('discount_desc'),
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
    """Describes tickets for a specific event/performance.

    Args:
        item (int): the item number within the trolley. If an order is removed
            from the trolley it will retain it's item number.
        event (:class:`Event <pyticketswitch.event.Event>`, optional): the event
            the order is for. Defaults to :obj:`None`.
        performance (:class:`Performance <pyticketswitch.performance.Performance>`, optional):
            the performance the order is for. Defaults to :obj:`None`.
        price_band_code (str, optional): the price band identifier. Defaults to
            :obj:`None`.
        ticket_type_code (str, optional): the ticket type identifier. Defaults
            to :obj:`None`.
        ticket_type_description (str, optional): description of the ticket type.
            Defaults to :obj:`None`.
        ticket_orders (list, optional): list of
            :class:`TicketOrders <pyticketswitch.order.TicketOrder>` that
            provide information on the specific tickets in the order. Defaults
            to :obj:`None`.
        number_of_seats (int, optional): total number of seats/tickets in the
            order. Defaults to :obj:`None`.
        total_seatprice (float, optional): total seat price of the order.
            Defaults to :obj:`None`
        total_surcharge (float, optional): total additional surcharges for the
            order. Defaults to :obj:`None`.
        seat_request_status (str, optional): when specifying seats this field
            will indicate wether the chosen seats were successfully reserved.
            otherwise will be ``not_requested``. Defaults to :obj:`None`.
        requested_seats (list, optional): list of
            :class:`Seats <pyticketswitch.seat.Seat>` requested at reservation
            time. Defaults to :obj:`None`.
        backend_purchase_reference (str, optional): a reference from the source
            supplier for this order. This is generally empty until the order
            has been successfully purchased. Defaults to :obj:`None`.

    """

    def __init__(self, item, event=None, performance=None, price_band_code=None,
                 ticket_type_code=None, ticket_type_description=None,
                 ticket_orders=None, number_of_seats=None,
                 total_seatprice=None, total_surcharge=None,
                 seat_request_status=None, requested_seats=None,
                 backend_purchase_reference=None):

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
        self.backend_purchase_reference = backend_purchase_reference

    @classmethod
    def from_api_data(cls, data):
        """Creates a new **Order** object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a order.

        Returns:
            :class:`Order <pyticketswitch.order.Order>`: a new
            :class:`Order <pyticketswitch.order.Order>` object populated with
            the data from the api.

        """
        kwargs = {
            'item': data.get('item_number'),
            'number_of_seats': data.get('total_no_of_seats'),
            'price_band_code': data.get('price_band_code'),
            'ticket_type_code': data.get('ticket_type_code'),
            'ticket_type_description': data.get('ticket_type_desc'),
            'seat_request_status': data.get('seat_request_status'),
            'backend_purchase_reference': data.get('backend_purchase_reference'),
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
        """Get all seats from all :class:`TicketOrder <pyticketswitch.order.TicketOrder>` children.

        Returns:
            list: list of `Seats <pyticketswitch.seat.Seat>`.

        """
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
