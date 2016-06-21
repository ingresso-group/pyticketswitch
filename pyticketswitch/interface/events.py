from datetime import datetime
from pyticketswitch.exceptions import IntegrityError


class Event(object):

    def __init__(self, event_id, status=None, event_type=None, source=None,
                 venue=None, description=None, postcode=None, classes=None,
                 filters=None, start_date=None, end_date=None,
                 upsell_list=None, city=None, country=None, country_code=None,
                 latitude=None, longditude=None, needs_departure_date=False,
                 needs_duration=False, needs_performance=False,
                 has_performances=False, is_seated=False,
                 performance_time=False, min_running_time=None,
                 max_running_time=None):

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
        self.performance_time = performance_time

        self.postcode = postcode
        self.city = city
        self.country = country
        self.country_code = country_code
        self.latitude = latitude
        self.longditude = longditude

        self.max_running_time = max_running_time
        self.min_running_time = min_running_time

        self.has_performances = has_performances
        self.is_seated = is_seated
        self.needs_departure_date = needs_departure_date
        self.needs_duration = needs_duration
        self.needs_performance = needs_performance

        self.upsell_list = upsell_list

    @classmethod
    def from_json(cls, data):

        event_id = data.get('event_id')

        if not event_id:
            raise IntegrityError("event_id not found in event data", data=data)

        args = {
            'event_id': event_id,
            'status': data.get('event_status'),
            'event_type': data.get('event_type'),
            'source': data.get('source_desc'),
            'venue': data.get('venue_desc'),

            'classes': data.get('class', [])
            'filters': data.get('custom_filer', [])
        }

        return cls(data)
