import pytest
import datetime
from pyticketswitch.interface.availability import AvailabilityMeta, AvailabilityDetails
from pyticketswitch.interface.currency import Currency


@pytest.fixture
def data_details():
    return {
        'ticket_type': [
            {
                'price_band': [
                    {
                        'price_band_code': 'A',
                        'price_band_desc': 'AYYY!',
                        'avail_detail': [
                            {
                                'available_weekdays_bitmask': 63,
                                'seatprice': 47,
                                'surcharge': 0,
                                'available_dates': {
                                    'last_yyyymmdd': '20170327',
                                    'first_yyyymmdd': '20161129',
                                    'year_2016': {
                                        'nov_bitmask': 805306368,
                                        'dec_bitmask': 1065287163
                                    },
                                    'year_2017': {
                                        'feb_bitmask': 251526135,
                                        'mar_bitmask': 117308407,
                                        'jan_bitmask': 2012209087
                                    }
                                },
                                'quantity_options': {
                                    'valid_quantity_bitmask': 126
                                },
                                'avail_currency': {
                                    'currency_factor': 100,
                                    'currency_number': 826,
                                    'currency_code': 'gbp',
                                    'currency_pre_symbol': '#',
                                    'currency_places': 2,
                                    'currency_post_symbol': ''
                                }
                            }
                        ]
                    }
                ],
                'ticket_type_code': 'BALCONY',
                'ticket_type_desc': 'Balcony'
            },
            {
                'price_band': [
                    {
                        'price_band_code': 'A',
                        'price_band_desc': 'AYYY!',
                        'avail_detail': [
                            {
                                'available_weekdays_bitmask': 63,
                                'seatprice': 35,
                                'surcharge': 0,
                                'available_dates': {
                                    'last_yyyymmdd': '20170327',
                                    'first_yyyymmdd': '20161129',
                                    'year_2016': {
                                        'nov_bitmask': 805306368,
                                        'dec_bitmask': 1065287163
                                    },
                                    'year_2017': {
                                        'feb_bitmask': 251526135,
                                        'mar_bitmask': 117308407,
                                        'jan_bitmask': 2012209087
                                    }
                                },
                                'quantity_options': {
                                    'valid_quantity_bitmask': 126
                                },
                                'avail_currency': {
                                    'currency_factor': 100,
                                    'currency_number': 826,
                                    'currency_code': 'gbp',
                                    'currency_pre_symbol': '#',
                                    'currency_places': 2,
                                    'currency_post_symbol': ''
                                }
                            }
                        ]
                    },
                    {
                        'price_band_code': 'B',
                        'price_band_desc': 'BEE!',
                        'avail_detail': [
                            {
                                'available_weekdays_bitmask': 63,
                                'seatprice': 30,
                                'surcharge': 0,
                                'available_dates': {
                                    'last_yyyymmdd': '20170327',
                                    'first_yyyymmdd': '20161129',
                                    'year_2016': {
                                        'nov_bitmask': 805306368,
                                        'dec_bitmask': 1065287163
                                    },
                                    'year_2017': {
                                        'feb_bitmask': 251526135,
                                        'mar_bitmask': 117308407,
                                        'jan_bitmask': 2012209087
                                    }
                                },
                                'quantity_options': {
                                    'valid_quantity_bitmask': 126
                                },
                                'avail_currency': {
                                    'currency_factor': 100,
                                    'currency_number': 826,
                                    'currency_code': 'gbp',
                                    'currency_pre_symbol': '#',
                                    'currency_places': 2,
                                    'currency_post_symbol': ''
                                }
                            }
                        ]
                    },
                    {
                        'price_band_code': 'C',
                        'price_band_desc': 'SEE!',
                        'avail_detail': [
                            {
                                'available_weekdays_bitmask': 63,
                                'seatprice': 25,
                                'surcharge': 0,
                                'available_dates': {
                                    'last_yyyymmdd': '20170327',
                                    'first_yyyymmdd': '20161129',
                                    'year_2016': {
                                        'nov_bitmask': 805306368,
                                        'dec_bitmask': 1065287163
                                    },
                                    'year_2017': {
                                        'feb_bitmask': 251526135,
                                        'mar_bitmask': 117308407,
                                        'jan_bitmask': 2012209087
                                    }
                                },
                                'quantity_options': {
                                    'valid_quantity_bitmask': 126
                                },
                                'avail_currency': {
                                    'currency_factor': 100,
                                    'currency_number': 826,
                                    'currency_code': 'gbp',
                                    'currency_pre_symbol': '#',
                                    'currency_places': 2,
                                    'currency_post_symbol': ''
                                }
                            }
                        ]
                    }
                ],
                'ticket_type_code': 'CIRCLE',
                'ticket_type_desc': 'Upper circle'
            },
            {
                'price_band': [
                    {
                        'price_band_code': 'A',
                        'price_band_desc': 'AYYY!',
                        'avail_detail': [
                            {
                                'available_weekdays_bitmask': 63,
                                'seatprice': 21,
                                'surcharge': 0,
                                'available_dates': {
                                    'last_yyyymmdd': '20170327',
                                    'first_yyyymmdd': '20161129',
                                    'year_2016': {
                                        'nov_bitmask': 805306368,
                                        'dec_bitmask': 1065287163
                                    },
                                    'year_2017': {
                                        'feb_bitmask': 251526135,
                                        'mar_bitmask': 117308407,
                                        'jan_bitmask': 2012209087
                                    }
                                },
                                'quantity_options': {
                                    'valid_quantity_bitmask': 126
                                },
                                'avail_currency': {
                                    'currency_factor': 100,
                                    'currency_number': 826,
                                    'currency_code': 'gbp',
                                    'currency_pre_symbol': '#',
                                    'currency_places': 2,
                                    'currency_post_symbol': ''
                                }
                            }
                        ]
                    },
                    {
                        'price_band_code': 'B',
                        'price_band_desc': 'BEE!',
                        'avail_detail': [
                            {
                                'available_weekdays_bitmask': 63,
                                'seatprice': 18,
                                'surcharge': 0,
                                'available_dates': {
                                    'last_yyyymmdd': '20170327',
                                    'first_yyyymmdd': '20161129',
                                    'year_2016': {
                                        'nov_bitmask': 805306368,
                                        'dec_bitmask': 1065287163
                                    },
                                    'year_2017': {
                                        'feb_bitmask': 251526135,
                                        'mar_bitmask': 117308407,
                                        'jan_bitmask': 2012209087
                                    }
                                },
                                'quantity_options': {
                                    'valid_quantity_bitmask': 14
                                },
                                'avail_currency': {
                                    'currency_factor': 100,
                                    'currency_number': 826,
                                    'currency_code': 'gbp',
                                    'currency_pre_symbol': '#',
                                    'currency_places': 2,
                                    'currency_post_symbol': ''
                                }
                            }
                        ]
                    }
                ],
                'ticket_type_code': 'STALLS',
                'ticket_type_desc': 'Stalls'
            }
        ]
    }


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
        "can_leave_singles": True,
        "contiguous_seat_selection_only": True,
        "currency": {
            "currency_code": "gbp",
            "currency_factor": 100,
            "currency_number": 826,
            "currency_places": 2,
            "currency_post_symbol": "",
            "currency_pre_symbol": "#"
        },
        "quantity_options": {
            "valid_quantity_flags": [
                False,
                True,
                True,
                True,
                True,
                True,
                True
            ]
        }
    }

    return data


