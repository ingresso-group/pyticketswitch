# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import datetime
import random
import string

import six

from six.moves import range

from . import settings

try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml


__all__ = (
    b'create_xml_from_dict', b'create_dict_from_xml',
    b'create_dict_from_xml_element',
    b'random_string_generator',
    b'format_price', b'format_price_with_symbol',
    b'yyyymmdd_to_date', b'hhmmss_to_time',
    b'date_to_yyyymmdd', b'time_to_hhmmss',
    b'dates_in_range', b'auto_date_to_slug',
    b'slug_to_auto_date', b'resolve_boolean',
    b'to_int_or_none', b'to_int_or_return',
    b'to_float_or_none', b'to_float_summed',
    b'to_float_or_zero'
)


def create_xml_from_dict(root_name, arg_dict):
    """ Create XML from dictionary

    Creates a XML Element Object from a dictionary (with a given 'root')
    Dictionary must be flat or contain only dict or list

    """
    root = xml.Element(root_name)

    return _recur_xml_dict(root, arg_dict)


def _recur_xml_list(root, key, arg_list):
    for value in arg_list:
        if type(value) is dict:
            tmp = xml.SubElement(root, key)
            _recur_xml_dict(tmp, value)
        elif type(value) is list:
            tmp = xml.SubElement(root, key)
            _recur_xml_list(root, key, value)
        elif type(value) is bool:
            if value:
                tmp = xml.SubElement(root, key)
        else:
            tmp = xml.SubElement(root, key)
            try:
                tmp.text = six.text_type(value)
            except:
                tmp.text = value
    return root


def _recur_xml_dict(root, arg_dict):
    for (key, value) in six.iteritems(arg_dict):
        if type(value) is dict:
            tmp = xml.SubElement(root, key)
            _recur_xml_dict(tmp, value)
        elif type(value) is list:
            _recur_xml_list(root, key, value)
        elif type(value) is bool:
            if value:
                tmp = xml.SubElement(root, key)
        else:
            tmp = xml.SubElement(root, key)
            try:
                tmp.text = six.text_type(value)
            except:
                tmp.text = value
    return root


def create_dict_from_xml(xml_string):
    """ Create dictionary from XML

    Creates a dictionary from a string of XML (tag, text becomes key, value).
    Returned dictionary will consist of dictionaries and lists.

    """
    tree = xml.fromstring(xml_string)
    root = xml.Element('root')
    root.append(tree)

    return create_dict_from_xml_element(root)


def _add_xml_elem_to_dict(key, value, ret_dict):
    if key in ret_dict:
        if not isinstance(ret_dict[key], list):
            child_list = [ret_dict[key]]
            ret_dict[key] = child_list
        ret_dict[key].append(value)
    else:
        ret_dict[key] = value
    return ret_dict


def create_dict_from_xml_element(root):
    """

    Creates a dictionary from an XML Element object
    (tag, text becomes key, value).
    Returned dictionary will consist of dictionaries and lists.

    """
    ret_dict = {}

    for child in root:
        if len(list(child)) == 0:
            ret_dict = _add_xml_elem_to_dict(child.tag, child.text, ret_dict)
        else:
            ret_dict = _add_xml_elem_to_dict(
                child.tag, create_dict_from_xml_element(child), ret_dict
            )

    return ret_dict


def dict_ignore_nones(**kwargs):
    return dict((k, v) for k, v in kwargs.items() if v is not None)


def random_string_generator(
    size=20, chars=string.ascii_uppercase + string.digits
):
    return ''.join(random.choice(chars) for x in range(size))


def format_price(price_string):
    return '{:.2f}'.format(float(price_string))


def format_price_with_symbol(price_string, pre_symbol, post_symbol):
    price_and_symbol = [
        pre_symbol,
        format_price(price_string),
        post_symbol
    ]

    price_and_symbol = [x for x in price_and_symbol if x is not None]

    return ''.join(price_and_symbol)


def yyyymmdd_to_date(date_yyyymmdd):
    year = int(date_yyyymmdd[0:4])
    month = int(date_yyyymmdd[4:6])
    day = int(date_yyyymmdd[6:8])

    return datetime.date(year, month, day)


def hhmmss_to_time(time_hhmmss):
    hour = int(time_hhmmss[0:2])
    minute = int(time_hhmmss[2:4])
    sec = int(time_hhmmss[4:6])

    return datetime.time(hour, minute, sec)


def date_to_yyyymmdd(date):
    return date.strftime('%Y%m%d')


def date_to_yyyymmdd_or_none(date):
    if date is None:
        return None
    return date_to_yyyymmdd(date)


def time_to_hhmmss(time):
    return time.strftime('%H%M%S')


def dates_in_range(first_date, last_date):

    dates = []

    delta = last_date - first_date

    for i in range(delta.days + 1):
        dates.append(first_date + datetime.timedelta(days=i))

    return dates


def auto_date_to_slug(auto_date):
    if auto_date:
        slug = None

        for mapping in settings.DATE_SLUG_MAP:
            if auto_date == mapping['auto_date']:
                slug = mapping['slug']

    return slug


def slug_to_auto_date(slug):
    if slug:
        auto_date = None

        for mapping in settings.DATE_SLUG_MAP:
            if slug == mapping['slug']:
                auto_date = mapping['auto_date']

    return auto_date


def resolve_boolean(yes_no_string):
    if yes_no_string:
        if yes_no_string == 'yes':
            return True
        return False
    return None


def boolean_to_yes_no(boolean):
    if boolean is True:
        return 'yes'
    else:
        return 'no'


def to_int_or_none(int_string):
    try:
        return int(int_string)
    except (ValueError, TypeError):
        return None


def to_int_or_return(to_convert):
    try:
        return int(to_convert)
    except ValueError:
        return to_convert


def to_float_or_none(float_string):
    try:
        return float(float_string)
    except (ValueError, TypeError):
        return None


def to_float_summed(*float_strings):
    total = float(0)
    all_none = True
    for fs in float_strings:
        try:
            fl = float(fs)
            all_none = False
        except ValueError:
            fl = float(0)

        total = total + fl

    if all_none:
        return None

    return total


def to_float_or_zero(float_string):
    try:
        return float(float_string)
    except ValueError:
        return float(0)


def day_mask_to_bool_list(day_mask):
    """Converts a day bit mask (used in TSW to represent a boolean value for
    days of the week) into a list of 7 booleans. The first item in the list
    represents the first day of the week.
    """
    bit_str = '{0:07b}'.format(int(day_mask))
    bit_str_list = list(bit_str)
    # Convert each element to a binary integer then convert to bool
    # List is reversed so that the lowest significant bit represents the first
    # day of the week
    bool_list = [bool(int(x)) for x in reversed(bit_str_list)]
    return bool_list
