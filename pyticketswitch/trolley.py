from pyticketswitch.bundle import Bundle
from pyticketswitch.order import Order


class Trolley(object):

    def __init__(self, token=None, random_index=None, bundles=None, discarded_orders=None):
        self.token = token
        self.random_index = random_index
        self.bundles = bundles
        self.discarded_orders = discarded_orders

    @classmethod
    def from_api_data(cls, data):

        raw_contents = data.get('trolley_contents', {})
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
            'random_index': data.get('random_index'),
            'bundles': bundles,
            'discarded_orders': discarded_orders,
        }

        return cls(**kwargs)
