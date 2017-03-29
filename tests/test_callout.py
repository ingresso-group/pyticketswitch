from collections import OrderedDict
from pyticketswitch.callout import Callout


class TestCallout:

    def test_from_api_data(self):

        data = {
            "bundle_source_code": "ext_test0",
            "bundle_source_desc": "External Test Backend 0",
            "bundle_total_cost": 79.5,
            "callout_destination_url": "https://foobar.com",
            "callout_integration_data": {
                "foo": False,
                "bar": True,
                "lol": "beans",
            },
            "callout_parameters": {
                "fours": 4,
                "twos": 222,
                "threes": 33,
                "ones": 1,
            },
            "callout_parameters_order": ['ones', 'twos', 'threes', 'fours'],
            "callout_type": "get",
            "currency_code": "gbp",
            "debitor": {
                "debitor_type": "dummy"
            },
            "return_token": "abc123"
        }

        callout = Callout.from_api_data(data)

        assert callout.code == 'ext_test0'
        assert callout.description == 'External Test Backend 0'
        assert callout.total == 79.5
        assert callout.destination == 'https://foobar.com'
        assert callout.parameters == OrderedDict(
            [
                ('ones', 1),
                ('twos', 222),
                ('threes', 33),
                ('fours', 4),
            ]
        )
        assert callout.integration_data == {
            'foo': False,
            'bar': True,
            'lol': 'beans',
        }
        assert callout.debitor.type == 'dummy'
        assert callout.currency_code == 'gbp'
        assert callout.return_token == 'abc123'
