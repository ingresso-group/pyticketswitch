from pyticketswitch.debitor import Debitor


class TestDebitor:

    def test_from_api_data(self):

        data = {
            "debitor_desc": "Stripe",
            "debitor_integration_data": {
                'publishable_key': 'abc123',
            },
            "debitor_name": "stripe_gbp",
            "debitor_type": "stripe",
            "debitor_aggregation_key": "abcd1234"
        }

        debitor = Debitor.from_api_data(data)

        assert debitor.type == 'stripe'
        assert debitor.name == 'stripe_gbp'
        assert debitor.description == 'Stripe'
        assert debitor.integration_data == {
            'publishable_key': 'abc123',
        }
        assert debitor.aggregation_key == 'abcd1234'
