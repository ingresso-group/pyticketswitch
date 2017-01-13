from pyticketswitch.currency import Currency
from pyticketswitch.bundle import Bundle
from pyticketswitch.event import Event
from pyticketswitch.order import Order


class TestBundle(object):
    def test_from_api_data(self):
        data = {
            'bundle_order_count': 1,
            'bundle_source_code': 'ext_test0',
            'bundle_source_desc': 'External Test Backend 0',
            'bundle_total_cost': 54.7,
            'bundle_total_seatprice': 51,
            'bundle_total_send_cost': 1.5,
            'bundle_total_surcharge': 2.2,
            'currency': {'currency_code': 'gbp'},
            'order': [
                {'item_number': 1},
                {'item_number': 2},
            ]
        }

        bundle = Bundle.from_api_data(data)

        assert bundle.source_code == 'ext_test0'
        assert len(bundle.orders) == 2
        assert bundle.orders[0].item == 1
        assert bundle.orders[1].item == 2
        assert bundle.description == 'External Test Backend 0'

        assert isinstance(bundle.total_seatprice, float)
        assert bundle.total_seatprice == 51.0

        assert isinstance(bundle.total_surcharge, float)
        assert bundle.total_surcharge == 2.2

        assert isinstance(bundle.total_send_cost, float)
        assert bundle.total_send_cost == 1.5

        assert isinstance(bundle.total, float)
        assert bundle.total == 54.7

        assert isinstance(bundle.currency, Currency)
        assert bundle.currency.code == 'gbp'

    def test_get_events(self):

        event_one = Event(id_='abc123')
        event_two = Event(id_='def456')

        bundle = Bundle(
            'tests',
            orders=[
                Order(item=1, event=event_one),
                Order(item=2, event=event_two),
            ]
        )

        events = bundle.get_events()

        assert events == [event_one, event_two]

    def test_get_events_with_no_orders(self):

        bundle = Bundle('tests', orders=None)

        events = bundle.get_events()

        assert events == []

    def test_get_event_ids(self):
        event_one = Event(id_='abc123')
        event_two = Event(id_='def456')

        bundle = Bundle(
            'tests',
            orders=[
                Order(item=1, event=event_one),
                Order(item=2, event=event_two),
            ]
        )

        events = bundle.get_event_ids()

        assert events == {'abc123', 'def456'}
