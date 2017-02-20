from abc import ABCMeta


class PaymentMethod(metaclass=ABCMeta):
    """Abstract base class for payment methods"""

    def as_api_parameters(self):
        """Generate keyword arguments suitable for consumption by the
        ticketswitch API

        Returns:
            dict: dictionary of keyword parameters to pass to the API call.
        """
        raise NotImplemented('as_api_parameters not implemented on ' +
                             self.__class__)


class CardDetails(object):
    """Credit card details

    This should never be returned by the API and is only used for supplying
    card details to the purchase call.

    Implements
    :class:`PaymentMethod <pyticketswitch.payment_methods.PaymentMethod>`.

    Args:
        card_number (str): the long credit card number
        expiry_month (int, optional): the month the card expires in. Defaults
            to :obj:`None`.
        expiry_year (int, optional): the year the card expires in. :obj:`None`
        start_month (int, optional): the month the card expires in. Defaults to
            :obj:`None`.
        start_year (int, optional): the year the card expires in. :obj:`None`
        ccv2 (str, optional): credit card security code. Defaults
            to :obj:`None`.
        issue_number (str, optional): issue number of the card. Defaults
            to :obj:`None`.

    Attributes:
        card_number (str): the long credit card number.
        expiry_month (int): the month the card expires in. Defaults to
            :obj:`None`.
        expiry_year (int): the year the card expires in. :obj:`None`.
        start_month (int): the month the card expires in. Defaults to
            :obj:`None`.
        start_year (int): the year the card expires in. :obj:`None`.
        ccv2 (str): credit card security code. Defaults to :obj:`None`.
        issue_number (str): issue number of the card. Defaults to :obj:`None`.

    """

    def __init__(self, card_number, expiry_month=None, expiry_year=None,
                 start_month=None, start_year=None, ccv2=None,
                 issue_number=None):

        self.card_number = card_number
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year
        self.start_month = start_month
        self.start_year = start_year
        self.ccv2 = ccv2
        self.issue_number = issue_number

    def as_api_parameters(self):
        params = {
            'card_number': self.card_number,
        }

        if self.expiry_month:
            params.update(expiry_month=self.expiry_month)

        if self.expiry_year:
            params.update(expiry_year=self.expiry_year)

        if self.start_month:
            params.update(start_month=self.start_month)

        if self.start_year:
            params.update(start_year=self.start_year)

        if self.ccv2:
            params.update(ccv2=self.ccv2)

        if self.issue_number:
            params.update(issue_number=self.issue_number)

        return params


class RedirectionDetails(object):
    """Information that specifies where a customer will be returned to after
    being redirected to an external payment provider.

    Implements
    :class:`PaymentMethod <pyticketswitch.payment_methods.PaymentMethod>`.

    Args:
        token (str): a unique token that can be used by you to identify when
            this callout returns to your website when the customer returns from
            the payment provider.
        url (str): the URL that the payment provider should redirect back to on
            succes/failure of the customers payment. The URL should be unique.
            The easy way to do this is to include the token in the URL address.
            It's important that this doesn't include any query string
            parameters.
        user_agent (str): the customer's browser's User-Agent header.
        accept (str): the customer's browser's Accept header.

    Attributes:
        token (str): a unique token that can be used by you to identify when
            this callout returns to your website.
        url (str): the URL that the payment provider should redirect back to on
            succes/failure of the customers payment.
        user_agent (str): the customer's browser's User-Agent header.
        accept (str): the customer's browser's Accept header.

    """

    def __init__(self, token, url, user_agent, accept):
        self.token = token
        self.url = url
        self.user_agent = user_agent
        self.accept = accept

    def as_api_parameters(self):
        """Generate API keyword args for these details.

        Returns:
            dict: the redirection details in a format the API will understand.

        """
        return {
            'return_token': self.token,
            'return_url': self.url,
            'client_http_user_agent': self.user_agent,
            'client_http_accept': self.accept,
        }


PaymentMethod.register(CardDetails)
PaymentMethod.register(RedirectionDetails)
