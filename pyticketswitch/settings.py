API_URL = 'https://www.tsd-aff.com/cgi-bin/xml_core.exe'
EXT_START_SESSION_URL = 'http://www.tsd-aff.com/cgi-bin/xml_start_session.exe'

TEST_USERNAME = ''
TEST_PASSWORD = ''

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

REQUEST_MEDIA = [
    'square', 'landscape', 'marquee', 'triplet_one',
    'triplet_two', 'triplet_three', 'seating_plan',
    'supplier',
]

NO_TIME_DESCR = 'Select'

DEFAULT_CONCESSION_DESCR = 'Standard'

SMALL_IMAGE = 'square'
MEDIUM_IMAGE = 'landscape'
LARGE_IMAGE = 'triplet_one'
LARGE_IMAGE_TWO = 'triplet_two'
LARGE_IMAGE_THREE = 'triplet_three'
MARQUEE_IMAGE = 'marquee'
SEATING_IMAGE = 'seating_plan'
SUPPLIER_IMAGE = 'supplier'

# timeout in seconds for API requests
API_REQUEST_TIMEOUT = 120
