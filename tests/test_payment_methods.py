import pytest
from pyticketswitch.exceptions import InvalidParametersError
from pyticketswitch.payment_methods import (
    PaymentMethod, CardDetails, RedirectionDetails, StripeDetails,
)


class TestCardDetails:

    def test_is_payment_method(self):
        card_details = CardDetails('411111111111111')
        assert isinstance(card_details, PaymentMethod)

    def test_as_api_parameters(self):
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=45,
            start_month=3,
            start_year=19,
            ccv2=123,
            issue_number=7,
        )

        params = card_details.as_api_parameters()

        assert params == {
            'card_number': '4111 1111 1111 1111',
            'expiry_date': '0545',
            'start_date': '0319',
            'cv_two': 123,
            'issue_number': 7,
        }

    def test_as_api_parameters_without_expiry_date(self):
        card_details = CardDetails('4111 1111 1111 1111')
        with pytest.raises(InvalidParametersError):
            card_details.as_api_parameters()

    def test_as_api_parameters_without_expiry_month(self):
        card_details = CardDetails('4111 1111 1111 1111', expiry_year=45)
        with pytest.raises(InvalidParametersError):
            card_details.as_api_parameters()

    def test_as_api_parameters_without_expiry_year(self):
        card_details = CardDetails('4111 1111 1111 1111', expiry_month=5)
        with pytest.raises(InvalidParametersError):
            card_details.as_api_parameters()

    def test_as_api_parameters_without_extras(self):
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=45,
        )

        params = card_details.as_api_parameters()

        assert params == {
            'card_number': '4111 1111 1111 1111',
            'expiry_date': '0545',
        }

    def test_as_api_parameters_with_start_month_without_start_year(self):
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=45,
            start_month=3,
        )

        with pytest.raises(InvalidParametersError):
            card_details.as_api_parameters()

    def test_as_api_parameters_with_start_year_without_start_month(self):
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=45,
            start_year=19,
        )

        with pytest.raises(InvalidParametersError):
            card_details.as_api_parameters()


class TestRedirectionDetails:

    def test_is_payment_method(self):
        redirect_details = RedirectionDetails(
            'abc123',
            'https://foobar.com/payment/abc123',
            'iceweasle 9000',
            'application/json',
            'foobar.com',
        )
        assert isinstance(redirect_details, PaymentMethod)

    def test_as_api_parameters(self):
        redirect_details = RedirectionDetails(
            'abc123',
            'https://foobar.com/payment/abc123',
            'iceweasle 9000',
            'application/json',
            'foobar.com',
        )

        params = redirect_details.as_api_parameters()

        assert params == {
            'return_token': 'abc123',
            'return_url': 'https://foobar.com/payment/abc123',
            'client_http_user_agent': 'iceweasle 9000',
            'client_http_accept': 'application/json',
            'remote_site': 'foobar.com'
        }


class TestStripeDetails:

    def test_is_payment_method(self):
        stripe_details = StripeDetails({'foo': 'abc123', 'bar': 'def456'})
        assert isinstance(stripe_details, PaymentMethod)

    def test_as_api_parameters(self):
        stripe_details = StripeDetails({'foo': 'abc123', 'bar': 'def456'})
        params = stripe_details.as_api_parameters()
        assert params == {
            'foo_callback/stripe_token': 'abc123',
            'bar_callback/stripe_token': 'def456',
        }
