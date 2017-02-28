from pyticketswitch.bundle import Bundle
from pyticketswitch.order import Order
from pyticketswitch.mixins import JSONMixin


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

        """
    def __init__(self, token=None, transaction_uuid=None, transaction_id=None,
                 bundles=None, discarded_orders=None, minutes_left=None):
        self.token = token
        self.transaction_uuid = transaction_uuid
        self.transaction_id = transaction_id
        self.bundles = bundles
        self.discarded_orders = discarded_orders
        self.minutes_left = minutes_left

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
            'transaction_id': raw_contents.get('transaction_id')
        }

        minutes = data.get('minutes_left_on_reserve')
        if minutes is not None:
            kwargs.update(minutes_left=float(minutes))

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

    def __repr__(self):
        if self.transaction_id:
            return u'<Trolley id:{}>'.format(self.transaction_id)
        if self.transaction_uuid:
            return u'<Trolley uuid:{}>'.format(self.transaction_uuid)
        if self.token:
            return u'<Trolley token:{}>'.format(self.token)

        return super(Trolley, self).__repr__()
