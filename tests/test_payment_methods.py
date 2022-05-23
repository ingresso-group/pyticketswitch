import pytest
from pyticketswitch.exceptions import InvalidParametersError
from pyticketswitch.address import Address
from pyticketswitch.payment_methods import (
    PaymentMethod, CardDetails, RedirectionDetails, StripeDetails, CiderDetails
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

    def test_as_api_parameters_with_billing_address(self):
        billing_address = Address(
            lines=['1303 Boulder Lane', 'Landslide district'],
            country_code='us',
            county='Louisana',
            town='Bedrock',
            post_code='70777',
        )
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=45,
            billing_address=billing_address,
        )

        params = card_details.as_api_parameters()

        assert params == {
            'card_number': '4111 1111 1111 1111',
            'expiry_date': '0545',
            'billing_address_line_one': '1303 Boulder Lane',
            'billing_address_line_two': 'Landslide district',
            'billing_country_code': 'us',
            'billing_county': 'Louisana',
            'billing_town': 'Bedrock',
            'billing_postcode': '70777',
        }

    def test_as_api_parameters_with_return_url_and_token(self):
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=45,
            return_url='https://acmetickets.com/checkout/',
            remote_site='acmetickets.com',
            return_token='abc123',
        )

        params = card_details.as_api_parameters()

        assert params == {
            'card_number': '4111 1111 1111 1111',
            'expiry_date': '0545',
            'return_url': 'https://acmetickets.com/checkout/',
            'remote_site': 'acmetickets.com',
            'return_token': 'abc123',
        }

    def test_as_api_parameters_with_user_agent_header(self):
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=45,
            user_agent='iceweasle',
        )

        params = card_details.as_api_parameters()

        assert params == {
            'card_number': '4111 1111 1111 1111',
            'expiry_date': '0545',
            'client_http_user_agent': 'iceweasle',
        }

    def test_as_api_parameters_with_accept_header(self):
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=45,
            accept='application/json',
        )

        params = card_details.as_api_parameters()

        assert params == {
            'card_number': '4111 1111 1111 1111',
            'expiry_date': '0545',
            'client_http_accept': 'application/json',
        }

    def test_as_api_parameters_with_long_expiry_start_year(self):
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_month=5,
            expiry_year=2017,
            start_month=3,
            start_year=1943,
        )

        params = card_details.as_api_parameters()

        assert params == {
            'card_number': '4111 1111 1111 1111',
            'expiry_date': '0517',
            'start_date': '0343',
        }


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
            'foo_callback/stripeToken': 'abc123',
            'bar_callback/stripeToken': 'def456',
        }


class TestCiderDetails:

    def test_is_payment_method(self):
        cider_details = CiderDetails({'beep': 'bop'}, ["test"])
        assert isinstance(cider_details, PaymentMethod)

    def test_as_api_parameters(self):
        cider_details = CiderDetails({'beep': 'boop'}, ["test", "bip"])
        params = cider_details.as_api_parameters()
        assert params == {
            'test_callback/beep': 'boop',
            'bip_callback/beep': 'boop',
        }
