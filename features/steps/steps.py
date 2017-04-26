from behave import given, then
from hamcrest import *  # noqa
from pyticketswitch import Client
from pyticketswitch.exceptions import AuthenticationError


@given('an API client with valid credentials')
def given_an_api_client_with_valid_credentials(context):
    client = Client('demo', 'demopass', url='https://api.ticketswitch.com')
    context.client = client
    context.user_id = 'demo'


@given('an API client with invalid credentials')
def given_an_api_client_with_invalid_credentials(context):
    client = Client('boatymcboatyface', 'irship', url='https://api.ticketswitch.com')
    context.client = client
    context.user_id = 'boatymcboatyface'


@then('an authorisation error should be raised')
def then_the_response_should_contain_a_user_object(context):
    assert_that(context.exception, instance_of(AuthenticationError))
