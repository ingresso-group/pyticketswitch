import pytest
import datetime
from pyticketswitch.availability import AvailabilityMeta, AvailabilityDetails
from pyticketswitch.currency import Currency


@pytest.fixture
def avail_details():
    kwargs = {
        'ticket_type': 'BALCONY',
        'ticket_type_description': 'Balcony',
        'price_band': 'A',
        'price_band_description': 'AYYY!',
        'seatprice': 47,
        'surcharge': 0,
        'currency': Currency(
            code='gbp',
            factor=100,
            places=2,
            number=826,
            pre_symbol='#',
            post_symbol='',
        ),
        'first_date': datetime.date(2016, 11, 29),
        'last_date': datetime.date(2017, 3, 27),
        'calendar_masks': {
            2016: {
                12: 1065287163,
                11: 805306368
            },
            2017: {
                2: 251526135,
                1: 2012209087,
                3: 117308407
            }
        },
        'weekday_mask': 63,
    }
    details = AvailabilityDetails(**kwargs)
    return details


@pytest.fixture
def data_meta():
    data = {
        "availability": {
            "ticket_type": [
                {
                    "price_band": [
                        {
                            "absolute_saving": 0,
                            "discount_code": "",
                            "discount_desc": "",
                            "is_alloc": False,
                            "is_offer": False,
                            "non_offer_sale_seatprice": 35,
                            "non_offer_sale_surcharge": 4,
                            "number_available": 6,
                            "percentage_saving": 0,
                            "price_band_code": "A",
                            "sale_seatprice": 35,
                            "sale_surcharge": 4,
                        },
                        {
                            "absolute_saving": 0,
                            "discount_code": "",
                            "discount_desc": "",
                            "is_alloc": False,
                            "is_offer": False,
                            "non_offer_sale_seatprice": 25,
                            "non_offer_sale_surcharge": 4,
                            "number_available": 6,
                            "percentage_saving": 0,
                            "price_band_code": "C",
                            "sale_seatprice": 25,
                            "sale_surcharge": 4,
                        }
                    ],
                    "ticket_type_code": "CIRCLE",
                    "ticket_type_desc": "Upper circle"
                },
                {
                    "price_band": [
                        {
                            "absolute_saving": 0,
                            "discount_code": "",
                            "discount_desc": "",
                            "is_alloc": False,
                            "is_offer": False,
                            "non_offer_sale_seatprice": 21,
                            "non_offer_sale_surcharge": 3,
                            "number_available": 6,
                            "percentage_saving": 0,
                            "price_band_code": "A",
                            "sale_seatprice": 21,
                            "sale_surcharge": 3
                        }
                    ],
                    "ticket_type_code": "STALLS",
                    "ticket_type_desc": "Stalls"
                }
            ]
        },
        "backend_is_broken": False,
        "backend_is_down": False,
        "backend_throttle_failed": False,
        "contiguous_seat_selection_only": True,
        "must_select_whole_seat_block": True,
        "currency_code": 'gbp',
        'currency_details': {
            "gbp": {
                "currency_code": "gbp",
            },
        },
        "max_bundle_size": 1,
        "source_code": "BackendCode",
        "valid_quantities": [
            1, 4, 6, 7
        ],
    }

    return data


class TestAvailabilityMeta:

    def test_from_api_data(self, data_meta):
        meta = AvailabilityMeta.from_api_data(data_meta)

        assert meta.contiguous_seat_selection_only is True
        assert meta.must_select_whole_seat_block is True
        assert meta.default_currency_code == 'gbp'
        assert meta.max_bundle_size == 1
        assert meta.valid_quantities == [1, 4, 6, 7]
        assert meta.backend_is_broken is False
        assert meta.backend_is_down is False
        assert meta.backend_throttle_failed is False
        assert meta.source_code == "BackendCode"

    def test_from_api_data_with_backend_issues(self):

        data = {
            'backend_is_broken': True,
            'backend_is_down': True,
            'backend_throttle_failed': True,
        }

        meta = AvailabilityMeta.from_api_data(data)

        assert meta.backend_is_broken is True
        assert meta.backend_is_down is True
        assert meta.backend_throttle_failed is True


