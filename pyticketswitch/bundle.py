from pyticketswitch.order import Order
from pyticketswitch.mixins import JSONMixin
from pyticketswitch.debitor import Debitor


class Bundle(JSONMixin, object):
    """A collection of orders into the same backend system

    Attributes:
        source_code (str): the identifier of the backend system.
        orders (list): the orders.
        description (str): description of the backend system.
        total_seatprice (float): the total cost of the seats/tickets in the
            bundle.
        total_surcharge (float): the total additional charges for the bundle.
        total_send_cost (float): the total postage fee for the bundle.
        total (float): the total amount of money required to purchase this
            bundle.
        currency_code (str): the currency that the prices are in.
        debitor (:class:`Debitor <pyticketswitch.debitor.Debitor>`):
            information about an external debitor that will be used to take
            payment for this bundle. When you are selling on credit, or the
            source system is taking payment, this will be :obj:`None`.
        terms_and_conditions (str): supplier terms and conditions. Only
            availabile when requested with the optional ``source_info`` flag.

    """

    def __init__(self, source_code, orders=None, description=None,
                 total_seatprice=None, total_surcharge=None,
                 total_send_cost=None, total=None, currency_code=None,
                 debitor=None, terms_and_conditions=None):
        self.source_code = source_code
        self.orders = orders
        self.description = description
        self.total_seatprice = total_seatprice
        self.total_surcharge = total_surcharge
        self.total_send_cost = total_send_cost
        self.total = total
        self.currency_code = currency_code
        self.debitor = debitor
        self.terms_and_conditions = terms_and_conditions

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Bundle object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a bundle.

        Returns:
            :class:`Bundle <pyticketswitch.bundle.Bundle>`: a new
            :class:`Bundle <pyticketswitch.bundle.Bundle>` object
            populated with the data from the api.

        """

        kwargs = {
            'source_code': data.get('bundle_source_code'),
            'description': data.get('bundle_source_desc'),
            'currency_code': data.get('currency_code'),
            'terms_and_conditions': data.get('source_t_and_c'),
        }

        raw_orders = data.get('order')
        if raw_orders:
            orders = [Order.from_api_data(order) for order in raw_orders]
            kwargs.update(orders=orders)

        # Below we are explicital checking for not None because we want to
        # differentiate between situtations where a value is 0 and a value is
        # missing from the response.
        total_seatprice = data.get('bundle_total_seatprice')
        if total_seatprice is not None:
            kwargs.update(total_seatprice=float(total_seatprice))

        total_surcharge = data.get('bundle_total_surcharge')
        if total_surcharge is not None:
            kwargs.update(total_surcharge=float(total_surcharge))

        total_send_cost = data.get('bundle_total_send_cost')
        if total_send_cost is not None:
            kwargs.update(total_send_cost=float(total_send_cost))

        total = data.get('bundle_total_cost')
        if total is not None:
            kwargs.update(total=float(total))

        raw_debitor = data.get('debitor')
        if raw_debitor:
            debitor = Debitor.from_api_data(raw_debitor)
            kwargs.update(debitor=debitor)

        return cls(**kwargs)

    def get_events(self):
        """Get the events in the bundle.

        Returns:
            list: list of :class:`Event <pyticketswitch.event.Event>` objects.
        """
        if not self.orders:
            return []
        return [
            order.event
            for order in self.orders
            if order.event and order.event.id
        ]

    def get_event_ids(self):
        """Get the event ids of the events in the bundle.

        Returns:
            set: set of events IDs (str).

        """
        return {event.id for event in self.get_events()}

    def __repr__(self):
        return u'<Bundle {}>'.format(self.source_code)
