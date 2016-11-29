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
