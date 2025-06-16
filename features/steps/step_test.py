import vcr
from behave import when, then
from behave import then
from hamcrest import (
    assert_that, instance_of
)
from pyticketswitch.exceptions import AuthenticationError


@when('the test method is called')
@vcr.use_cassette('fixtures/cassettes/test.yaml', record_mode='new_episodes', match_on=['method', 'uri', 'headers'])
def when_the_test_method_is_called(context):
    try:
        context.user = context.client.test()
        context.exception = None
    except Exception as e:
        context.user = None
        context.exception = e


@then('the response should contain a User object')
def then_the_response_should_contain_a_user_object(context):
    assert context.exception is None
    assert context.user.id == context.expected_user_id


@then('an authorisation error should be raised')
def an_auth_error_should_be_raised(context):
    assert_that(context.exception, instance_of(AuthenticationError))
