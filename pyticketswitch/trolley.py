from pyticketswitch.bundle import Bundle
from pyticketswitch.order import Order
from pyticketswitch.mixins import JSONMixin
from pyticketswitch.purchase_result import PurchaseResult


class Trolley(JSONMixin, object):
    """Describes a collection of products that are being purchased.

    Attributes:
        token (str): a token that represents the current state of the trolley.
        transaction_uuid (str): unique identifier for this trolley. Only
            present after reservation.
        transaction_id (str): unique identifier for this trolley. Only present
            after purchase. This supposed to be an identifer that is easily
            readable/recognisable by a human being.
        bundles (list): list of :class:`Bundles <pyticketswitch.bundle.Bundle>`
            objects that break down the items to be purchased by their source
            systems.
        discarded_orders (list): list of
            :class:`Orders <pyticketswitch.order.Order>` objects that were in
            the trolley in the past but have been removed.
        minutes_left (float): the number of minutes left before a reservation
            expires.
        order_count (int): the number of orders in the trolley.
        purchase_result (:class:`PurchaseResult <pyticketswitch.callout.Callout>`):
            the result of the purchase attempt when available.
        input_contained_unavailable_order (bool): indicates that the call used
            to create or modify this trolley object included at least one order
            that was not available.
    """
    def __init__(self, token=None, transaction_uuid=None, transaction_id=None,
                 bundles=None, discarded_orders=None, minutes_left=None,
                 order_count=None, purchase_result=None,
                 input_contained_unavailable_order=False):
        self.token = token
        self.transaction_uuid = transaction_uuid
        self.transaction_id = transaction_id
        self.bundles = bundles
        self.discarded_orders = discarded_orders
        self.minutes_left = minutes_left
        self.order_count = order_count
        self.purchase_result = purchase_result
        self.input_contained_unavailable_order = input_contained_unavailable_order

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Trolley object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a trolley.

        Returns:
            :class:`Trolley <pyticketswitch.trolley.Trolley>`: a new
            :class:`Trolley <pyticketswitch.trolley.Trolley>` object
            populated with the data from the api.

        """
        raw_contents = data.get('trolley_contents', {})

        if not raw_contents:
            raw_contents = data.get('reserved_trolley', {})

        if not raw_contents:
            raw_contents = data.get('trolley_token_contents', {})

        raw_bundles = raw_contents.get('bundle', [])

        bundles = [
            Bundle.from_api_data(bundle)
            for bundle in raw_bundles
        ]

        raw_discarded_orders = data.get('discarded_orders', [])

        discarded_orders = [
            Order.from_api_data(order)
            for order in raw_discarded_orders
        ]

        kwargs = {
            'token': data.get('trolley_token'),
            'bundles': bundles,
            'discarded_orders': discarded_orders,
            'transaction_uuid': raw_contents.get('transaction_uuid'),
            'transaction_id': raw_contents.get('transaction_id'),
            'order_count': data.get('trolley_order_count'),
            'input_contained_unavailable_order': data.get(
                'input_contained_unavailable_order', False),
        }

        minutes = data.get('minutes_left_on_reserve')
        if minutes is not None:
            kwargs.update(minutes_left=float(minutes))

        purchase_result = raw_contents.get('purchase_result')
        if purchase_result:
            kwargs.update(
                purchase_result=PurchaseResult.from_api_data(purchase_result))

        return cls(**kwargs)

    def get_events(self):
        """Get the events in the trolley.

        Returns:
            list: list of :class:`Event <pyticketswitch.event.Event>` objects.
        """
        if not self.bundles:
            return []
        return [
            event
            for bundle in self.bundles
            for event in bundle.get_events()
            if event and event.id
        ]

    def get_event_ids(self):
        """Get the event ids of the events in the trolley.

        Returns:
            set: set of events IDs (str).

        """
        return {event.id for event in self.get_events()}

    def get_bundle(self, source_code):
        """Find a bundle with a specific source code

        Args:
            source_code (str): the source code for the target bundle.

        Returns:
            :class:`Bundle <pyticketswitch.bundle.Bundle>`: the bundle with the
            requested source code.

            When no bundle with that source code is present returns :obj:`None`.

        """

        if not self.bundles:
            return None

        for bundle in self.bundles:
            if bundle.source_code == source_code:
                return bundle

        return None

    def get_item(self, item_number):
        """Find an order with the given item number

        Args:
            item_number (int): the item number of the target order

        Returns:
            :class:`Order <pyticketswitch.order.order>`: the order with the
            specified

        """
        if not self.bundles:
            return None

        for order in self.get_orders():
            if order.item == item_number:
                return order

        return None

    def get_orders(self):
        """Get all orders in all bundles in a trolley

        Returns:
            list: orders from all bundles in the the trolley

        """

        if not self.bundles:
            return []

        return [
            order
            for bundle in self.bundles
            if bundle.orders
            for order in bundle.orders
        ]

    def __repr__(self):
        if self.transaction_id:
            return u'<Trolley id:{}>'.format(self.transaction_id)
        if self.transaction_uuid:
            return u'<Trolley uuid:{}>'.format(self.transaction_uuid)
        if self.token:
            return u'<Trolley token:{}>'.format(self.token)

        return super(Trolley, self).__repr__()
