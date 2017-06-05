import datetime

from pyticketswitch.misc import MONTH_NUMBERS
from pyticketswitch.mixins import JSONMixin
from pyticketswitch.utils import bitmask_to_numbered_list


class Month(JSONMixin, object):
    """Availability summary data for a given month

    Attributes:
        month (int): number of the month, jan == 1, feb == 2, dec == 12, etc.
        year (int): year of the month. eg. 2014, 2015, 2016.
        description (str): the human readable description of the month.

    """
    def __init__(self, month, year, description=None, dates_bitmask=None,
                 weekday_bitmask=None):

        self.month = month
        self.year = year
        self.description = description
        self._dates_bitmask = dates_bitmask
        self._weekday_bitmask = weekday_bitmask

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'month': MONTH_NUMBERS.get(data.get('month')),
            'year': data.get('year'),
            'description': data.get('month_desc'),
            'dates_bitmask': data.get('month_dates_bitmask'),
            'weekday_bitmask': data.get('month_weekdays_bitmask'),
        }

        return cls(**kwargs)

    def is_available(self, day):
        """Indicates if the event has availability on a given day.

        the dates bitmask is a 32 bit int where the right most bit is the first
        day of the month. To find if we have availability on a specfic day,
        we bit shift the mask by the zero indexed day and AND it by 1. If the
        result is a 1 then this combo of ticket type and price band is
        available on that day, otherwise it is not.

        Args:
            day (int): the day of the month.

        Returns:
            bool: :obj:`True` there is availability on the given day. Otherwise
            :obj:`False`.
        """

        return bool(self._dates_bitmask >> (day - 1) & 1)

    def on_weekday(self, day):
        """Indicates if the event has availability on a given day of the week.

        Check if the month has shows available on a given day of the week,
        where 0 is monday and sunday is 6.

        .. note:: the api uses sunday as day 0 where as python uses monday.
                  I've made a concious decision here to use the python numbers
                  to keep it consistent with anything written against this.
                  (also a sunday day 0 is silly).

        FIXME: this is copied directly from the AvailabilityDetails class.
        Perhaps worth breaking this out to common base or mixin class?

        Args:
            day (int): the day of the week. monday = 0, tuesday = 1, sunday = 6.

        Returns:
            bool: :obj:`True` there is availability on the given day. Otherwise
            :obj:`False`.

        """
        adjusted_day = day + 1 if day < 6 else 0
        return bool(self._weekday_bitmask >> adjusted_day & 1)

    def start_date(self):
        num_list = bitmask_to_numbered_list(self._dates_bitmask)
        if not num_list:
            return
        first_day = num_list[0]
        howdy = datetime.date(year=self.year, month=self.month, day=first_day)
        return howdy

    def end_date(self):
        num_list = bitmask_to_numbered_list(self._dates_bitmask)
        if not num_list:
            return
        last_day = num_list[-1]
        howdy = datetime.date(year=self.year, month=self.month, day=last_day)
        return howdy