class TestAvailabilityMeta:

    def test_from_api_data(self, data_meta):

        meta = AvailabilityMeta.from_api_data(data_meta)

        assert meta.can_leave_singles is True
        assert meta.contiguous_seat_selection_only is True
        assert meta.currency == Currency(
            'gbp', factor=100, places=2, number=826, post_symbol='',
            pre_symbol='#'
        )
        assert meta.valid_quantities == [2, 3, 4, 5, 6, 7]


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

        assert details[0].ticket_type == 'FOO'
        assert details[0].ticket_type_description == 'Foo'
        assert details[0].price_band == 'PLB'
        assert details[0].price_band_description == 'Plebians'

        assert details[1].ticket_type == 'FOO'
        assert details[1].ticket_type_description == 'Foo'
        assert details[1].price_band == 'TRG'
        assert details[1].price_band_description == 'Troglodites'

        assert details[2].ticket_type == 'BAR'
        assert details[2].ticket_type_description == 'Bar'
        assert details[2].price_band == 'VIP'
        assert details[2].price_band_description == 'Very Important People'

        assert details[3].ticket_type == 'BAR'
        assert details[3].ticket_type_description == 'Bar'
        assert details[3].price_band == 'CBH'
        assert details[3].price_band_description == 'Chinese Billionaire Heiress'

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
                                'avail_currency': {
                                    'currency_code': 'gbp',
                                    'currency_factor': 100,
                                    'currency_number': 826,
                                    'currency_places': 2,
                                    'currency_post_symbol': 'GBP',
                                    'currency_pre_symbol': '#'
                                },
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0].currency.code == 'gbp'
        assert details[0].currency.factor == 100
        assert details[0].currency.number == 826
        assert details[0].currency.places ==2
        assert details[0].currency.post_symbol == 'GBP'
        assert details[0].currency.pre_symbol =='#'

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
                'dec': 1065287163,
                'nov': 536870912
            },
            2017: {
                'feb': 251526135,
                'jan': 2012209087,
                'mar': 519961591
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
                                'valid_quantity_bitmask': 14,
                            }],
                        },
                    ]
                },
            ],
        }
        details = AvailabilityDetails.from_api_data(data)
        assert len(details) == 1

        assert details[0].valid_quanities == [2, 3, 4]
