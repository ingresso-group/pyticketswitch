from pyticketswitch.cost_range import CostRange, CostRangeDetails
from pyticketswitch.offer import Offer


class TestCostRange:

    def test_from_api_data(self):
        data = {
            "best_value_offer": {
                "absolute_saving": 10,
            },
            "max_saving_offer": {
                "absolute_saving": 8,
            },
            "max_seatprice": 149.5,
            "max_surcharge": 29.65,
            "min_cost_offer": {
                "absolute_saving": 7,
            },
            "min_seatprice": 37.5,
            "min_surcharge": 7.25,
            "range_currency_code": "usd",
            "top_price_offer": {
                "absolute_saving": 9,
            },
            "max_combined_combined_tax_component": 35.0,
            "max_combined_surcharge_tax_sub_component": 0.0,
            "min_combined_combined_tax_component": 35.0,
            "min_combined_surcharge_tax_sub_component": 0.0,
            "valid_quantities": [1, 2, 3, 4]
        }
        cost_range = CostRange.from_api_data(data)

        assert cost_range.max_surcharge == 29.65
        assert cost_range.max_seatprice == 149.5
        assert cost_range.min_surcharge == 7.25
        assert cost_range.min_seatprice == 37.5

        assert cost_range.top_price_offer.absolute_saving == 9.0
        assert cost_range.min_cost_offer.absolute_saving == 7.0
        assert cost_range.max_saving_offer.absolute_saving == 8.0
        assert cost_range.best_value_offer.absolute_saving == 10.0

        assert cost_range.currency == 'usd'
        assert cost_range.valid_quantities == [1, 2, 3, 4]

        assert cost_range.max_combined_combined_tax_component == 35.0
        assert cost_range.max_combined_surcharge_tax_sub == 0.0
        assert cost_range.min_combined_combined_tax_component == 35.0
        assert cost_range.min_combined_surcharge_tax_sub == 0.0

    def test_has_offer_with_no_offers(self):
        cost_range = CostRange()
        assert cost_range.has_offer() is False

    def test_has_offer_with_best_value_offer(self):
        offer = Offer()
        cost_range = CostRange(best_value_offer=offer)
        assert cost_range.has_offer() is True

    def test_has_offer_with_max_saving_offer(self):
        offer = Offer()
        cost_range = CostRange(max_saving_offer=offer)
        assert cost_range.has_offer() is True

    def test_has_offer_with_min_cost_offer(self):
        offer = Offer()
        cost_range = CostRange(min_cost_offer=offer)
        assert cost_range.has_offer() is True

    def test_has_offer_with_top_price_offer(self):
        offer = Offer()
        cost_range = CostRange(top_price_offer=offer)
        assert cost_range.has_offer() is True

    def test_get_min_combined_price(self):
        cost_range = CostRange(min_seatprice=10, min_surcharge=5)
        assert cost_range.get_min_combined_price() == 15.0

    def test_get_max_combined_price(self):
        cost_range = CostRange(max_seatprice=22, max_surcharge=8)
        assert cost_range.get_max_combined_price() == 30.0

    def test_has_tax_with_combined_tax_components(self):
        cost_range = CostRange(
            max_combined_combined_tax_component=35.0,
            min_combined_combined_tax_component=0.0,
        )
        assert cost_range.has_tax() is True

    def test_has_tax_with_surcharge_tax_sub_components(self):
        cost_range = CostRange(
            max_combined_surcharge_tax_sub=35.0,
            min_combined_surcharge_tax_sub=0.0,
        )
        assert cost_range.has_tax() is True


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

        assert details[0].ticket_type_code == 'FOO'
        assert details[0].ticket_type_description == 'Foo'
        assert details[0].price_band_code == 'PLB'
        assert details[0].price_band_description == 'Plebians'

        assert details[1].ticket_type_code == 'FOO'
        assert details[1].ticket_type_description == 'Foo'
        assert details[1].price_band_code == 'TRG'
        assert details[1].price_band_description == 'Troglodites'

        assert details[2].ticket_type_code == 'BAR'
        assert details[2].ticket_type_description == 'Bar'
        assert details[2].price_band_code == 'VIP'
        assert details[2].price_band_description == 'Very Important People'

        assert details[3].ticket_type_code == 'BAR'
        assert details[3].ticket_type_description == 'Bar'
        assert details[3].price_band_code == 'CBH'
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
