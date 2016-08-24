from datetime import date, datetime
from dateutil import parser
from pyticketswitch.exceptions import InvalidParametersError


def date_range_str(start_date, end_date):
    if start_date and not isinstance(start_date, date):
        raise InvalidParametersError("start_date is not a datetime instance")
    if end_date and not isinstance(end_date, date):
        raise InvalidParametersError("end_date is not a datetime instance")

    if start_date:
        start_date = start_date.strftime('%Y%m%d')
    else:
        start_date = ''

    if end_date:
        end_date = end_date.strftime('%Y%m%d')
    else:
        end_date = ''

    if start_date or end_date:
        date_range = '{}:{}'.format(start_date, end_date)
    else:
        date_range = ''

    return date_range


def isostr_to_datetime(date_str):
    if not date_str:
        raise ValueError('{} is not a valid datetime string'.format(date_str))

    dt = parser.parse(date_str)
    return dt


def yyyymmdd_to_date(date_str):
    if not date_str:
        raise ValueError('{} is not a valid datetime string'.format(date_str))

    date = datetime.strptime(date_str, '%Y%m%d')
    if date:
        return date.date()


def specific_dates_from_api_data(dates):

    MONTHS = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
        'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
        'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
    }

    return [
        date(int(year.split('_')[1]), MONTHS.get(month), int(day.split('_')[1]))
        for year, months in dates.items()
        if year.startswith('year_')
        for month, days in months.items()
        for day, valid in days.items()
        if valid is True
    ]
