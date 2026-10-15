from __future__ import annotations

import functools
import warnings
from collections.abc import Callable
from datetime import date, datetime
from decimal import Decimal
from typing import Any, ParamSpec, TypeVar, overload

from dateutil import parser

from pyticketswitch.exceptions import InvalidParametersError

P = ParamSpec("P")
R = TypeVar("R")


def date_range_str(start_date: date | None, end_date: date | None) -> str:
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

    start = start_date.strftime("%Y%m%d") if start_date else ""

    end = end_date.strftime("%Y%m%d") if end_date else ""

    return f"{start}:{end}" if start or end else ""


def isostr_to_datetime(date_str: str | None) -> datetime:
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
        raise ValueError(f"{date_str} is not a valid datetime string")

    return parser.parse(date_str)


def yyyymmdd_to_date(date_str: str) -> date:
    """Convert a YYYYMMDDD formated date to python :py:class:`datetime.date` object.

    Args:
        date_str (str): the string to convert.

    Returns:
        :py:class:`datetime.date`: the python representation of the date.

    Raises:
        ValueError: when the date_str is empty or None.
    """
    if not date_str:
        raise ValueError(f"{date_str} is not a valid datetime string")

    return datetime.strptime(date_str, "%Y%m%d").date()


def specific_dates_from_api_data(dates: dict[str, Any]) -> list[date]:

    MONTHS = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }

    return [
        date(int(year.split("_")[1]), MONTHS[month], int(day.split("_")[1]))
        for year, months in dates.items()
        if year.startswith("year_")
        for month, days in months.items()
        for day, valid in days.items()
        if valid is True
    ]


def bitmask_to_boolean_list(mask: int) -> list[bool]:
    """Convert a bitmask to boolean list

    Args:
        mask (int): the mask returned by the API

    Returns:
        list: list of booleans.

    """
    of_length = max(1, mask.bit_length())
    return [bool(mask >> i & 1) for i in range(of_length)]


def bitmask_to_numbered_list(mask: int | None) -> list[int]:
    """Convert a bitmask to a numbered list

    Args:
        mask (int): the mask returned by the API

    Returns:
        list: list of integers

    """
    if mask is None:
        return []

    return [i + 1 for i in range(mask.bit_length() + 1) if bool(mask >> i & 1)]


def get_price(data: dict[str, Any], key: str) -> float | None:
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


@overload
def add_prices(*prices: float | Decimal) -> float | Decimal: ...


@overload
def add_prices(*prices: float | Decimal | str) -> float | Decimal | str: ...


def add_prices(*prices: float | Decimal | str) -> float | Decimal | str:
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
        raise TypeError(f"add_prices expected at least 2 arguments, got {len(prices)}")
    if any(price is None for price in prices):
        raise TypeError("add_prices does not accept None prices")
    converted = [Decimal(str(price)) for price in prices]
    combined = sum(converted)
    if any(isinstance(price, Decimal) for price in prices):
        return Decimal(combined)
    if any(isinstance(price, str) for price in prices):
        return str(combined)
    if any(isinstance(price, float) for price in prices):
        return float(combined)
    return int(combined)


def filter_none_from_parameters(params: dict[str, Any]) -> dict[str, Any]:
    """Removes parameters whos value is :obj:None

    Args:
        params (dict): dictionary of parameters to be passed to the API.

    Returns:
        dict: the original parameters with any parameters whos value was
        :obj:`None` removed.

    """
    return {key: value for key, value in params.items() if value is not None}


def deprecation_warning(message: str, stacklevel: int = 2) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(message, category=DeprecationWarning, stacklevel=stacklevel)


def deprecated(func: Callable[P, R]) -> Callable[P, R]:
    """Mark a function as deprecated and raise a warning

    This decorator is used to mark functions as deprecated. It will result in
    a warning being emitted when the function is called.

    Args:
        func: the function to be wrapped

    Returns:
        the wrapped function that raises a warning
    """

    @functools.wraps(func)
    def wrapped_func(*args: P.args, **kwargs: P.kwargs) -> R:
        deprecation_warning(f"Call to deprecated function {func.__name__}")
        return func(*args, **kwargs)

    # Mark the function as deprecated
    setattr(wrapped_func, "is_deprecated", True)  # noqa: B010
    return wrapped_func
