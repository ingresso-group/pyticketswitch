from __future__ import annotations

from typing import Any

from pyticketswitch.mixins import JSONMixin
from pyticketswitch.order import Order
from pyticketswitch.trolley import Trolley


class CancellationResult(JSONMixin):
    def __init__(
        self,
        cancelled_item_numbers: list[int] | None = None,
        must_also_cancel: list[Order] | None = None,
        trolley: Trolley | None = None,
    ) -> None:
        self.cancelled_item_numbers = cancelled_item_numbers
        self.must_also_cancel = must_also_cancel
        self.trolley = trolley

    @classmethod
    def from_api_data(cls, data: dict[str, Any]) -> CancellationResult:
        kwargs = {
            "cancelled_item_numbers": data.get("cancelled_item_numbers", []),
            "trolley": Trolley.from_api_data(data),
        }

        raw_must_also_cancel = data.get("must_also_cancel")
        if raw_must_also_cancel:
            must_also_cancel = [
                Order.from_api_data(order) for order in raw_must_also_cancel
            ]
            kwargs.update(must_also_cancel=must_also_cancel)

        return cls(**kwargs)

    def is_fully_cancelled(self) -> bool:
        if self.trolley is None or not self.trolley.bundles:
            return False
        for bundle in self.trolley.bundles:
            for order in bundle.orders or []:
                if order.cancellation_status != "cancelled":
                    return False

        return True
