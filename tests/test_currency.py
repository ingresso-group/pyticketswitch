from pyticketswitch.currency import Currency


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

    def test_eq(self):
        currency_one = Currency(
            code='usd', factor=321, places=2, number=123, pre_symbol='$',
            post_symbol='USD'
        )

        currency_two = Currency(
            code='usd', factor=321, places=2, number=123, pre_symbol='$',
            post_symbol='USD'
        )

        assert currency_one == currency_two

    def test_neq_code(self):
        currency_one = Currency('gbp')
        currency_two = Currency('usd')

        assert currency_one != currency_two

    def test_neq_factor(self):
        currency_one = Currency('gbp', factor=123)
        currency_two = Currency('gbp', factor=321)

        assert currency_one != currency_two

    def test_neq_number(self):
        currency_one = Currency('gbp', number=123)
        currency_two = Currency('gbp', number=321)

        assert currency_one != currency_two

    def test_neq_places(self):
        currency_one = Currency('gbp', places=3)
        currency_two = Currency('gbp', places=2)

        assert currency_one != currency_two

    def test_neq_pre_symbol(self):
        currency_one = Currency('gbp', pre_symbol='$')
        currency_two = Currency('gbp', pre_symbol='@')

        assert currency_one != currency_two

    def test_neq_post_symbol(self):
        currency_one = Currency('gbp', post_symbol='$')
        currency_two = Currency('gbp', post_symbol='@')

        assert currency_one != currency_two

    def test_neq_none(self):
        currency = Currency('gbp')
        assert currency != None  # noqa
