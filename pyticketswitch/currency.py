import six
from pyticketswitch.mixins import JSONMixin


class Currency(JSONMixin, object):
    """Information about the currency prices are described in.

    This information can be used to create human readable prices.

    Attributes:
        code (str): ISO 4217 currency code.
        places (int): precision of decimal numbers.
        pre_symbol (str): a symbol to place before the digits of a price.
        post_symbol (str): a symbol to place after the digits of a price.
        factor (int): arbitary scale factor, can be used to roughly convert
            from one currency to another.
        number (int): internal identifier.

    """

    def __init__(self, code, factor=None, places=None, number=None,
                 pre_symbol=None, post_symbol=None):

        self.factor = factor
        self.places = places
        self.pre_symbol = pre_symbol
        self.post_symbol = post_symbol
        self.code = code
        self.number = number

    def __eq__(self, other):
        """
        FIXME: do we need this anywhere other than tests?
        """
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
        """Convert data from the API into a native object.

        Args:
            data (dict): API data describing a currency.

        Returns:
            :class:`Currency <pyticketswitch.currency.Currency>`: the currency.

        """

        kwargs = {
            'factor': data.get('currency_factor'),
            'places': data.get('currency_places'),
            'number': data.get('currency_number'),
            'pre_symbol': data.get('currency_pre_symbol'),
            'post_symbol': data.get('currency_post_symbol'),
        }

        return cls(data.get('currency_code'), **kwargs)

    def price_as_string(self, price):
        """Generates a human readble string for a price.

        Args:
            price (float): a price

        Returns:
            str: the price with the correct number of places with pre and post
            symbols attached

        Example:

            >>> from pyticketswitch.currency import Currency
            >>> usd = Currency('usd', pre_symbol='$', places=2)
            >>> usd.price_as_string(5)
            u'$5.00'
            >>> usd.price_as_string(12.34567)
            u'$12.34'

        """
        price = price if price else 0
        format_string = six.text_type('{pre}{price:.' + str(self.places) + 'f}{post}')
        return format_string.format(
            pre=self.pre_symbol or '',
            price=price,
            post=self.post_symbol or '',
        )

    def __repr__(self):
        return u'<Currency {}>'.format(self.code)


class CurrencyMeta(JSONMixin, object):
    """Currency information for another object.

    Attributes:
        currencies (dict) dictionary of
            :class:`Currency <pytickectswitch.currency.Currency>`) objects
            indexed on currency code.
        default_currency_code (str): unless other wise specified all prices in
            the related response will be in this currency.
        desired_currency_code (str):
            the currency that the user account is expecting. Useful for
            conversions.

    """

    def __init__(self, currencies, default_currency_code=None,
                 desired_currency_code=None):
        self.currencies = currencies
        self.default_currency_code = default_currency_code
        self.desired_currency_code = desired_currency_code

    @classmethod
    def from_api_data(cls, data):
        """Convert data from the API into a native object.

        Args:
            data (dict): API data describing the currencies of a related
                object.

        Returns:
            :class:`CurrencyMeta <pyticketswitch.currency.CurrencyMeta>`: the
                currency meta data.

        """
        currency_data = data.get('currency_details')
        if not currency_data:
            return cls(currencies={})

        currencies = {
            code: Currency.from_api_data(value)
            for code, value in currency_data.items()
        }

        default_currency_code = data.get('currency_code')
        desired_currency_code = data.get('desired_currency_code')

        return cls(
            currencies=currencies,
            default_currency_code=default_currency_code,
            desired_currency_code=desired_currency_code,
        )

    def get_currency(self, code=None):
        """Get the :class:`Currency <pyticketswitch.currency.Currency>` object for the given code.

        Args:
            code (str, optional): ISO 4217 currency code.

        Returns:
            :class:`Currency <pyticketswitch.currency.Currency>`: The currency
            for the given code.

            If no code is specified, return the default currency as specified
            by :attr:`CurrencyMeta.default_currency_code <pyticketswitch.currency.CurrencyMeta.default_currency_code>`.

            If no default currency is specified return :obj:`None`.

        """
        if not code:
            code = self.default_currency_code

        if not code:
            return None

        return self.currencies.get(code)

    def get_desired_currency(self):
        """Get the :class:`Currency <pyticketswitch.currency.Currency>` object for the desired currency.

        Returns:
            :class:`Currency <pyticketswitch.currency.Currency>`: The currency
            for the desired currency.

            If no desired currency is specified return :obj:`None`.
        """
        if not self.desired_currency_code:
            return None

        return self.currencies.get(self.desired_currency_code)
