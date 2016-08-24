from pyticketswitch.interface.performance import Performance


class TestPerformance:

    def test_from_api_data(self):

        data = {
            'iso8601_date_and_time': '2016-10-05T14:30:00+01:00',
            'event_id': '25DR',
            'time_desc': '2.30 PM',
            'date_desc': 'Wed, 5th October 2016',
            'is_limited': False,
            'is_ghost': False,
            'perf_id': '25DR-52O',
            'has_pool_seats': True,
            'cached_max_seats': 10,
            'cost_range': {
                'quantity_options': {
                    'valid_quantity_mask': 2046
                },
                'max_surcharge': 11.65,
                'max_seatprice': 59.5,
                'range_currency': {
                    'currency_factor': 100,
                    'currency_places': 2,
                    'currency_post_symbol': '',
                    'currency_number': 826,
                    'currency_pre_symbol': '\xa3',
                    'currency_code': 'gbp'
                },
                'min_surcharge': 11.25,
                'no_singles_cost_range': {
                    'quantity_options': {
                        'valid_quantity_mask': 2046
                    },
                    'max_surcharge': 11.65,
                    'max_seatprice': 69.5,
                    'range_currency': {
                        'currency_factor': 100,
                        'currency_places': 2,
                        'currency_post_symbol': '',
                        'currency_number': 826,
                        'currency_pre_symbol': '\xa3',
                        'currency_code': 'gbp'
                    },
                    'min_surcharge': 11.25,
                    'min_seatprice': 57.5
                },
                'min_seatprice': 57.5
            },
        }

        class FakeEvent(object):
            def __init__(self):
                self.event_id = '25DR'

        event = FakeEvent()
        performance = Performance.from_api_data(data, event)
        assert performance.event.event_id == '25DR'
        assert performance.date_time.year == 2016
        assert performance.date_time.month == 10
        assert performance.date_time.day == 5
        assert performance.date_time.hour == 14
        assert performance.has_pool_seats is True
        assert performance.cached_max_seats == 10
        assert performance.cost_range.max_seatprice == 59.5
        assert performance.no_singles_cost_range.max_seatprice == 69.5
