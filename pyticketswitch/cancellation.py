from pyticketswitch.mixins import JSONMixin
from pyticketswitch.order import Order
from pyticketswitch.trolley import Trolley


class CancellationResult(JSONMixin):
    def __init__(self, cancelled_item_numbers=None, must_also_cancel=None, trolley=None):
        self.cancelled_item_numbers = cancelled_item_numbers
        self.must_also_cancel = must_also_cancel
        self.trolley = trolley

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            "cancelled_item_numbers": data.get("cancelled_item_numbers", []),
            "trolley": Trolley.from_api_data(data),
        }

        raw_must_also_cancel = data.get("must_also_cancel")
        if raw_must_also_cancel:
            must_also_cancel = [Order.from_api_data(order) for order in raw_must_also_cancel]
            kwargs.update(must_also_cancel=must_also_cancel)

        return cls(**kwargs)
