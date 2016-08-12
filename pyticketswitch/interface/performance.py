from pyticketswitch import utils


class Performance(object):

    def __init__(self, performance_id, event, date_time=None,
                 has_pool_seats=False, is_limited=False,
                 cached_max_seats=None):

        self.performance_id = performance_id
        self.event = event
        self.date_time = date_time
        self.has_pool_seats = has_pool_seats
        self.is_limited = is_limited
        self.cached_max_seats = cached_max_seats

    @classmethod
    def from_api_data(cls, data, event):

        performance_id = data.get('perf_id')

        date_time = data.get('iso8601_date_and_time')
        if date_time:
            utils.isostr_to_datetime(date_time)

        kwargs = {
            'performance_id': performance_id,
            'event': event,
            'date_time': date_time,
            'has_pool_seats': data.get('has_pool_seats', False),
            'is_limited': data.get('is_limited', False),
            'cached_max_seats': data.get('cached_max_seats'),
        }

        return cls(**kwargs)
