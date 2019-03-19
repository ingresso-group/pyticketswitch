import functools
import warnings

from datetime import date, datetime
from dateutil import parser
from decimal import Decimal
from pyticketswitch.exceptions import InvalidParametersError


def date_range_str(start_date, end_date):
    """Convert a set of dates to string readable by the API

    Args:
        start_date (datetime.date): the start of the date range.
        end_date (datetime.date): the end of the date range.

    Returns:
        str: a date range in the format of "YYYYMMDD:YYYYMMDD".

        Missing either or both dates is acceptable and will return
        "YYYYMMDD:", ":YYYYMMDD", ":".

    Raises:
        InvalidParametersError: when a start_date or end_date is specified and
            it is not a datetime.date object.

    """
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
    """Convert an iso datetime string to a :py:class:`datetime.datetime` object.

    Args:
        date_str (str): the string to convert.

    Returns:
        :py:class:`datetime.datetime`: the python representation of the date
            and time.

    Raises:
        ValueError: when the date_str is empty or None.

    """
    if not date_str:
        raise ValueError('{} is not a valid datetime string'.format(date_str))

    dt = parser.parse(date_str)
    return dt


def yyyymmdd_to_date(date_str):
    """Convert a YYYYMMDDD formated date to python :py:class:`datetime.date` object.

    Args:
        date_str (str): the string to convert.

    Returns:
        :py:class:`datetime.date`: the python representation of the date.

    Raises:
        ValueError: when the date_str is empty or None.
    """
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


def bitmask_to_boolean_list(mask):
    """Convert a bitmask to boolean list

    Args:
        mask (int): the mask returned by the API

    Returns:
        list: list of booleans.

    """
    of_length = max(1, mask.bit_length())
    return [
        bool(mask >> i & 1)
        for i in range(of_length)
    ]


def bitmask_to_numbered_list(mask):
    """Convert a bitmask to a numbered list

    Args:
        mask (int): the mask returned by the API

    Returns:
        list: list of integers

    """
    if mask is None:
        return []

    return [
        i+1
        for i in range(mask.bit_length() + 1)
        if bool(mask >> i & 1)
    ]


def get_price(data, key):
    """Extracts a price as a float from some data

    Args:
        data (dict): the data containing the price
        key (str): the key of the target price.

    Returns:
        float: the price as a float.

        When the dictionary is missing the requested key, returns :obj:`None`
    """

    price = data.get(key)
    if price is not None:
        price = float(price)

    return price


def add_prices(*prices):
    """Adds two or more prices together

    Args:
        *prices: Prices to add together. They, can be a
            :py:class:`float`, :py:class:`int`,
            :py:class:`Decimal <decimal.Decimal>` or :py:class:`str`

    Returns:
        :class:`Decimal <decimal.Decimal>`, str, float or int.
        The sum of the prices, using the most specific of these types that
        is used in the input arguments, where specificity is in the order

        - :py:class:`Decimal <decimal.Decimal>`
        - :py:class:`str`
        - :py:class:`float`
        - :py:class:`int`


    Raises:
        TypeError: when fewer than 2 prices are provided
        decimal.InvalidOperation: when the string representation
            of an argument cannot be parsed as a decimal
    """
    if len(prices) < 2:
        raise TypeError(
            'add_prices expected at least 2 arguments, got {}'.format(len(prices))
        )
    converted = [
        Decimal(str(price)) if price is not None else None
        for price in prices
    ]
    combined = sum(converted)
    if any(isinstance(price, Decimal) for price in prices):
        return Decimal(combined)
    if any(isinstance(price, str) for price in prices):
        return str(combined)
    if any(isinstance(price, float) for price in prices):
        return float(combined)
    return int(combined)


def filter_none_from_parameters(params):
    """Removes parameters whos value is :obj:None

    Args:
        params (dict): dictionary of parameters to be passed to the API.

    Returns:
        dict: the original parameters with any parameters whos value was
        :obj:`None` removed.

    """
    return {
        key: value
        for key, value in params.items()
        if value is not None
    }


def deprecation_warning(message, stacklevel=2):
    warnings.simplefilter('always', DeprecationWarning)  # turn off filter
    warnings.warn(message,
                  category=DeprecationWarning,
                  stacklevel=stacklevel)
    warnings.simplefilter('default', DeprecationWarning)  # reset filter


def deprecated(func):
    """Mark a function as deprecated and raise a warning

    This decorator is used to mark functions as deprecated. It will result in
    a warning being emitted when the function is called.

    Args:
        func: the function to be wrapped

    Returns:
        the wrapped function that raises a warning
    """

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        deprecation_warning(
            "Call to deprecated function {}".format(func.__name__)
        )
        return func(*args, **kwargs)

    # Mark the function as deprecated
    wrapped_func.is_deprecated = True
    return wrapped_func
