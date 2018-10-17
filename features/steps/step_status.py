from behave import given, when, then
from hamcrest import assert_that, equal_to


@given('I have a completed transaction')
def given_i_have_a_completed_transaction(context):
    context.execute_steps("""
        Given my account is set up to allow a user to buy on credit
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        When I purchase the tickets
        Then the purchase is succesful""")

@when('I fetch the status of the transaction')
def when_i_fetch_the_status_of_the_transaction(context):
    status, _ = context.client.get_status(context.transaction_uuid)
    context.status = status


@then('the status is "{expected}"')
def then_the_status_is(context, expected):
    assert context.status
    assert_that(context.status.status, equal_to(expected))
