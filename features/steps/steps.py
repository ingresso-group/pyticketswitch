from behave import given
from pyticketswitch import Client


@given('an API client with valid credentials')
def given_an_api_client_with_valid_credentials(context):
    client = Client('demo', 'demopass', url='https://api.ticketswitch.com')
    context.client = client
    context.expected_user_id = 'demo'


@given('an API client with invalid credentials')
def given_an_api_client_with_invalid_credentials(context):
    client = Client('boatymcboatyface', 'irship', url='https://api.ticketswitch.com')
    context.client = client
    context.expected_user_id = 'boatymcboatyface'

