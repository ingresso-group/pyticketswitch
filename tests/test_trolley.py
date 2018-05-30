from pyticketswitch.trolley import Trolley
from pyticketswitch.bundle import Bundle
from pyticketswitch.event import Event
from pyticketswitch.order import Order


class TestTrolley:

    def test_from_api_data_with_trolley_data(self):
        data = {
            'discarded_orders': [
                {'item_number': 3},
                {'item_number': 6},
            ],

            'trolley_contents': {
                'bundle': [
                    {'bundle_source_code': 'foo'},
                    {'bundle_source_code': 'bar'},
                ],
                "purchase_result": {'success': True},
            },
            'trolley_token': 'ABC123',
            'trolley_order_count': 8,
        }

        trolley = Trolley.from_api_data(data)

        assert trolley.token == 'ABC123'

        assert len(trolley.bundles) == 2
        assert trolley.bundles[0].source_code == 'foo'
        assert trolley.bundles[1].source_code == 'bar'

        assert len(trolley.discarded_orders) == 2
        assert trolley.discarded_orders[0].item == 3
        assert trolley.discarded_orders[1].item == 6
        assert trolley.order_count == 8
        assert trolley.purchase_result.success is True

    def test_from_api_data_with_reservation_data(self):
        data = {
            'discarded_orders': [
                {'item_number': 3},
                {'item_number': 6},
            ],

            'reserved_trolley': {
                'bundle': [
                    {'bundle_source_code': 'foo'},
                    {'bundle_source_code': 'bar'},
                ],
                'transaction_id': 'T1000-0000',
                'transaction_uuid': 'DEF456',
            },
        }

        trolley = Trolley.from_api_data(data)

        assert trolley.transaction_uuid == 'DEF456'
        assert trolley.transaction_id == 'T1000-0000'

        assert len(trolley.bundles) == 2
        assert trolley.bundles[0].source_code == 'foo'
        assert trolley.bundles[1].source_code == 'bar'

        assert len(trolley.discarded_orders) == 2
        assert trolley.discarded_orders[0].item == 3
        assert trolley.discarded_orders[1].item == 6

    def test_from_api_data_with_empty_trolley(self):
        data = {
            "discarded_orders": [],
            "input_contained_unavailable_order": True,
            "trolley_token": "abc123",
            "trolley_token_contents": {
                "trolley_bundle_count": 0,
                "trolley_order_count": 0
            }
        }

        trolley = Trolley.from_api_data(data)

        assert trolley.token == 'abc123'
        assert trolley.input_contained_unavailable_order is True


    def test_get_events(self):

        event_one = Event(id_='abc123')
        event_two = Event(id_='def456')
        event_three = Event(id_='ghi789')
        event_four = Event(id_='jlk012')

        bundle_one = Bundle(
            'tests',
            orders=[
                Order(item=1, event=event_one),
                Order(item=2, event=event_two),
            ]
        )
        bundle_two = Bundle(
            'tests_two',
            orders=[
                Order(item=3, event=event_three),
                Order(item=4, event=event_four),
            ]
        )

        trolley = Trolley(
            bundles=[bundle_one, bundle_two]
        )

        events = trolley.get_events()

        assert events == [event_one, event_two, event_three, event_four]

    def test_get_events_with_no_bundles(self):

        trolley = Trolley(bundles=None)

        events = trolley.get_events()

        assert events == []

    def test_get_event_ids(self):

        event_one = Event(id_='abc123')
        event_two = Event(id_='def456')
        event_three = Event(id_='ghi789')
        event_four = Event(id_='abc123')

        bundle_one = Bundle(
            'tests',
            orders=[
                Order(item=1, event=event_one),
                Order(item=2, event=event_two),
            ]
        )
        bundle_two = Bundle(
            'tests_two',
            orders=[
                Order(item=3, event=event_three),
                Order(item=4, event=event_four),
            ]
        )

        trolley = Trolley(
            bundles=[bundle_one, bundle_two]
        )

        events = trolley.get_event_ids()

        assert events == {'abc123', 'def456', 'ghi789'}

    def test_get_bundle(self):

        # state
        bundle_one = Bundle('tests')
        bundle_two = Bundle('tests_two')
        trolley = Trolley(bundles=[bundle_one, bundle_two])

        # action
        bundle = trolley.get_bundle('tests_two')

        # results
        assert bundle is bundle_two

    def test_get_bundle_when_none(self):

        # state
        trolley = Trolley(bundles=[])

        # action
        bundle = trolley.get_bundle('tests_two')

        # results
        assert bundle is None

    def test_get_bundle_when_no_match(self):

        # state
        bundle_one = Bundle('tests')
        bundle_two = Bundle('tests_two')
        trolley = Trolley(bundles=[bundle_one, bundle_two])

        # action
        bundle = trolley.get_bundle('tests_three')

        # results
        assert bundle is None

    def test_get_item(self):

        #state
        order_one = Order(1)
        order_two = Order(2)
        order_three = Order(3)
        order_four = Order(4)
        bundle_one = Bundle('tests', orders=[order_one, order_three])
        bundle_two = Bundle('tests_two', orders=[order_two, order_four])
        trolley = Trolley(bundles=[bundle_one, bundle_two])

        # results
        order = trolley.get_item(3)
        assert order is order_three

        # results
        order = trolley.get_item(2)
        assert order is order_two

    def test_get_orders(self):

        #state
        order_one = Order(1)
        order_two = Order(2)
        order_three = Order(3)
        order_four = Order(4)
        bundle_one = Bundle('tests', orders=[order_one, order_three])
        bundle_two = Bundle('tests_two', orders=[order_two, order_four])
        trolley = Trolley(bundles=[bundle_one, bundle_two])

        # results
        orders = trolley.get_orders()
        assert orders == [order_one, order_three, order_two, order_four]
