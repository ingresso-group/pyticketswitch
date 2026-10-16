import datetime
import json

import pytest
from dateutil.tz import tzoffset

from pyticketswitch.order import Order
from pyticketswitch.sold_order import SoldOrder


@pytest.fixture
def orders_data():
    with open("test_data/orders_sold.json") as file_handle:
        return json.load(file_handle)["orders"]


@pytest.fixture
def customer_order_data():
    # an order returned with ``add_customer`` (personal details are made up)
    with open("test_data/orders_sold_with_customer.json") as file_handle:
        return json.load(file_handle)["orders"][0]


@pytest.fixture
def placeholder_order_data():
    # an affiliate order with placeholder customer details and no gross commission
    with open("test_data/orders_sold_with_customer.json") as file_handle:
        return json.load(file_handle)["orders"][1]


class TestSoldOrder:
    ZULU = tzoffset("ZULU", 0)

    def test_is_an_order(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        assert isinstance(sold_order, Order)

    def test_from_api_data_populates_the_library_named_fields(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[1])

        assert sold_order.transaction_id == "U000-000T-0002-LDNX"
        assert (
            sold_order.transaction_uuid
            == "U-00000000-0000-4000-8000-000000000002-00000002-LDNX"
        )
        assert sold_order.item == 1
        assert sold_order.number_of_seats == 2
        assert sold_order.price_band_code == "601APNNMRMBJQQPBSCNQGQHGKKCRPSSGN"
        assert sold_order.ticket_type_code == "1009ADNGHMBMMQCTNJKDHRDRTHPHLKQTH"
        assert sold_order.ticket_type_description == "Section 204"
        assert sold_order.backend_purchase_reference == "PURCHASE-0002"
        assert sold_order.source_code == "magic_mike_live_lasvegas"
        assert sold_order.source_description == "Magic Mike Live Las Vegas"
        assert sold_order.currency_code == "usd"
        assert sold_order.remote_site == "rattatosk-ldn.ingresso.co.uk"
        assert sold_order.purchase_succeeded is True
        assert sold_order.purchased_at == datetime.datetime(
            2025, 11, 21, 23, 59, 2, tzinfo=self.ZULU
        )

    def test_prices_are_numbers(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[1])

        assert sold_order.total_seatprice == 151.82
        assert sold_order.total_surcharge == 0.0

    def test_commissions(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[1])

        assert sold_order.gross_commission.including_vat == 24.98
        assert sold_order.gross_commission.excluding_vat == 20.81
        assert sold_order.gross_commission.currency_code == "usd"
        assert sold_order.user_commission.including_vat == 23.16
        assert sold_order.user_commission.excluding_vat == 23.16

    def test_event(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[1])

        event = sold_order.event
        assert event.id == "1FMY8"
        assert event.description == "Magic Mike Live Las Vegas"
        assert event.venue == (
            "Magic Mike Las Vegas\r\n2535 S. Las Vegas Blvd. Las Vegas, NV 89109"
        )
        assert event.venue_code == "201AGBHDRLQHNHPHKKMPKLGPMDRDTDMVL"
        assert event.area_code == "EW"
        assert event.country_code == "us"

    def test_event_does_not_keep_the_rest_of_the_data(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        assert "agent_ref" not in sold_order.event.raw
        assert "purchase_user" not in sold_order.event.raw

    def test_performance(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[2])

        performance = sold_order.performance
        assert performance.id is None
        assert performance.event_id == "1FVFG"
        assert performance.name == "Reservation Start"
        # the performance time has no time zone in the API data
        assert performance.date_time == datetime.datetime(2025, 11, 23, 11, 30)

    def test_performance_without_a_name(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        assert sold_order.performance.name is None
        assert sold_order.performance.date_time == datetime.datetime(
            2025, 12, 3, 14, 15
        )

    def test_keeps_performance_fields_without_a_slot(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        assert sold_order.performance_type_code == "gnice12032025_0215pm"
        assert sold_order.performance_is_cancelled is False

    def test_send_method_type_is_the_actual_send_method(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        send_method = sold_order.send_method
        assert send_method.code == "7"
        assert send_method.description == "E-ticket (printed or mobile)"
        assert send_method.type == "selfprint"

    def test_send_method_type_for_failed_order(self, orders_data):
        data = {**orders_data[0], "actual_send_method": "failed"}

        assert SoldOrder.from_api_data(data).send_method.type == "failed"

    def test_keeps_the_remaining_fields(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[1])

        assert sold_order.agent_reference == "TP-TEST-0002"
        assert sold_order.purchase_user == "example-user"
        assert sold_order.transaction_type == "direct"
        assert sold_order.barcodes == ["TESTBARCODE0002A", "TESTBARCODE0002B"]
        assert sold_order.seat_ids == ["Table 1 Seat 1", "Table 1 Seat 2"]
        assert sold_order.discount_codes == [
            "GPONFS30/9601AVDDJDNPPDCBTDGNSVVJSTBLBSPNQ"
        ]
        assert sold_order.cancellation_possible is False
        assert sold_order.has_been_exchanged is False
        assert sold_order.venue_description_from_backend == (
            "Magic Mike Live Theater at SAHARA Las Vegas"
        )

    def test_data_protection_flags_are_booleans(self, orders_data):
        data = {
            **orders_data[0],
            "user_can_use_customer_data": "yes",
            "supplier_can_use_customer_data": "no",
        }

        sold_order = SoldOrder.from_api_data(data)

        assert sold_order.user_can_use_data is True
        assert sold_order.supplier_can_use_data is False
        assert sold_order.world_can_use_data is False

    def test_data_protection_flags_missing(self):
        sold_order = SoldOrder.from_api_data({"event_id": "ABC1"})

        assert sold_order.user_can_use_data is None
        assert sold_order.supplier_can_use_data is None
        assert sold_order.world_can_use_data is None

    def test_last_modified_is_a_datetime(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        assert sold_order.last_modified_at == datetime.datetime(
            2026, 2, 24, 2, 9, 38, tzinfo=self.ZULU
        )

    def test_cancelled_order(self, orders_data):
        data = {
            **orders_data[0],
            "seat_cancellation_status": "all",
            "seat_refund_status": "all",
            "last_cancellation_type": "customer",
        }

        sold_order = SoldOrder.from_api_data(data)

        assert sold_order.cancellation_status == "cancelled"
        assert sold_order.seat_cancellation_status == "all"
        assert sold_order.seat_refund_status == "all"
        assert sold_order.last_cancellation_type == "customer"

    def test_order_that_is_not_cancelled(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        assert sold_order.cancellation_status is None
        assert sold_order.seat_cancellation_status == "none"
        assert sold_order.seat_refund_status == "none"

    def test_failed_purchase(self, orders_data):
        data = {
            key: value
            for key, value in orders_data[0].items()
            if not key.startswith(("seat_cancellation", "seat_refund"))
            and not key.startswith(("cancellation_", "last_cancellation"))
            and not key.startswith(("gross_commission", "user_commission"))
        }
        data["purchase_succeeded"] = False

        sold_order = SoldOrder.from_api_data(data)

        assert sold_order.purchase_succeeded is False
        assert sold_order.gross_commission is None
        assert sold_order.user_commission is None
        assert sold_order.cancellation_status is None
        assert sold_order.cancellation_possible is None
        assert sold_order.seat_cancellation_status is None

    def test_exchange_and_gift_card(self, orders_data):
        data = {
            **orders_data[0],
            "has_been_exchanged": True,
            "replacement_trans_id": "U000-000T-0005-LDNX",
            "replacement_item_number": 2,
            "gift_card_issued": True,
            "gift_card_type": "voucher",
            "gift_card_number": "1234",
            "gift_card_value": "25.0000",
            "gift_card_currency": "usd",
            "gift_card_valid_from_iso8601": "2025-12-01T00:00:00Z",
            "gift_card_valid_until_iso8601": "2026-12-01T00:00:00Z",
        }

        sold_order = SoldOrder.from_api_data(data)

        assert sold_order.has_been_exchanged is True
        assert sold_order.replacement_transaction_id == "U000-000T-0005-LDNX"
        assert sold_order.replacement_item_number == 2
        assert sold_order.gift_card_issued is True
        assert sold_order.gift_card_value == "25.0000"
        assert sold_order.gift_card_valid_from == datetime.datetime(
            2025, 12, 1, tzinfo=self.ZULU
        )
        assert sold_order.gift_card_valid_until == datetime.datetime(
            2026, 12, 1, tzinfo=self.ZULU
        )

    def test_purchase_user_details(self, orders_data):
        data = {
            **orders_data[0],
            "purchase_user_details": {
                "user_id": "example-user",
                "sub_user": "00000000-0000-4000-8000-000000000001",
                "real_name": "Groupon USA",
                "is_b2b": True,
                "default_country_code": "us",
            },
        }

        user = SoldOrder.from_api_data(data).purchase_user_details

        assert user.id == "example-user"
        assert user.name == "Groupon USA"
        assert user.is_b2b is True
        assert user.country == "us"

    def test_missing_fields(self):
        sold_order = SoldOrder.from_api_data({"event_id": "ABC1"})

        assert sold_order.transaction_id is None
        assert sold_order.purchased_at is None
        assert sold_order.last_modified_at is None
        assert sold_order.agent_reference is None
        assert sold_order.seat_ids is None
        assert sold_order.total_seatprice is None
        assert sold_order.send_method is None
        assert sold_order.performance.date_time is None
        assert sold_order.performance.name is None
        assert sold_order.gross_commission is None
        assert sold_order.user_commission is None
        assert sold_order.customer is None
        assert sold_order.purchase_user_details is None

    def test_without_customer(self, orders_data):
        assert SoldOrder.from_api_data(orders_data[0]).customer is None

    def test_customer(self, customer_order_data):
        customer = SoldOrder.from_api_data(customer_order_data).customer

        assert customer.first_name == "Jo"
        assert customer.last_name == "Bloggs"
        assert customer.address_lines == ["1 Example Street", "Test Park"]
        assert customer.town == "Testtown"
        assert customer.county == "Testshire"
        assert customer.post_code == "AB1 2CD"
        assert customer.country == "United Kingdom"
        assert customer.country_code == "uk"
        assert customer.email == "jo.bloggs@example.com"
        assert customer.home_phone == "0000000000"
        assert customer.work_phone == "0000000000"
        assert customer.agent_reference == "TP-TEST-0002"

    def test_customer_data_protection_flags(self, customer_order_data):
        customer_order_data["customer"]["user_can_use_customer_data"] = True

        customer = SoldOrder.from_api_data(customer_order_data).customer

        assert customer.user_can_use_data is True
        assert customer.supplier_can_use_data is False
        assert customer.world_can_use_data is False

    def test_customer_does_not_leak_into_the_event(self, customer_order_data):
        sold_order = SoldOrder.from_api_data(customer_order_data)

        assert "customer" not in sold_order.event.raw
        assert sold_order.as_json().count("jo.bloggs@example.com") == 1

    def test_customer_agent_reference_falls_back_to_the_order(self, orders_data):
        data = {**orders_data[0], "customer": {"first_name": "Jo"}}

        customer = SoldOrder.from_api_data(data).customer

        assert customer.agent_reference == "TP-TEST-0001"

    def test_customer_keeps_its_own_agent_reference(self, orders_data):
        data = {
            **orders_data[0],
            "customer": {"first_name": "Jo", "agent_ref": "CUSTOMER-REF"},
        }

        assert SoldOrder.from_api_data(data).customer.agent_reference == "CUSTOMER-REF"

    def test_order_without_gross_commission(self, placeholder_order_data):
        sold_order = SoldOrder.from_api_data(placeholder_order_data)

        assert sold_order.gross_commission is None
        assert sold_order.user_commission.including_vat == 20.9
        assert sold_order.user_commission.excluding_vat == 17.42
        assert sold_order.user_commission.currency_code == "gbp"

    def test_order_with_a_surcharge(self, placeholder_order_data):
        sold_order = SoldOrder.from_api_data(placeholder_order_data)

        assert sold_order.total_seatprice == 130.0
        assert sold_order.total_surcharge == 13.0
        assert sold_order.currency_code == "gbp"

    def test_empty_strings_are_kept(self, placeholder_order_data):
        sold_order = SoldOrder.from_api_data(placeholder_order_data)

        assert sold_order.agent_reference == ""
        assert sold_order.purchase_sub_user == ""
        assert sold_order.customer.agent_reference == ""

    def test_customer_with_placeholder_details(self, placeholder_order_data):
        customer = SoldOrder.from_api_data(placeholder_order_data).customer

        assert customer.address_lines == ["n/a"]
        assert customer.town == "n/a"
        assert customer.post_code == "N A"
        assert customer.county == ""

    def test_event_subdata_is_kept_as_a_string(self, placeholder_order_data):
        sold_order = SoldOrder.from_api_data(placeholder_order_data)

        assert sold_order.event_subdata == '{"is_seated": true, "arr": "1118682"}'

    def test_affiliate_order(self, placeholder_order_data):
        sold_order = SoldOrder.from_api_data(placeholder_order_data)

        assert sold_order.transaction_type == "affiliate"
        assert sold_order.seat_ids == ["B7", "B8"]
        assert sold_order.source_code == "atg_av"
        assert sold_order.event.country_code == "uk"

    def test_order_helpers_with_the_data_a_sold_order_has(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[1])

        # the row has seat IDs, but no per-ticket-order seats or send cost
        assert sold_order.get_seat_ids() == []
        assert sold_order.seat_ids == ["Table 1 Seat 1", "Table 1 Seat 2"]
        with pytest.raises(AssertionError):
            sold_order.total_including_send_cost()

    def test_repr(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        assert repr(sold_order) == "<SoldOrder U000-000T-0001-LDNX>"

    def test_as_json(self, orders_data):
        sold_order = SoldOrder.from_api_data(orders_data[0])

        data = json.loads(sold_order.as_json())

        assert data["agent_reference"] == "TP-TEST-0001"
        assert data["transaction_id"] == "U000-000T-0001-LDNX"
        assert data["event"]["id"] == "1HCUW"
        assert "trolley" not in data
