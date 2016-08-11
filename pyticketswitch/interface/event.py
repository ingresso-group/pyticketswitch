from pyticketswitch.exceptions import IntegrityError
from pyticketswitch.interface.cost_range import CostRange
from pyticketswitch import utils


class Event(object):

    def __init__(self, event_id, status=None, event_type=None, source=None,
                 venue=None, description=None, postcode=None, classes=None,
                 filters=None, start_date=None, end_date=None,
                 upsell_list=None, city=None, country=None, country_code=None,
                 latitude=None, longditude=None, needs_departure_date=False,
                 needs_duration=False, needs_performance=False,
                 has_performances=False, is_seated=False,
                 show_performance_time=False, min_running_time=None,
                 max_running_time=None, cost_range=None,
                 no_singles_cost_range=None):

        self.event_id = event_id
        self.status = status
        self.description = description
        self.source = source
        self.event_type = event_type
        self.venue = venue

        self.classes = classes
        self.filters = filters

        self.start_date = start_date
        self.end_date = end_date

        self.postcode = postcode
        self.city = city
        self.country = country
        self.country_code = country_code
        self.latitude = latitude
        self.longditude = longditude

        self.max_running_time = max_running_time
        self.min_running_time = min_running_time

        self.show_performance_time = show_performance_time
        self.has_performances = has_performances
        self.is_seated = is_seated
        self.needs_departure_date = needs_departure_date
        self.needs_duration = needs_duration
        self.needs_performance = needs_performance

        self.upsell_list = upsell_list

        self.cost_range = cost_range
        self.no_singles_cost_range = no_singles_cost_range

    @classmethod
    def from_api_data(cls, data):

        event_id = data.get('event_id')

        if not event_id:
            raise IntegrityError("event_id not found in event data", data=data)

        start_date = data.get('date_range_start', {}).get('iso8601_date_and_time')
        if start_date:
            start_date = utils.isostr_to_datetime(start_date)

        end_date = data.get('date_range_end', {}).get('iso8601_date_and_time')
        if end_date:
            end_date = utils.isostr_to_datetime(end_date)

        classes = data.get('class', [])
        if classes:
            classes = [
                c.get('class_desc') for c in classes
                if 'class_desc' in c
            ]

        geo_data = data.get('geo_data', {})

        # the raw field 'has_no_perfs' is a negative flag, so I'm inverting it
        has_performances = not data.get('has_no_perfs', False)

        api_cost_range = data.get('cost_range', {})
        api_no_singles_cost_range = api_cost_range.get('no_singles_cost_range', {})
        cost_range = None
        no_singles_cost_range = None

        if api_cost_range:
            api_cost_range['singles'] = True
            cost_range = CostRange.from_api_data(api_cost_range)
        if api_no_singles_cost_range:
            api_no_singles_cost_range['singles'] = False
            no_singles_cost_range = CostRange.from_api_data(
                api_no_singles_cost_range)

        kwargs = {
            'event_id': event_id,
            'status': data.get('event_status'),
            'event_type': data.get('event_type'),
            'source': data.get('source_desc'),
            'venue': data.get('venue_desc'),

            'classes': classes,
            #TODO: don't actually know what filters look like yet...
            'filters': data.get('custom_filter', []),

            'start_date': start_date,
            'end_date': end_date,

            'postcode': data.get('postcode'),
            'city': data.get('city_desc'),
            'country': data.get('country_desc'),
            'country_code': data.get('country_code'),

            'latitude': geo_data.get('latitude'),
            'longditude': geo_data.get('longditude'),

            'max_running_time': data.get('max_running_time'),
            'min_running_time': data.get('min_running_time'),

            'has_performances': has_performances,
            'show_performance_time': data.get('show_perf_time', False),
            'is_seated': data.get('is_seated', False),
            'needs_departure_date': data.get('needs_departure_date', False),
            'needs_duration': data.get('needs_duration', False),
            'needs_performance': data.get('needs_performance', False),

            'upsell_list': data.get('event_upsell_list', {}).get('event_id', []),

            'cost_range': cost_range,
            'no_singles_cost_range': no_singles_cost_range,
        }

        return cls(**kwargs)
