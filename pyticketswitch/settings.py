# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

API_URL = 'https://www.tsd-aff.com/cgi-bin/xml_core.exe'

DATE_SLUG_MAP = (
    {
        'slug': 'today',
        'auto_date': 'today_only',
    },
    {
        'slug': 'this-week',
        'auto_date': 'next_week',
    }
)

AUTO_DATE_RANGE = (
    'today_only', 'this_weekend', 'next_week',
    'this_month', 'next_month',
)

NO_TIME_DESCR = 'Select'

DEFAULT_CONCESSION_DESCR = 'Standard'

SMALL_IMAGE = 'square'
MEDIUM_IMAGE = 'landscape'
LARGE_IMAGE = 'triplet_one'
LARGE_IMAGE_TWO = 'triplet_two'
LARGE_IMAGE_THREE = 'triplet_three'
LARGE_IMAGE_FOUR = 'triplet_four'
LARGE_IMAGE_FIVE = 'triplet_five'
MARQUEE_IMAGE = 'marquee'
SEATING_IMAGE = 'seating_plan'
SUPPLIER_IMAGE = 'supplier'

REQUEST_MEDIA = [
    SMALL_IMAGE, MEDIUM_IMAGE, LARGE_IMAGE, LARGE_IMAGE_TWO,
    LARGE_IMAGE_THREE, LARGE_IMAGE_FOUR, LARGE_IMAGE_FIVE,
    MARQUEE_IMAGE, SEATING_IMAGE, SUPPLIER_IMAGE,
]

LARGE_IMAGE_LIST = [
    LARGE_IMAGE, LARGE_IMAGE_TWO, LARGE_IMAGE_THREE,
    LARGE_IMAGE_FOUR, LARGE_IMAGE_FIVE,
]

# timeout in seconds for API requests
API_REQUEST_TIMEOUT = 120
