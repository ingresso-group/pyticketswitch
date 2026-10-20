from __future__ import annotations

from pyticketswitch.sold_order import SoldOrder


class SuppliedOrder(SoldOrder):
    """An order that was supplied, as returned by ``orders_supplied.v1``.

    The API returns the same data as for ``orders_sold.v1``, so this is a
    :class:`SoldOrder <pyticketswitch.sold_order.SoldOrder>` and has all of its
    attributes. The difference is the point of view: these are the orders the
    calling user supplied, and ``purchase_user`` is the user that sold them.
    """
