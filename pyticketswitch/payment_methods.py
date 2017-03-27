import six
from abc import ABCMeta
from pyticketswitch.exceptions import InvalidParametersError


@six.add_metaclass(ABCMeta)
class PaymentMethod(object):
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
        """Generates a dictionary of parameters to be passed back to the API.

        Returns:
            dict: a set of parameters describing the card details to the API.

        """
        params = {
            'card_number': self.card_number,
        }

        missing_expiry_year = not self.expiry_year
        missing_expiry_month = not self.expiry_month

        if missing_expiry_year or missing_expiry_month:
            raise InvalidParametersError(
                'both expiry_year and expiry_month must be specified')

        params.update(
            expiry_date='{:0>2}{:0>2}'.format(
                self.expiry_month,
                self.expiry_year
            )
        )

        missing_start_year = not self.start_year
        missing_start_month = not self.start_month

        specifying_start_date = self.start_year or self.start_month

        if specifying_start_date and (missing_start_year or missing_start_month):
            raise InvalidParametersError(
                'both start_year and start_month must be specified or neither specified')

        if specifying_start_date:
            params.update(
                start_date='{:0>2}{:0>2}'.format(
                    self.start_month,
                    self.start_year
                )
            )

        if self.ccv2:
            params.update(cv_two=self.ccv2)

        if self.issue_number:
            params.update(issue_number=self.issue_number)

        return params


class RedirectionDetails(object):
    """Information that specifies where a customer will be returned to after
    being redirected to an external payment provider.

    Implements
    :class:`PaymentMethod <pyticketswitch.payment_methods.PaymentMethod>`.

    Attributes:
        token (str): a unique token that can be used by you to identify when
            this callout returns to your website.
        url (str): the URL that the payment provider should redirect back to on
            success/failure of the customers payment.
        user_agent (str): the customer's browser's User-Agent header.
        accept (str): the customer's browser's Accept header.
        remote_site (str): the remote site's domain must match the domain of the
            return_url.

    """

    def __init__(self, token, url, user_agent, accept, remote_site):
        self.token = token
        self.url = url
        self.user_agent = user_agent
        self.accept = accept
        self.remote_site = remote_site

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
            'remote_site': self.remote_site,
        }


class StripeDetails(object):
    """For use with self generated stripe tokens

    Can be used to provide stripe tokens directly to the API at purchase time
    avoiding a callout/callback cycle.

    Implements
    :class:`PaymentMethod <pyticketswitch.payment_methods.PaymentMethod>`.

    Attributes:
        tokens (dict): dictionary of stripe card tokens indexed on bundle source
            code. If there are multiple bundles in the trolley, then a unique
            stripe token must be provided for each of the bundles you wish to
            purchase with stripe.
    """

    def __init__(self, tokens):
        self.tokens = tokens

    def as_api_parameters(self):
        """Generate API keyword args for these details.

        Returns:
            dict: the stripe details in a format the API will understand.

        """

        return {
            '{}_callback/stripe_token'.format(source): token
            for source, token in self.tokens.items()
        }


PaymentMethod.register(CardDetails)
PaymentMethod.register(RedirectionDetails)
PaymentMethod.register(StripeDetails)
