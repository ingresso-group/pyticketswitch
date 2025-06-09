from pyticketswitch.user import User


class TestUser:

    def test_from_api_data(self):

        data = {
            "b2b_attributes": {
                "address": {
                    "addr_line_1": "",
                    "addr_line_2": "",
                    "can_be_edited": True,
                    "country_code": "uk",
                    "county": "",
                    "day_phone": "",
                    "email_addr": "",
                    "eve_phone": "",
                    "town": "",
                },
                "allow_anon_clients": True,
                "has_clients": False,
            },
            "direct_suppliers": [],
            "fixed_codes": {
                "area_codes": [],
                "backend_systems": [],
                "event_codes": [],
                "venue_codes": [],
            },
            "user_groups": [
                {"controllable": True, "group_desc": "Demo product", "group_number": 0}
            ],
            "user_info": {
                "always_force_offline_avail": False,
                "always_mark_as_test": True,
                "always_needs_agent_ref": False,
                "always_needs_email_addr": False,
                "backend_group": "demo_internal_credit_group",
                "can_buy": True,
                "can_login": True,
                "can_report_on_same_owner_code_users": False,
                "can_see_non_pool_perfs": False,
                "content_group": "demo_content_group",
                "contracting_office": "ingresso_uk",
                "custom_from_email_addr": "",
                "default_country_code": "uk",
                "default_lang_code": "",
                "desired_currency": "",
                "is_b2b": True,
                "max_reserve_minutes": 15,
                "owner_code": "",
                "real_name": "Demonstration User",
                "reports_show_cust_data": True,
                "statement_descriptor": "TICKETSWITCH-USER",
                "style": "fixed-tabs",
                "sub_style": "styled-aff-default",
                "sub_sub_style": "b2b-users",
                "sub_user": "pyticketswitch-test",
                "upfront_data_scheme": "",
                "user_id": "demo",
            },
        }

        user = User.from_api_data(data)

        assert user.id == "demo"
        assert user.name == "Demonstration User"
        assert user.country == "uk"
        assert user.sub_user == "pyticketswitch-test"
        assert user.is_b2b is True
        assert user.statement_descriptor == "TICKETSWITCH-USER"
        assert user.backend_group == "demo_internal_credit_group"
        assert user.content_group == "demo_content_group"
