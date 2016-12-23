from pyticketswitch.cost_range import CostRange, CostRangeDetails


class TestCostRange:

    def test_from_api_data(self):
        data = {
            'quantity_options': {
                'valid_quantity_mask': 170,
            },
            'max_surcharge': 29.65,
            'max_seatprice': 149.5,
            'range_currency': {
                'currency_factor': 100,
                'currency_places': 2,
                'currency_post_symbol': '',
                'currency_pre_symbol': '\xa3',
                'currency_code': 'gbp'
            },
            'min_surcharge': 7.25,
            'min_seatprice': 37.5,
        }
        cost_range = CostRange.from_api_data(data)

        assert cost_range.max_surcharge == 29.65
        assert cost_range.max_seatprice == 149.5
        assert cost_range.min_surcharge == 7.25
        assert cost_range.min_seatprice == 37.5

        assert cost_range.currency.code == 'gbp'
        assert cost_range.currency.pre_symbol == '\xa3'
        assert cost_range.currency.post_symbol == ''
        assert cost_range.currency.places == 2
        assert cost_range.currency.factor == 100
        assert cost_range.valid_quantities == [2, 4, 6, 8]


class TestCostRangeDetails:

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
                            'cost_range': {
                                'max_surcharge': 29.65,
                                'max_seatprice': 149.5,
                            },
                        },
                        {
                            'price_band_code': 'TRG',
                            'price_band_desc': 'Troglodites',
                            'cost_range': {
                                'max_surcharge': 29.65,
                                'max_seatprice': 149.5,
                            },
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
                            'cost_range': {
                                'max_surcharge': 29.65,
                                'max_seatprice': 149.5,
                            },
                        },
                        {
                            'price_band_code': 'CBH',
                            'price_band_desc': 'Chinese Billionaire Heiress',
                            'cost_range': {
                                'max_surcharge': 29.65,
                                'max_seatprice': 149.5,
                            },
                        }
                    ]
                }
            ]
        }

        details = CostRangeDetails.from_api_data(data)
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

    def test_from_api_data_adds_cost_range(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'cost_range': {
                                'max_surcharge': 29.65,
                                'max_seatprice': 149.5,
                            },
                        },
                    ]
                },
            ]
        }

        details = CostRangeDetails.from_api_data(data)
        assert len(details) == 1
        assert isinstance(details[0].cost_range, CostRange)

    def test_from_api_data_adds_cost_range_no_singles(self):
        data = {
            'ticket_type': [
                {
                    'ticket_type_code': 'FOO',
                    'ticket_type_desc': 'Foo',
                    'price_band': [
                        {
                            'price_band_code': 'PLB',
                            'price_band_desc': 'Plebians',
                            'cost_range': {
                                'no_singles_cost_range': {
                                    'max_surcharge': 29.65,
                                    'max_seatprice': 149.5,
                                }
                            },
                        },
                    ]
                },
            ]
        }

        details = CostRangeDetails.from_api_data(data)
        assert len(details) == 1
        assert isinstance(details[0].cost_range_no_singles, CostRange)

    def test_from_api_data_ignores_data_with_no_cost_ranges(self):
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
                    ]
                },
            ]
        }

        details = CostRangeDetails.from_api_data(data)
        assert len(details) == 0
