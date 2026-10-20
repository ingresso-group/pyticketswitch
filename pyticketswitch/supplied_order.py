from __future__ import annotations

from pyticketswitch.sold_order import SoldOrder


class SuppliedOrder(SoldOrder):
    """An order for tickets that the calling user supplied, as returned by
    ``orders_supplied.v1``.

    This is the supplier's view of the orders: the sales made by other users
    (the ``purchase_user``) of inventory that belongs to the calling user's
    supplier codes. It is the counterpart of
    :class:`SoldOrder <pyticketswitch.sold_order.SoldOrder>`, which is the
    seller's view of the orders they sold.

    The API returns the same data in both cases, so this is a
    :class:`SoldOrder <pyticketswitch.sold_order.SoldOrder>` and has all of its
    attributes. In the core system ``orders_supplied`` is the ``orders_sold``
    script run in the opposite mode.
    """
