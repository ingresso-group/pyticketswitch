from pyticketswitch.event import Event
from pyticketswitch.performance import Performance
from pyticketswitch.seat import Seat
from pyticketswitch.send_method import SendMethod
from pyticketswitch.mixins import JSONMixin


class TicketOrder(JSONMixin, object):
    """Describes a set of identical priced tickets.

    Attributes:
        code (str): the discount code.
        seats (list): list of seat IDs.
        number_of_seats (int): number of seats of this type the ticket
            order represents.
        description (str): the discount description.
        seatprice (float): price of individual seat in this ticket order.
        surcharge (float): additional surcharge added per seat in this
            ticket order.
        total_seatprice (float): seatprice for all tickets in the ticket order.
        total_surcharge (float): surcharge for all tickets in the ticket order.

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

    def combined_price(self):
        """Returns the combined seatprice and surcharge.

        This method assumes that we have both a seatprice and surcharge.
        In the situation where are missing either a seatprice or a surcharge
        then we don't have all the information to be able provide this
        information.

        Returns:
            float: the ticket order seatprice and surcharge

        Raises:
            AssertionError: It might seem like the obvious thing to do would be
                to assume the missing data was in fact zero and simply allow the
                addition to continue. However that would be somewhat dangerous when
                we are talking about prices, and it's better to actually raise an
                exception to indicate that there was a problem with the objects
                data, than to inform a customer that the tickets are free or have
                no booking fees

        """
        assert self.seatprice is not None, 'seatprice data missing'
        assert self.surcharge is not None, 'surcharge data missing'
        return self.seatprice + self.surcharge

    def total_combined_price(self):
        """Returns the combined total seatprice and surcharge.

        This method assumes that we have both a seatprice and surcharge.
        In the situation where are missing either a seatprice or a surcharge
        then we don't have all the information to be able provide this
        information.

        Returns:
            float: the ticket order total seatprice and total surcharge

        Raises:
            AssertionError: It might seem like the obvious thing to do would be
                to assume the missing data was in fact zero and simply allow the
                addition to continue. However that would be somewhat dangerous when
                we are talking about prices, and it's better to actually raise an
                exception to indicate that there was a problem with the objects
                data, than to inform a customer that the tickets are free or have
                no booking fees

        """
        assert self.total_seatprice is not None, 'seatprice data missing'
        assert self.total_surcharge is not None, 'surcharge data missing'
        return self.total_seatprice + self.total_surcharge

    def __repr__(self):
        return u'<TicketOrder {}>'.format(self.code)


class Order(JSONMixin, object):
    """Describes tickets for a specific event/performance.

    Attributes:
        item (int): the item number within the trolley. If an order is removed
            from the trolley it will retain it's item number.
        event (:class:`Event <pyticketswitch.event.Event>`): the event
            the order is for.
        performance (:class:`Performance <pyticketswitch.performance.Performance>`):
            the performance the order is for.
        price_band_code (str): the price band identifier.
        ticket_type_code (str): the ticket type identifier.
        ticket_type_description (str): description of the ticket type.
        ticket_orders (list): list of
            :class:`TicketOrders <pyticketswitch.order.TicketOrder>` that
            provide information on the specific tickets in the order.
        number_of_seats (int): total number of seats/tickets in the
            order.
        total_seatprice (float): total seat price of the order.
        total_surcharge (float): total additional surcharges for the order.
        seat_request_status (str): the status of requested seats. Will be filled
            after the order has been reserved, and :obj:`None` before.
        requested_seats (list): list of
            :class:`Seats <pyticketswitch.seat.Seat>` requested at reservation
            time.
        backend_purchase_reference (str): a reference from the source
            supplier for this order. This is generally empty until the order
            has been successfully purchased.
        send_method (:class:`SendMethod <pyticketswitch.send_method.SendMethod>`):
            method of ticket delivery. Only present when requested.

    """

    def __init__(self, item, event=None, performance=None, price_band_code=None,
                 ticket_type_code=None, ticket_type_description=None,
                 ticket_orders=None, number_of_seats=None,
                 total_seatprice=None, total_surcharge=None,
                 seat_request_status=None, requested_seat_ids=None,
                 backend_purchase_reference=None, send_method=None):

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
        self.requested_seat_ids = requested_seat_ids
        self.backend_purchase_reference = backend_purchase_reference
        self.send_method = send_method

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
            'requested_seat_ids': data.get('requested_seat_ids'),
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

        raw_send_method = data.get('send_method')
        if raw_send_method:
            send_method = SendMethod.from_api_data(raw_send_method)
            kwargs.update(send_method=send_method)

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
            if ticket_order.seats
            for seat in ticket_order.seats
        ]

    def get_seat_ids(self):
        """Get all seat ids from all :class:`TicketOrders <pyticketswitch.order.TickerOrder>`

        Returns:
            list: list of seat ids.

        """
        return [seat.id for seat in self.get_seats() if seat.id]

    def unique_seat_text(self):
        """Get the unique seat text for all seats in an order

        Returns:
            string: string combining all seat texts for the order

        """
        text_set = {
            seat.seat_text: seat.seat_text
            for seat in self.get_seats() if seat.seat_text
        }
        return ', '.join(seat_text for seat_text in text_set.values())

    def total_including_send_cost(self):
        return self.total_seatprice + self.total_surcharge + self.send_method.cost

    def __repr__(self):
        return u'<Order {}>'.format(self.item)
