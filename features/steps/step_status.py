from behave import given, when, then
from hamcrest import assert_that, equal_to


@given('I have a completed transaction')
def given_i_have_a_completed_transaction(context):
    context.transaction_uuid = 'f9f429d5-ff7b-11e6-983c-0025903268a0'


@when('I fetch the status of the transaction')
def when_i_fetch_the_status_of_the_transaction(context):
    status = context.client.get_status(context.transaction_uuid)
    context.status = status


@then('the status is "{expected}"')
def then_the_status_is(context, expected):
    assert context.status
    assert_that(context.status.status, equal_to(expected))
