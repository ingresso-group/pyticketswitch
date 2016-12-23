from pyticketswitch.misc import MONTH_NUMBERS


class Month(object):

    def __init__(self, month, year, description=None, dates_bitmask=None,
                 weekday_bitmask=None):

        self.month = month
        self.year = year
        self.description = description
        self.dates_bitmask = dates_bitmask
        self.weekday_bitmask = weekday_bitmask

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
        """
        the dates bitmask is a 32 bit int where the right most bit is the first
        day of the month. To find if we have availability on a specfic day,
        we bit shift the mask by the zero indexed day and AND it by 1. If the
        result is a 1 then this combo of ticket type and price band is
        available on that day, otherwise it is not.
        """

        return bool(self.dates_bitmask >> (day - 1) & 1)

    def on_weekday(self, day):
        """
        Check if the month has shows available on a given day of the week,
        where 0 is monday and sunday is 6.

        NOTE: the api uses sunday as day 0 where as python uses monday. I've
        made a concious decision here to use the python numbers to keep it
        consistant with anything written against this. (also a sunday day 0 is
        silly)

        FIXME: this is copied directly from the AvailabilityDetails class.
        Perhaps worth breaking this out to common base or mixin class?
        """
        adjusted_day = day + 1 if day < 6 else 0
        return bool(self.weekday_bitmask >> adjusted_day & 1)
