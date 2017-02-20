from pyticketswitch.callout import Integration, Callout

class TestIntegration:

    def test_from_api_data(self):
        data = {
            "debit_amount": 76.5,
            "debit_base_amount": 7650,
            "debit_currency": "gbp",
            "debitor_specific_data": {
                "is_dummy_3d_secure": False
            },
            "debitor_type": "dummy"
        }

        integration = Integration.from_api_data(data)

        assert integration.amount == 76.5
        assert integration.base_amount == 7650
        assert integration.currency == 'gbp'
        assert integration.type == 'dummy'
        assert integration.data == {
            'is_dummy_3d_secure': False,
        }

class TestCallout:

    def test_from_api_data(self):

        data = {
            'debitor_integration_data': {
                'debitor_type': 'foobar',
            },
            'redirect_html_page_data': 'something something money',
        }

        callout = Callout.from_api_data(data)

        assert callout.integration.type == 'foobar'
        assert callout.html == 'something something money'
