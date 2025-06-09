import datetime
from dateutil.tz import tzoffset
from pyticketswitch.status import Status
from pyticketswitch.address import Address
from pyticketswitch.trolley import Trolley


class TestStatus:

    ZULU = tzoffset('ZULU', 0)

    def test_from_api_data(self):

        data = {
            "allowed_countries": {
                "ad": "Andorra",
                "ae": "United Arab Emirates",
            },
            "accepted_payment_cards": {
                "amex": "American Express",
                "visa": "Visa"
            },
            "can_edit_address": True,
            "language_list": ["en-gb", "en", "en-us", "nl"],
            "minutes_left_on_reserve": 57.5,
            "needs_agent_reference": True,
            "needs_email_address": True,
            "needs_payment_card": True,
            "supports_billing_address": True,
            "remote_site": 'foobar.example.com',
            "prefilled_address": {
                'addr_line_one': '123 fakestreet',
            },
            "reserve_iso8601_date_and_time": "2016-11-9T18:19:27Z",
            "purchase_iso8601_date_and_time": "2016-11-11T12:34:49Z",
            "transaction_status": "reserved",
            "trolley_contents": {
                "transaction_uuid": "6a2f2e03-08e8-11e7-a86b-d0bf9c45f5c0",
            },
            "reserve_user": {"user_id": "foobar"},
            "pending_callout": {"bundle_source_code": "ext_test0"},
            'customer': {
                "addr_line_one": "Metro Building",
                "addr_line_one_latin": "METRO BUILDING",
                "addr_line_two": "1 Butterwick",
                "addr_line_two_latin": "1 BUTTERWICK",
                "agent_ref": "foobar123",
                "country": "United Kingdom",
                "country_code": "uk",
                "country_latin": "UNITED KINGDOM",
                "county": "London",
                "county_latin": "LONDON",
                "dp_supplier": True,
                "dp_user": True,
                "dp_world": True,
                "email_addr": "tester@gmail.com",
                "first_name": "Test",
                "first_name_latin": "TEST",
                "home_phone": "0203 137 7420",
                "work_phone": "079888888888",
                "phone": "079000000000",
                "initials": "l.o.l",
                "initials_latin": "L.O.L",
                "last_name": "Tester",
                "last_name_latin": "TESTER",
                "postcode": "w6 8dl",
                "postcode_latin": "W6 8DL",
                "suffix": "esq",
                "suffix_latin": "ESQ",
                "title": "rt.hon",
                "title_latin": "RT.HON",
                "town": "Hammersmith",
                "town_latin": "HAMMERSMITH",
            }
        }

        status = Status.from_api_data(data)

        assert status.status == 'reserved'
        assert status.reserved_at == datetime.datetime(2016, 11, 9, 18, 19, 27, tzinfo=self.ZULU)
        assert status.purchased_at == datetime.datetime(2016, 11, 11, 12, 34, 49, tzinfo=self.ZULU)
        assert status.external_sale_page is None
        assert status.languages == ['en-gb', 'en', 'en-us', 'nl']
        assert status.remote_site == 'foobar.example.com'
        assert status.trolley.transaction_uuid == '6a2f2e03-08e8-11e7-a86b-d0bf9c45f5c0'
        # assert status.reserve_user.id == 'foobar'
        assert status.needs_payment_card is True
        assert status.needs_email_address is True
        assert status.needs_agent_reference is True
        assert status.can_edit_address is True
        assert status.minutes_left == 57.5
        assert status.supports_billing_address is True

        assert isinstance(status.prefilled_address, Address)
        assert isinstance(status.trolley, Trolley)

        assert len(status.allowed_countries) == 2
        assert status.allowed_countries[0].code == 'ad'
        assert status.allowed_countries[1].code == 'ae'

        assert len(status.accepted_cards) == 2
        assert any(x.code == 'amex' for x in status.accepted_cards)
        assert any(x.code == 'visa' for x in status.accepted_cards)
        assert any(x.description == 'Visa' for x in status.accepted_cards)
        assert any(x.description == 'American Express' for x in status.accepted_cards)

        assert status.pending_callout.code == 'ext_test0'
