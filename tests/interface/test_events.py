from pyticketswitch.interface.events import Event
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
        assert event.performance_time is None

        assert event.postcode is None
        assert event.city is None
        assert event.country is None
        assert event.country_code is None
        assert event.latitude is None
        assert event.longditude is None

        assert event.max_running_time is None
        assert event.min_running_time is None

        assert event.has_performances is False
        assert event.is_seated is False
        assert event.needs_departure_date is False
        assert event.needs_duration is False
        assert event.needs_performance is False

        assert event.upsell_list is None
