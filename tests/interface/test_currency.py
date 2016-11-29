from pyticketswitch.interface.currency import Currency


class TestCurrency:

    def test_from_api_data(self):

        data = {
            'currency_factor': 100,
            'currency_places': 2,
            'currency_post_symbol': '\xa4',
            'currency_pre_symbol': '\xa3',
            'currency_code': 'gbp',
            'currency_number': 826,
        }
        currency = Currency.from_api_data(data)

        assert currency.factor == 100
        assert currency.places == 2
        assert currency.post_symbol == '\xa4'
        assert currency.pre_symbol == '\xa3'
        assert currency.code == 'gbp'
        assert currency.number == 826
