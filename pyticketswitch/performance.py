from pyticketswitch import utils
from pyticketswitch.cost_range import CostRange
from pyticketswitch.availability import AvailabilityDetails
from pyticketswitch.mixins import JSONMixin


class Performance(JSONMixin, object):

    def __init__(self, id_, event_id, date_time=None,
                 date_desc=None, time_desc=None, required_info=None,
                 has_pool_seats=False, is_limited=False,
                 cached_max_seats=None, cost_range=None,
                 no_singles_cost_range=None, is_ghost=False, name=None,
                 running_time=None, availability_details=None):

        self.id = id_
        self.event_id = event_id
        self.date_time = date_time
        self.date_desc = date_desc
        self.time_desc = time_desc
        self.required_info = required_info
        self.has_pool_seats = has_pool_seats
        self.is_limited = is_limited
        self.cached_max_seats = cached_max_seats
        self.cost_range = cost_range
        self.no_singles_cost_range = no_singles_cost_range
        self.is_ghost = is_ghost
        self.name = name
        self.running_time = running_time
        self.availability_details = availability_details

    @classmethod
    def from_api_data(cls, data):

        id_ = data.get('perf_id')
        event_id = data.get('event_id')

        date_time = data.get('iso8601_date_and_time')
        if date_time:
            date_time = utils.isostr_to_datetime(date_time)

        date_desc = data.get('date_desc')
        time_desc = data.get('time_desc')
        required_info = data.get('required_info')

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

        availability_details = AvailabilityDetails.from_api_data(
            data.get('avail_details', {}))

        kwargs = {
            'id_': id_,
            'event_id': event_id,
            'date_time': date_time,
            'date_desc': date_desc,
            'time_desc': time_desc,
            'required_info': required_info,
            'running_time': data.get('running_time'),
            'name': data.get('perf_name'),
            'has_pool_seats': data.get('has_pool_seats', False),
            'is_limited': data.get('is_limited', False),
            'is_ghost': data.get('is_ghost', False),
            'cached_max_seats': data.get('cached_max_seats'),
            'cost_range': cost_range,
            'no_singles_cost_range': no_singles_cost_range,
            'availability_details': availability_details,
        }

        return cls(**kwargs)
