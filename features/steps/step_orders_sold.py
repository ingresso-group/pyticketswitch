import time
from datetime import datetime, timedelta

from behave import given, when, then
from hamcrest import assert_that, empty, equal_to, has_length, instance_of, not_
from pyticketswitch.exceptions import InvalidParametersError
from pyticketswitch.sold_order import SoldOrder

# These steps call the live API without a cassette: the orders sold change
# all the time, so a recorded response would not tell us anything.


@given("my user has sold at least two orders")
def given_my_user_has_sold_at_least_two_orders(context):
    orders = context.client.list_orders_sold(page_length=2)
    assert len(orders) == 2, "the demo account needs at least two orders sold"


@when("I list the orders sold for the transaction")
def when_i_list_the_orders_sold_for_the_transaction(context):
    # a new order takes a second or two to show up in the list, so keep asking
    deadline = time.monotonic() + 15
    while True:
        context.orders = context.client.list_orders_sold(
            transaction_uuid=context.transaction_uuid
        )
        if context.orders or time.monotonic() > deadline:
            return
        time.sleep(0.5)


@when("I list the orders sold one at a time for the first two pages")
def when_i_list_the_orders_sold_one_at_a_time(context):
    context.pages = [
        context.client.list_orders_sold(page=page, page_length=1) for page in (0, 1)
    ]


@when("I list the orders sold that were purchased from tomorrow")
def when_i_list_the_orders_sold_purchased_from_tomorrow(context):
    tomorrow = datetime.now() + timedelta(days=1)
    context.orders = context.client.list_orders_sold(earliest_purchase_time=tomorrow)


@when("I list the orders sold excluding purchased orders but not including failed ones")
def when_i_list_the_orders_sold_excluding_purchased(context):
    try:
        context.orders = context.client.list_orders_sold(include_purchased=False)
        context.exception = None
    except InvalidParametersError as excp:
        context.orders = None
        context.exception = excp


@then("I get one order")
def then_i_get_one_order(context):
    assert_that(context.orders, has_length(1))
    assert_that(context.orders[0], instance_of(SoldOrder))


@then("I get no orders")
def then_i_get_no_orders(context):
    assert_that(context.orders, empty())


@then("the order is for the transaction")
def then_the_order_is_for_the_transaction(context):
    assert_that(context.orders[0].transaction_uuid, equal_to(context.transaction_uuid))


@then("the order was purchased successfully")
def then_the_order_was_purchased_successfully(context):
    assert_that(context.orders[0].purchase_succeeded, equal_to(True))


@then("each page has one order")
def then_each_page_has_one_order(context):
    for page in context.pages:
        assert_that(page, has_length(1))
        assert_that(page[0], instance_of(SoldOrder))


@then("the two pages have different orders")
def then_the_two_pages_have_different_orders(context):
    # one transaction can hold several orders, told apart by item number
    first, second = ((page[0].transaction_uuid, page[0].item) for page in context.pages)
    assert_that(first, not_(equal_to(second)))


@then("an invalid parameters error is raised")
def then_an_invalid_parameters_error_is_raised(context):
    assert_that(context.exception, instance_of(InvalidParametersError))
