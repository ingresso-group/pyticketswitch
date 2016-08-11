from pyticketswitch.interface.currency import Currency


class TestCurrency:

    def test_from_api_data(self):

        data = {
            'currency_factor': 100,
            'currency_places': 2,
            'currency_post_symbol': '',
            'currency_pre_symbol': '\xa3',
            'currency_code': 'gbp'
        }
        currency = Currency.from_api_data(data)

        assert currency.factor == 100
        assert currency.places == 2
        assert currency.post_symbol == ''
        assert currency.pre_symbol == '\xa3'
        assert currency.code == 'gbp'
