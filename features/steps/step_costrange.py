import json
from behave import then
from hamcrest import assert_that, equal_to


@then(u'the event has cost range and no singles cost range')
def the_event_has_cost_range_and_no_singles_cost_range(context):
    assert context.event.cost_range
    assert context.event.no_singles_cost_range


@then(u'the cost range min seatprice is "{price}"')
def the_cost_range_min_seatprice_is(context, price):
    assert price
    price = float(price)
    assert_that(context.event.cost_range.min_seatprice, equal_to(price))


@then(u'the cost range max seatprice is "{price}"')
def the_cost_range_max_seatprice_is(context, price):
    assert price
    price = float(price)
    assert_that(context.event.cost_range.max_seatprice, equal_to(price))


@then(u'the cost range min surcharge is "{price}"')
def the_cost_range_min_surcharge_is(context, price):
    assert price
    price = float(price)
    assert_that(context.event.cost_range.min_surcharge, equal_to(price))


@then(u'the cost range max surcharge is "{price}"')
def the_cost_range_max_surcharge_is(context, price):
    assert price
    price = float(price)
    assert_that(context.event.cost_range.max_surcharge, equal_to(price))


@then(u'the cost range currency is "{currency}"')
def the_cost_range_currency_is(context, currency):
    assert currency
    assert_that(context.event.cost_range.currency.code, equal_to(currency))


@then(u'the valid quanities are "{quantities}"')
def the_valid_quantities_currency_are(context, quantities):
    assert quantities
    quantities = map(int, quantities.split(', '))
    assert_that(context.event.cost_range.valid_quantities, equal_to(quantities))


@then(u'the no singles cost range min seatprice is "{price}"')
def the_no_singles_cost_range_min_seatprice_is(context, price):
    assert price
    price = float(price)
    assert_that(context.event.no_singles_cost_range.min_seatprice, equal_to(price))


@then(u'the no singles cost range max seatprice is "{price}"')
def the_no_singles_cost_range_max_seatprice_is(context, price):
    assert price
    price = float(price)
    assert_that(context.event.no_singles_cost_range.max_seatprice, equal_to(price))


@then(u'the no singles cost range min surcharge is "{price}"')
def the_no_singles_cost_range_min_surcharge_is(context, price):
    assert price
    price = float(price)
    assert_that(context.event.no_singles_cost_range.min_surcharge, equal_to(price))


@then(u'the no singles cost range max surcharge is "{price}"')
def the_no_singles_cost_range_max_surcharge_is(context, price):
    assert price
    price = float(price)
    assert_that(context.event.no_singles_cost_range.max_surcharge, equal_to(price))


@then(u'the no singles cost range currency is "{currency}"')
def the_no_singles_cost_range_currency_is(context, currency):
    assert currency
    assert_that(context.event.no_singles_cost_range.currency.code, equal_to(currency))


@then(u'the no singles valid quanities are "{quantities}"')
def the_no_singles_valid_quantities_currency_are(context, quantities):
    assert quantities
    quantities = map(int, quantities.split(', '))
    assert_that(context.event.cost_range.valid_quantities, equal_to(quantities))


@then(u'the cost range has offers')
def then_the_cost_range_has_offers(context):
    expected = json.loads(context.text)
    for key, offer in expected.items():
        pass


@then(u'the no singles cost range has offers')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the no singles cost range has offers')
