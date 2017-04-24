import datetime
from pyticketswitch.performance import Performance, PerformanceMeta


class TestPerformance:

    def test_from_api_data(self):

        data = {
            'iso8601_date_and_time': '2016-10-05T14:30:00+01:00',
            'event_id': '25DR',
            'time_desc': '2.30 PM',
            'date_desc': 'Wed, 5th October 2016',
            'is_limited': False,
            'is_ghost': False,
            'perf_id': '25DR-52O',
            'perf_name': 'ABC123',
            'has_pool_seats': True,
            'cached_max_seats': 10,
            'running_time': 200,
            'cost_range': {
                'quantity_options': {
                    'valid_quantity_mask': 2046
                },
                'max_surcharge': 11.65,
                'max_seatprice': 59.5,
                'range_currency': {
                    'currency_factor': 100,
                    'currency_places': 2,
                    'currency_post_symbol': '',
                    'currency_number': 826,
                    'currency_pre_symbol': '\xa3',
                    'currency_code': 'gbp'
                },
                'min_surcharge': 11.25,
                'no_singles_cost_range': {
                    'quantity_options': {
                        'valid_quantity_mask': 2046
                    },
                    'max_surcharge': 11.65,
                    'max_seatprice': 69.5,
                    'range_currency': {
                        'currency_factor': 100,
                        'currency_places': 2,
                        'currency_post_symbol': '',
                        'currency_number': 826,
                        'currency_pre_symbol': '\xa3',
                        'currency_code': 'gbp'
                    },
                    'min_surcharge': 11.25,
                    'min_seatprice': 57.5
                },
                'min_seatprice': 57.5
            },
            'avail_details': {
                'ticket_type': [
                    {
                        'price_band': [
                            {
                                'avail_detail': [
                                    {
                                        'avail_currency': {
                                            'currency_code': 'gbp'
                                        },
                                        'cached_number_available': 6,
                                        'quantity_options': {
                                            'valid_quantity_bitmask': 126
                                        },
                                        'seatprice': 47,
                                        'surcharge': 0
                                    }
                                ],
                                'price_band_code': 'A',
                                'price_band_desc': ''
                            }
                        ],
                        'ticket_type_code': 'BALCONY',
                        'ticket_type_desc': 'Balcony'
                    },
                    {
                        'price_band': [
                            {
                                'avail_detail': [
                                    {
                                        'avail_currency': {
                                            'currency_code': 'gbp'
                                        },
                                        'cached_number_available': 6,
                                        'quantity_options': {
                                            'valid_quantity_bitmask': 126
                                        },
                                        'seatprice': 35,
                                        'surcharge': 0
                                    }
                                ],
                                'price_band_code': 'A',
                                'price_band_desc': ''
                            },
                            {
                                'avail_detail': [
                                    {
                                        'avail_currency': {
                                            'currency_code': 'gbp'
                                        },
                                        'cached_number_available': 6,
                                        'quantity_options': {
                                            'valid_quantity_bitmask': 126
                                        },
                                        'seatprice': 30,
                                        'surcharge': 0
                                    }
                                ],
                                'price_band_code': 'B',
                                'price_band_desc': ''
                            },
                            {
                                'avail_detail': [
                                    {
                                        'avail_currency': {
                                            'currency_code': 'gbp'
                                        },
                                        'cached_number_available': 6,
                                        'quantity_options': {
                                            'valid_quantity_bitmask': 126
                                        },
                                        'seatprice': 25,
                                        'surcharge': 0
                                    }
                                ],
                                'price_band_code': 'C',
                                'price_band_desc': ''
                            }
                        ],
                        'ticket_type_code': "CIRCLE",
                        'ticket_type_desc': "Upper circle"
                    },
                    {
                        'price_band': [
                            {
                                'avail_detail': [
                                    {
                                        'avail_currency': {
                                            'currency_code': 'gbp'
                                        },
                                        'cached_number_available': 6,
                                        'quantity_options': {
                                            'valid_quantity_bitmask': 126
                                        },
                                        'seatprice': 21,
                                        'surcharge': 0
                                    }
                                ],
                                'price_band_code': 'A',
                                'price_band_desc': ''
                            },
                            {
                                'avail_detail': [
                                    {
                                        'avail_currency': {
                                            'currency_code': 'gbp'
                                        },
                                        'cached_number_available': 3,
                                        'quantity_options': {
                                            'valid_quantity_bitmask': 14
                                        },
                                        'seatprice': 18,
                                        'surcharge': 0
                                    }
                                ],
                                'price_band_code': 'B',
                                'price_band_desc': ''
                            }
                        ],
                        'ticket_type_code': 'STALLS',
                        'ticket_type_desc': 'Stalls'
                    }
                ]
            }
        }

        performance = Performance.from_api_data(data)
        assert performance.id == '25DR-52O'
        assert performance.event_id == '25DR'
        assert performance.date_time.year == 2016
        assert performance.date_time.month == 10
        assert performance.date_time.day == 5
        assert performance.date_time.hour == 14
        assert performance.has_pool_seats is True
        assert performance.cached_max_seats == 10
        assert performance.cost_range.max_seatprice == 59.5
        assert performance.no_singles_cost_range.max_seatprice == 69.5
        assert performance.is_ghost is False
        assert performance.name == 'ABC123'
        assert performance.running_time == 200

        assert len(performance.availability_details) == 6

    def test_repr_with_date(self):
        performance = Performance(
            'ABC1-23',
            'ABC1',
            date_time=datetime.datetime(2017, 2, 8, 14, 8, 0),
        )
        assert repr(performance) == u'<Performance ABC1-23: 2017-02-08T14:08:00>'

    def test_repr_without_date(self):
        performance = Performance('ABC1-23', 'ABC1')
        assert repr(performance) == u'<Performance ABC1-23>'


class TestPerformanceMeta:

    def test_from_api_data(self):
        data = {
            'autoselect_this_performance': True,
            'results': {
                'has_perf_names': True,
                'performance': [
                    {'perf_id': '6IF-B1H', 'event_id': '6IF'}
                ],
                'paging_status': {
                    'total_unpaged_results': 1,
                },
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        meta = PerformanceMeta.from_api_data(data)

        assert meta.auto_select is True
        assert meta.has_names is True
        assert meta.total_results == 1
        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'
