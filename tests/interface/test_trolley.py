from pyticketswitch.interface.trolley import Trolley


class TestTrolley:

    def test_from_api_data(self):
        data = {
            'discarded_orders': [
                {'item_number': 3},
                {'item_number': 6},
            ],

            'trolley_contents': {
                'bundle': [
                    {'bundle_source_code': 'foo'},
                    {'bundle_source_code': 'bar'},
                ]
            },
            'trolley_token': 'ABC123',
        }

        trolley = Trolley.from_api_data(data)

        assert trolley.token == 'ABC123'

        assert len(trolley.bundles) == 2
        assert trolley.bundles[0].source_code == 'foo'
        assert trolley.bundles[1].source_code == 'bar'

        assert len(trolley.discarded_orders) == 2
        assert trolley.discarded_orders[0].item == 3
        assert trolley.discarded_orders[1].item == 6
