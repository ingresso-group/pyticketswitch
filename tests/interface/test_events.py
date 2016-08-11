import pytest
from pyticketswitch import exceptions
from pyticketswitch.interface.event import Event
from datetime import datetime
from dateutil.tz import tzoffset


class TestEvent:

    BST = tzoffset('BST', 3600)
    DRC = tzoffset('DRC', 7200)

    def test_from_api_data(self):
        data = {
            'event_id': 'ABC1',
            'event_status': 'live',
            'event_type': 'simple_ticket',
            'source_desc': 'Super Awesome Ticketer',
            'venue_desc': 'Top Notch Theater',

            'class': [
                {'class_desc': 'Theater'},
                {'class_desc': 'Amazeballs'},
            ],

            #TODO: don't actually know what filters look like yet...
            'filters': [],

            'date_range_start': {
                'iso8601_date_and_time': '2016-07-21T23:57:15+01:00',
            },
            'date_range_end': {
                'iso8601_date_and_time': '2017-09-03T11:30:40+02:00',
            },

            'postcode': 'W6 8DL',
            'city_desc': 'London',
            'country_desc': 'United Kingdom',
            'country_code': 'uk',

            'geo_data': {
                'latitude': 51.49691253,
                'longditude': -0.17223274,
            },

            'max_running_time': 120,
            'min_running_time': 90,

            'has_no_perfs': True,
            'show_perf_time': True,
            'is_seated': True,
            'needs_departure_date': True,
            'needs_duration': True,
            'needs_performance': True,

            'event_upsell_list': {
                'event_id': ['DEF2', 'GHI3', 'JKL4'],
            },
            'cost_range': {
                'quantity_options': {
                    'valid_quantity_mask': '2046'
                },
                'max_surcharge': 29.65,
                'max_seatprice': 149.5,
                'range_currency': {
                    'currency_factor': 100,
                    'currency_places': 2,
                    'currency_post_symbol': '',
                    'currency_number': 826,
                    'currency_pre_symbol': '\xa3',
                    'currency_code': 'gbp'
                },
                'min_surcharge': 7.25,
                'no_singles_cost_range': {
                    'quantity_options': {
                        'valid_quantity_mask': '2046'
                    },
                    'max_surcharge': 29.65,
                    'max_seatprice': 149.5,
                    'range_currency': {
                        'currency_factor': 100,
                        'currency_places': 2,
                        'currency_post_symbol': '',
                        'currency_number': 826,
                        'currency_pre_symbol': '\xa3',
                        'currency_code': 'gbp'
                    },
                    'min_surcharge': 7.25,
                    'min_seatprice': 37.5
                },
                'min_seatprice': 37.5
            },

        }

        event = Event.from_api_data(data)
        assert event.event_id is 'ABC1'
        assert event.status == 'live'

        assert event.description is None

        assert event.source == 'Super Awesome Ticketer'
        assert event.event_type == 'simple_ticket'
        assert event.venue == 'Top Notch Theater'

        assert event.classes == ['Theater', 'Amazeballs']
        assert event.filters == []

        assert event.start_date == datetime(2016, 7, 21, 23, 57, 15, tzinfo=self.BST)
        assert event.end_date == datetime(2017, 9, 3, 11, 30, 40, tzinfo=self.DRC)

        assert event.postcode == 'W6 8DL'
        assert event.city == 'London'
        assert event.country == 'United Kingdom'
        assert event.country_code == 'uk'
        assert event.latitude == 51.49691253
        assert event.longditude == -0.17223274

        assert event.max_running_time == 120
        assert event.min_running_time == 90

        assert event.show_performance_time is True
        assert event.has_performances is False
        assert event.is_seated is True
        assert event.needs_departure_date is True
        assert event.needs_duration is True
        assert event.needs_performance is True

        assert event.upsell_list == ['DEF2', 'GHI3', 'JKL4']

    def test_from_api_data_with_no_event_id(self):
        data = {
            'foo': 'bar',
        }

        with pytest.raises(exceptions.IntegrityError):
            Event.from_api_data(data)

    def test_from_api_data_with_has_no_perfs(self):
        data = {
            'event_id': 'ABC1',
            'has_no_perfs': True,
        }

        event = Event.from_api_data(data)

        assert event.has_performances is False
