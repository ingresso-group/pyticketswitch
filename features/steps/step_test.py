import vcr
from behave import when, then


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
    assert context.user.id == context.user_id
