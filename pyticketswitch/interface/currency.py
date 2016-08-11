class Currency(object):

    def __init__(self, factor=100, places=2, code=None,
                 pre_symbol=None, post_symbol=None):

        self.factor = factor
        self.places = places
        self.pre_symbol = pre_symbol
        self.post_symbol = post_symbol
        self.code = code

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'factor': data.get('currency_factor', 100),
            'places': data.get('currency_places', 2),
            'code': data.get('currency_code', None),
            'pre_symbol': data.get('currency_pre_symbol', None),
            'post_symbol': data.get('currency_post_symbol', None),
        }

        return cls(**kwargs)
