import six


class Currency(object):

    def __init__(self, code, factor=None, places=None, number=None,
                 pre_symbol=None, post_symbol=None):

        self.factor = factor
        self.places = places
        self.pre_symbol = pre_symbol
        self.post_symbol = post_symbol
        self.code = code
        self.number = number

    def __eq__(self, other):

        if not other:
            return False

        if not self.code == other.code:
            return False

        if not self.number == other.number:
            return False

        if not self.factor == other.factor:
            return False

        if not self.places == other.places:
            return False

        if not self.pre_symbol == other.pre_symbol:
            return False

        if not self.post_symbol == other.post_symbol:
            return False

        return True

    def __ne__(self, other):
        return not self == other

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'factor': data.get('currency_factor'),
            'places': data.get('currency_places'),
            'number': data.get('currency_number'),
            'pre_symbol': data.get('currency_pre_symbol'),
            'post_symbol': data.get('currency_post_symbol'),
        }

        return cls(data.get('currency_code'), **kwargs)

    def price_as_string(self, price):
        price = price if price else 0
        format_string = six.text_type('{pre}{price:.' + str(self.places) + 'f}{post}')
        return format_string.format(
            pre=self.pre_symbol or '',
            price=price,
            post=self.post_symbol or '',
        )


class CurrencyMeta(object):

    def __init__(self, currency, desired_currency=None):
        self.currency = currency
        self.desired_currency = desired_currency

    @classmethod
    def from_api_data(cls, data):
        currency_data = data.get('currency')
        if not currency_data:
            return

        currency = Currency.from_api_data(currency_data)

        desired_currency_data = data.get('desired_currency')
        if desired_currency_data:
            desired_currency = Currency.from_api_data(desired_currency_data)
        else:
            desired_currency = None

        return cls(currency, desired_currency=desired_currency)
