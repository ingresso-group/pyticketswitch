from __future__ import annotations

import datetime
from typing import Any

from pyticketswitch.commission import Commission
from pyticketswitch.customer import Customer
from pyticketswitch.event import Event
from pyticketswitch.order import Order
from pyticketswitch.performance import Performance
from pyticketswitch.send_method import SendMethod
from pyticketswitch.user import User
from pyticketswitch.utils import get_price, isostr_to_datetime


class SoldOrder(Order):
    """An order that was sold, as returned by ``orders_sold.v1``.

    A :class:`SoldOrder` is an :class:`Order <pyticketswitch.order.Order>` with
    the details of the transaction it was sold in. The attributes that
    :class:`Order <pyticketswitch.order.Order>` already has are filled in from
    the API data:

    - ``item``, ``number_of_seats``, ``price_band_code``, ``ticket_type_code``,
      ``ticket_type_description``, ``backend_purchase_reference``,
      ``total_seatprice`` and ``total_surcharge``. The prices are converted
      from the strings the API returns to floats. ``total_seatprice`` comes
      from the API's ``total_seat_cost``, which is the sale seat price
      excluding the surcharge, as ``total_sale_seatprice`` is elsewhere.
    - ``event``, with its description, country, venue and area.
    - ``performance``, with its time (without a time zone, as the API does not
      return one), name and event ID. Its ``id`` is :obj:`None`, as the API
      does not return a performance ID.
    - ``send_method``. Its ``type`` is the send method actually used, so it can
      be ``"post"``, ``"collect"``, ``"selfprint"`` or ``"failed"``, and a
      dynamic send method shows as the one it resolved to.
    - ``gross_commission`` and ``user_commission``, when the calling user can
      see them.
    - ``cancellation_status`` is ``"cancelled"`` when the API reports every
      seat as cancelled, and :obj:`None` otherwise. The API's own value is in
      ``seat_cancellation_status``.

    Everything else the API returns is kept in the attributes below. Where the
    library already has a name for something it is used (``transaction_id``,
    ``agent_reference`` and so on), the ``*_list`` suffix is dropped and
    ``*_desc`` is spelt out. The ``*_can_use_data`` flags are converted from
    ``"yes"``/``"no"`` to booleans. The cancellation, refund and commission
    fields are only returned for purchases that succeeded, and the gift card
    and exchange fields only when they apply, so expect :obj:`None` in those
    attributes otherwise.

    Attributes:
        transaction_uuid (str): the API's ``transaction_uuid``.
        transaction_id (str): the API's ``trans_id``.
        source_code (str): the API's ``backend_system``.
        source_description (str): the API's ``backend_desc``.
        currency_code (str): the API's ``currency``.
        purchased_at (datetime.datetime): the API's ``purchase_iso8601_date_and_time``.
        remote_site (str): the API's ``remote_site``.
        purchase_succeeded (bool): the API's ``purchase_succeeded``.
        customer (:class:`Customer <pyticketswitch.customer.Customer>`): the customer, when the call was made with ``add_customer`` and the calling user is allowed to see the customer data. Its ``agent_reference`` falls back to the order's.
        agent_reference (str): the API's ``agent_ref``.
        area_description (str): the API's ``area_desc``.
        area_description_from_backend (str): the API's ``area_desc_from_backend``.
        barcodes (list[str]): the API's ``barcode_data_list``.
        cancellation_blocked_by_result (bool): the API's ``cancellation_blocked_by_result``.
        cancellation_blocked_by_settings (bool): the API's ``cancellation_blocked_by_settings``.
        cancellation_possible (bool): the API's ``cancellation_possible``.
        discount_codes (list[str]): the API's ``discount_codes_list``.
        event_code (str): the API's ``event_code``.
        event_description_from_backend (str): the API's ``event_desc_from_backend``.
        event_subdata (str): the API's ``event_subdata``.
        gift_card_currency (str): the API's ``gift_card_currency``.
        gift_card_issued (bool): the API's ``gift_card_issued``.
        gift_card_number (str): the API's ``gift_card_number``.
        gift_card_type (str): the API's ``gift_card_type``.
        gift_card_valid_from (datetime.datetime): the API's ``gift_card_valid_from_iso8601``.
        gift_card_valid_until (datetime.datetime): the API's ``gift_card_valid_until_iso8601``.
        gift_card_value (str): the API's ``gift_card_value``.
        has_been_exchanged (bool): the API's ``has_been_exchanged``.
        is_exchange_replacement (bool): the API's ``is_exchange_replacement``.
        is_package_component (bool): the API's ``is_package_component``.
        last_cancellation_type (str): the API's ``last_cancellation_type``.
        last_modified_at (datetime.datetime): the API's ``last_modified_iso8601_date_and_time``.
        owner_code (str): the API's ``owner_code``.
        performance_is_cancelled (bool): the API's ``perf_is_cancelled``.
        performance_type_code (str): the API's ``perf_type_code``.
        purchase_sub_user (str): the API's ``purchase_sub_user``.
        purchase_user (str): the API's ``purchase_user``.
        purchase_user_details (User): the API's ``purchase_user_details``.
        replacement_item_number (int): the API's ``replacement_item_number``.
        replacement_transaction_id (str): the API's ``replacement_trans_id``.
        seat_cancellation_status (str): the API's ``seat_cancellation_status``.
        seat_ids (list[str]): the API's ``seat_id_list``.
        seat_refund_status (str): the API's ``seat_refund_status``.
        supplier_can_use_data (bool): the API's ``supplier_can_use_customer_data``.
        supplier_code (str): the API's ``supplier_code``.
        tag_codes (list[str]): the API's ``tag_codes_list``.
        transaction_type (str): the API's ``trans_type``.
        user_can_use_data (bool): the API's ``user_can_use_customer_data``.
        venue_description_from_backend (str): the API's ``venue_desc_from_backend``.
        world_can_use_data (bool): the API's ``world_can_use_customer_data``.
    """

    def __init__(
        self,
        *args: Any,
        transaction_uuid: str | None = None,
        transaction_id: str | None = None,
        source_code: str | None = None,
        source_description: str | None = None,
        currency_code: str | None = None,
        purchased_at: datetime.datetime | None = None,
        remote_site: str | None = None,
        purchase_succeeded: bool | None = None,
        customer: Customer | None = None,
        agent_reference: str | None = None,
        area_description: str | None = None,
        area_description_from_backend: str | None = None,
        barcodes: list[str] | None = None,
        cancellation_blocked_by_result: bool | None = None,
        cancellation_blocked_by_settings: bool | None = None,
        cancellation_possible: bool | None = None,
        discount_codes: list[str] | None = None,
        event_code: str | None = None,
        event_description_from_backend: str | None = None,
        event_subdata: str | None = None,
        gift_card_currency: str | None = None,
        gift_card_issued: bool | None = None,
        gift_card_number: str | None = None,
        gift_card_type: str | None = None,
        gift_card_valid_from: datetime.datetime | None = None,
        gift_card_valid_until: datetime.datetime | None = None,
        gift_card_value: str | None = None,
        has_been_exchanged: bool | None = None,
        is_exchange_replacement: bool | None = None,
        is_package_component: bool | None = None,
        last_cancellation_type: str | None = None,
        last_modified_at: datetime.datetime | None = None,
        owner_code: str | None = None,
        performance_is_cancelled: bool | None = None,
        performance_type_code: str | None = None,
        purchase_sub_user: str | None = None,
        purchase_user: str | None = None,
        purchase_user_details: User | None = None,
        replacement_item_number: int | None = None,
        replacement_transaction_id: str | None = None,
        seat_cancellation_status: str | None = None,
        seat_ids: list[str] | None = None,
        seat_refund_status: str | None = None,
        supplier_can_use_data: bool | None = None,
        supplier_code: str | None = None,
        tag_codes: list[str] | None = None,
        transaction_type: str | None = None,
        user_can_use_data: bool | None = None,
        venue_description_from_backend: str | None = None,
        world_can_use_data: bool | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.transaction_uuid = transaction_uuid
        self.transaction_id = transaction_id
        self.source_code = source_code
        self.source_description = source_description
        self.currency_code = currency_code
        self.purchased_at = purchased_at
        self.remote_site = remote_site
        self.purchase_succeeded = purchase_succeeded
        self.customer = customer
        self.agent_reference = agent_reference
        self.area_description = area_description
        self.area_description_from_backend = area_description_from_backend
        self.barcodes = barcodes
        self.cancellation_blocked_by_result = cancellation_blocked_by_result
        self.cancellation_blocked_by_settings = cancellation_blocked_by_settings
        self.cancellation_possible = cancellation_possible
        self.discount_codes = discount_codes
        self.event_code = event_code
        self.event_description_from_backend = event_description_from_backend
        self.event_subdata = event_subdata
        self.gift_card_currency = gift_card_currency
        self.gift_card_issued = gift_card_issued
        self.gift_card_number = gift_card_number
        self.gift_card_type = gift_card_type
        self.gift_card_valid_from = gift_card_valid_from
        self.gift_card_valid_until = gift_card_valid_until
        self.gift_card_value = gift_card_value
        self.has_been_exchanged = has_been_exchanged
        self.is_exchange_replacement = is_exchange_replacement
        self.is_package_component = is_package_component
        self.last_cancellation_type = last_cancellation_type
        self.last_modified_at = last_modified_at
        self.owner_code = owner_code
        self.performance_is_cancelled = performance_is_cancelled
        self.performance_type_code = performance_type_code
        self.purchase_sub_user = purchase_sub_user
        self.purchase_user = purchase_user
        self.purchase_user_details = purchase_user_details
        self.replacement_item_number = replacement_item_number
        self.replacement_transaction_id = replacement_transaction_id
        self.seat_cancellation_status = seat_cancellation_status
        self.seat_ids = seat_ids
        self.seat_refund_status = seat_refund_status
        self.supplier_can_use_data = supplier_can_use_data
        self.supplier_code = supplier_code
        self.tag_codes = tag_codes
        self.transaction_type = transaction_type
        self.user_can_use_data = user_can_use_data
        self.venue_description_from_backend = venue_description_from_backend
        self.world_can_use_data = world_can_use_data

    @staticmethod
    def _datetime(raw: str | None) -> datetime.datetime | None:
        return isostr_to_datetime(raw) if raw else None

    @staticmethod
    def _yes_no(raw: str | None) -> bool | None:
        return None if raw is None else raw == "yes"

    @staticmethod
    def _user(raw: dict[str, Any] | None) -> User | None:
        return User.from_api_data({"user_info": raw}) if raw else None

    @staticmethod
    def _commission(data: dict[str, Any], prefix: str) -> Commission | None:
        currency = data.get(f"{prefix}_currency")
        including_vat = get_price(data, f"{prefix}_inc_vat")
        excluding_vat = get_price(data, f"{prefix}_ex_vat")
        if currency is None and including_vat is None and excluding_vat is None:
            return None
        return Commission(
            including_vat=including_vat,
            excluding_vat=excluding_vat,
            currency_code=currency,
        )

    @staticmethod
    def _customer(
        raw: dict[str, Any] | None, agent_reference: str | None
    ) -> Customer | None:
        if not raw:
            return None
        # the customer data uses the new data protection names, which
        # Customer.from_api_data does not read
        return Customer.from_api_data(
            {
                "agent_ref": agent_reference,
                "dp_user": raw.get("user_can_use_customer_data"),
                "dp_supplier": raw.get("supplier_can_use_customer_data"),
                "dp_world": raw.get("world_can_use_customer_data"),
                **raw,
            }
        )

    @classmethod
    def from_api_data(cls, data: dict[str, Any]) -> SoldOrder:
        """Creates a new SoldOrder object from API data from ticketswitch.

        Args:
            data (dict): one entry from the ``orders`` list in the response
                from the ``orders_sold.v1`` API call.

        Returns:
            :class:`SoldOrder <pyticketswitch.sold_order.SoldOrder>`: a new
            :class:`SoldOrder <pyticketswitch.sold_order.SoldOrder>` object
            populated with the data from the api.

        """
        # only pass the event data on, as the Event keeps the dictionary it is
        # given and the rest of the data (e.g. the customer) does not belong there
        event_data = {
            key: data[key]
            for key in (
                "event_id",
                "event_desc",
                "venue_desc",
                "venue_code",
                "area_code",
            )
            if key in data
        }
        if "event_country_code" in data:
            event_data["country_code"] = data["event_country_code"]

        send_method = None
        if any(
            data.get(key) is not None
            for key in ("send_code", "send_desc", "actual_send_method")
        ):
            send_method = SendMethod(
                code=data.get("send_code"),
                description=data.get("send_desc"),
                typ=data.get("actual_send_method"),
            )

        kwargs: dict[str, Any] = {
            "event": Event.from_api_data(event_data),
            "performance": Performance(
                id_=None,
                event_id=data.get("event_id"),
                date_time=cls._datetime(data.get("perf_iso8601_date_and_time")),
                name=data.get("perf_name") or None,
            ),
            "send_method": send_method,
            "cancellation_status": (
                "cancelled" if data.get("seat_cancellation_status") == "all" else None
            ),
            "gross_commission": cls._commission(data, "gross_commission"),
            "user_commission": cls._commission(data, "user_commission"),
            "customer": cls._customer(data.get("customer"), data.get("agent_ref")),
            "item": data.get("item_number"),
            "number_of_seats": data.get("total_no_of_seats"),
            "price_band_code": data.get("price_band"),
            "ticket_type_code": data.get("type_code"),
            "ticket_type_description": data.get("type_desc"),
            "backend_purchase_reference": data.get("backend_purchase_ref"),
            "total_seatprice": get_price(data, "total_seat_cost"),
            "total_surcharge": get_price(data, "total_surcharge"),
            "transaction_uuid": data.get("transaction_uuid"),
            "transaction_id": data.get("trans_id"),
            "source_code": data.get("backend_system"),
            "source_description": data.get("backend_desc"),
            "currency_code": data.get("currency"),
            "purchased_at": cls._datetime(data.get("purchase_iso8601_date_and_time")),
            "remote_site": data.get("remote_site"),
            "purchase_succeeded": data.get("purchase_succeeded"),
            "agent_reference": data.get("agent_ref"),
            "area_description": data.get("area_desc"),
            "area_description_from_backend": data.get("area_desc_from_backend"),
            "barcodes": data.get("barcode_data_list"),
            "cancellation_blocked_by_result": data.get(
                "cancellation_blocked_by_result"
            ),
            "cancellation_blocked_by_settings": data.get(
                "cancellation_blocked_by_settings"
            ),
            "cancellation_possible": data.get("cancellation_possible"),
            "discount_codes": data.get("discount_codes_list"),
            "event_code": data.get("event_code"),
            "event_description_from_backend": data.get("event_desc_from_backend"),
            "event_subdata": data.get("event_subdata"),
            "gift_card_currency": data.get("gift_card_currency"),
            "gift_card_issued": data.get("gift_card_issued"),
            "gift_card_number": data.get("gift_card_number"),
            "gift_card_type": data.get("gift_card_type"),
            "gift_card_valid_from": cls._datetime(
                data.get("gift_card_valid_from_iso8601")
            ),
            "gift_card_valid_until": cls._datetime(
                data.get("gift_card_valid_until_iso8601")
            ),
            "gift_card_value": data.get("gift_card_value"),
            "has_been_exchanged": data.get("has_been_exchanged"),
            "is_exchange_replacement": data.get("is_exchange_replacement"),
            "is_package_component": data.get("is_package_component"),
            "last_cancellation_type": data.get("last_cancellation_type"),
            "last_modified_at": cls._datetime(
                data.get("last_modified_iso8601_date_and_time")
            ),
            "owner_code": data.get("owner_code"),
            "performance_is_cancelled": data.get("perf_is_cancelled"),
            "performance_type_code": data.get("perf_type_code"),
            "purchase_sub_user": data.get("purchase_sub_user"),
            "purchase_user": data.get("purchase_user"),
            "purchase_user_details": cls._user(data.get("purchase_user_details")),
            "replacement_item_number": data.get("replacement_item_number"),
            "replacement_transaction_id": data.get("replacement_trans_id"),
            "seat_cancellation_status": data.get("seat_cancellation_status"),
            "seat_ids": data.get("seat_id_list"),
            "seat_refund_status": data.get("seat_refund_status"),
            "supplier_can_use_data": cls._yes_no(
                data.get("supplier_can_use_customer_data")
            ),
            "supplier_code": data.get("supplier_code"),
            "tag_codes": data.get("tag_codes_list"),
            "transaction_type": data.get("trans_type"),
            "user_can_use_data": cls._yes_no(data.get("user_can_use_customer_data")),
            "venue_description_from_backend": data.get("venue_desc_from_backend"),
            "world_can_use_data": cls._yes_no(data.get("world_can_use_customer_data")),
        }

        return cls(**kwargs)

    def __repr__(self) -> str:
        return f"<SoldOrder {self.transaction_id}>"
