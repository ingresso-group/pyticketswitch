from pyticketswitch.interface.cost_range import CostRange


class TestCostRange:

    def test_from_api_data(self):
        data = {
            'quantity_options': {
                'valid_quantity_mask': '2046'
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
