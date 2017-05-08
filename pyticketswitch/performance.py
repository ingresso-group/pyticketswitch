from pyticketswitch import utils
from pyticketswitch.cost_range import CostRange
from pyticketswitch.availability import AvailabilityDetails
from pyticketswitch.mixins import JSONMixin, PaginationMixin
from pyticketswitch.currency import CurrencyMeta


class Performance(JSONMixin, object):
    """Describes and occurance of an :class:`Event <pyticketswitch.event.Event>`.

    The performance will have either a **date_time** or a **name**.

    .. note:: The **date_time** field is a timezone aware datetime and it is
              localised for the venue and not the user.

    Attributes:
        id (str): identifier for the performance.
        event_id (str): identifier for the event.
        date_time (:obj:`datetime.datetime`): the localised date and time for
            the performance.
        date_description (str): a human readable description of the date of the
            performance.
        time_description (str): a human readable description of the time of the
            performance.
        has_pool_seats (bool): the performance has pool seats available.
        is_limited (bool): the performance has limited availability.
        cached_max_seats (int): the maximum number of seats available to book
            in a single order. This value is cached and may not be accurate.
        cost_range (:class:`CostRange <pyticketswitch.cost_range.CostRange>`):
            pricing summary, may also include offers.
        no_singles_cost_range (:class:`CostRange <pyticketswitch.cost_range.CostRange>`):
            pricing summary when no leaving single seats, may also include
            offers.
        is_ghost (bool): the performance is a ghost performance and is nolonger
            available.
        name (str): the name of the performance.
        running_time (int): the number of minutes the performance is expected
            to run for.
        availability_details (:class:`AvailabilityDetails <pyticketswitch.availability.AvailabilityDetails>`):
            summerised availability data for the performance. This data is
            cached from previous availability calls and may not be accurate.

    """

    def __init__(self, id_, event_id, date_time=None,
                 date_description=None, time_description=None, has_pool_seats=False,
                 is_limited=False, cached_max_seats=None, cost_range=None,
                 no_singles_cost_range=None, is_ghost=False, name=None,
                 running_time=None, availability_details=None):

        self.id = id_
        self.event_id = event_id
        self.date_time = date_time
        self.date_description = date_description
        self.time_description = time_description
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
        """Creates a new **Performance** object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a performance.

        Returns:
            :class:`Performance <pyticketswitch.order.Performance>`: a new
            :class:`Performance <pyticketswitch.order.Performance>` object
            populated with the data from the api.

        """
        id_ = data.get('perf_id')
        event_id = data.get('event_id')

        date_time = data.get('iso8601_date_and_time')
        if date_time:
            date_time = utils.isostr_to_datetime(date_time)

        date_desc = data.get('date_desc')
        time_desc = data.get('time_desc')

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
            'date_description': date_desc,
            'time_description': time_desc,
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

    def __repr__(self):
        if self.date_time:
            return u'<Performance {}: {}>'.format(self.id, self.date_time.isoformat())
        return u'<Performance {}>'.format(self.id)


class PerformanceMeta(PaginationMixin, CurrencyMeta, object):
    """
    PerformanceMeta contains meta information about a list of
    :class:`Performances <pyticketswitch.performance.Performance>`.

    Attributes:
        auto_select (bool): indicates that the performance list will contain
            only one performance and this performance should be automatically
            selected for the customer.
        has_names: (bool): indicates that the related performances have names
    """

    def __init__(self, auto_select=False, has_names=False, *args, **kwargs):
        self.auto_select = auto_select
        self.has_names = has_names
        super(PerformanceMeta, self).__init__(*args, **kwargs)

    @classmethod
    def from_api_data(cls, data):
        """Creates a new **PerformanceMeta** object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns some performance meta data.

        Returns:
            :class:`PerformanceMeta <pyticketswitch.order.PerformanceMeta>`: a
            new :class:`PerformanceMeta <pyticketswitch.order.PerformanceMeta>`
            object populated with the data from the api.

        """
        inst = super(PerformanceMeta, cls).from_api_data(data)
        inst.auto_select = data.get('autoselect_this_performance', False)
        inst.has_names = data.get('results', {}).get('has_perf_names', False)

        return inst