class TestAvailabilityDetails:

    def test_from_api_data_flattens_ticket_types_and_price_bands(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                        },
                        {
                            'price_band_code': 'TRG',
                            'price_band_desc': 'Troglodites',
                        }
                    ]
                },
                {
                    'ticket_type_code': 'BAR',
                    'ticket_type_desc': 'Bar',
                    'price_band': [
                        {
                            'price_band_code': 'VIP',
                            'price_band_desc': 'Very Important People',
                        },
                        {
                            'price_band_code': 'CBH',
                            'price_band_desc': 'Chinese Billionaire Heiress',
                        }
                    ]
                }
            ]
        }

        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 4

        assert details[2].ticket_type == 'FOO'
        assert details[2].ticket_type_description == 'Foo'
        assert details[2].price_band == 'PLB'
        assert details[2].price_band_description == 'Plebians'

        assert details[3].ticket_type == 'FOO'
        assert details[3].ticket_type_description == 'Foo'
        assert details[3].price_band == 'TRG'
        assert details[3].price_band_description == 'Troglodites'

        assert details[0].ticket_type == 'BAR'
        assert details[0].ticket_type_description == 'Bar'
        assert details[0].price_band == 'VIP'
        assert details[0].price_band_description == 'Very Important People'

        assert details[1].ticket_type == 'BAR'
        assert details[1].ticket_type_description == 'Bar'
        assert details[1].price_band == 'CBH'
        assert details[1].price_band_description == 'Chinese Billionaire Heiress'

    def test_from_api_data_adds_prices_availability(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'avail_detail': [{
                                'seatprice': 47.0,
                                'surcharge': 6.5,
                                'full_seatprice': 48.0,
                                'full_surcharge': 7.5,
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0].seatprice == 47.0
        assert details[0].surcharge == 6.5
        assert details[0].full_seatprice == 48.0
        assert details[0].full_surcharge == 7.5
        assert details[0].combined_price() == 53.5
        assert details[0].combined_full_price() == 55.5

    def test_from_api_data_adds_currency(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'avail_detail': [{
                                'avail_currency_code': 'gbp',
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0].currency == 'gbp'

    def test_from_api_data_adds_cached_number_available(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'avail_detail': [{
                                'cached_number_available': 4,
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0].cached_number_available == 4

    def test_from_api_data_adds_first_last_dates(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'avail_detail': [{
                                'available_dates': {
                                    'first_yyyymmdd': '20161129',
                                    'last_yyyymmdd': '20170621',
                                }
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0].first_date == datetime.date(2016, 11, 29)
        assert details[0].last_date == datetime.date(2017, 6, 21)

    def test_from_api_data_copes_with_zero_dates(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'avail_detail': [{
                                'available_dates': {
                                    'first_yyyymmdd': '00000000',
                                    'last_yyyymmdd': '00000000',
                                }
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0].first_date is None
        assert details[0].last_date is None

    def test_from_api_data_adds_calendar_masks(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'avail_detail': [{
                                'available_dates': {
                                    'year_2016': {
                                        'dec_bitmask': 1065287163,
                                        'nov_bitmask': 536870912
                                    },
                                    'year_2017': {
                                        'feb_bitmask': 251526135,
                                        'jan_bitmask': 2012209087,
                                        'mar_bitmask': 519961591
                                    }
                                }
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0]._calendar_masks == {
            2016: {
                12: 1065287163,
                11: 536870912
            },
            2017: {
                2: 251526135,
                1: 2012209087,
                3: 519961591
            },
        }

    def test_from_api_data_adds_weekday_masks(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'avail_detail': [{
                                'available_weekdays_bitmask': 63,
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0]._weekday_mask == 63

    def test_from_api_data_adds_valid_quantities(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'avail_detail': [{
                                'valid_quantities': [2, 3, 4],
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0].valid_quantities == [2, 3, 4]

    def test_is_available_with_valid_year(self, avail_details):
        assert avail_details.is_available(2016) is True

    def test_is_available_with_invalid_year(self, avail_details):
        assert avail_details.is_available(2019) is False

    def test_is_available_fails_with_year_and_day_but_not_month(self, avail_details):
        with pytest.raises(ValueError):
            avail_details.is_available(2016, day=23)

    def test_is_available_with_valid_year_month_combo(self, avail_details):
        assert avail_details.is_available(2016, 12) is True

    def test_is_available_with_invalid_year_month_combo(self, avail_details):
        assert avail_details.is_available(2017, 6) is False

    def test_is_available_with_valid_year_month_day_combo(self, avail_details):
        """
        mask is 1065287163 for dec 2016, this is 0b111111011111101111110111111011
        each bit right to left is a day of the month, i.e we have availbility on
        the 1st and 2nd and 4th, but not on the 3rd, 10th or 17th.
        """
        assert avail_details.is_available(2016, 12, 1) is True
        assert avail_details.is_available(2016, 12, 2) is True
        assert avail_details.is_available(2016, 12, 4) is True

    def test_is_available_with_invalid_year_month_day_combo(self, avail_details):
        """
        mask is 1065287163 for dec 2016, this is 0b111111011111101111110111111011
        each bit right to left is a day of the month, i.e we have availbility on
        the 1st and 2nd and 4th, but not on the 3rd, 10th, 17th.
        """
        assert avail_details.is_available(2016, 12, 3) is False
        assert avail_details.is_available(2016, 12, 10) is False
        assert avail_details.is_available(2016, 12, 17) is False

    def test_on_weekday(self):
        """
        mask is 7 bits representing the 7 days of the week. it's read right to
        left with the right most being sunday and the left most being saturday
        """
        # 23 = 0b10111 (VALID = sun, mon, tues, thurs; INVALID = wed, fri, sat)
        details = AvailabilityDetails(weekday_mask=23)

        # 0 is monday
        assert details.on_weekday(0) is True
        # 1 is tuesday
        assert details.on_weekday(1) is True
        # 2 is wednesday
        assert details.on_weekday(2) is False
        # 3 is thursday
        assert details.on_weekday(3) is True
        # 4 is friday
        assert details.on_weekday(4) is False
        # 5 is saturday
        assert details.on_weekday(5) is False
        # 6 is sunday
        assert details.on_weekday(6) is True
