import vcr
from behave import given, when, then
from hamcrest import (assert_that, has_length, greater_than, is_not,
                      empty)


@given('I have a performance ID for event with ID "{event_id}"')
@vcr.use_cassette('fixtures/cassettes/availability-performances.yaml', record_mode='new_episodes')
def given_i_have_a_performance_id(context, event_id):
    assert event_id
    performances, _ = context.client.list_performances(event_id)
    assert performances
    context.performance = performances[0]


@when('I fetch availability for my performance')
@vcr.use_cassette('fixtures/cassettes/availability.yaml', record_mode='new_episodes')
def when_i_fetch_availability(context):
    ticket_types, meta = context.client.get_availability(
        context.performance.id,
        example_seats=True,
        seat_blocks=True,
    )

    context.ticket_types = ticket_types
    context.availability_meta = meta


@then('I get a list of available ticket types')
def then_i_get_a_list_of_available_ticket_types(context):
    assert_that(context.ticket_types, has_length(greater_than(0)))


@then('each ticket type has at least one price band')
def then_each_ticket_type_has_at_least_one_price_band(context):
    for ticket_type in context.ticket_types:
        assert_that(ticket_type.price_bands, has_length(greater_than(0)))


@then('each price band has a price')
def then_each_price_band_has_a_price(context):
    for ticket_type in context.ticket_types:
        for price_band in ticket_type.price_bands:
            assert_that(price_band.seatprice, greater_than(0))


@then('each price band has some example seats')
def then_each_price_band_has_some_example_seats(context):
    for ticket_type in context.ticket_types:
        for price_band in ticket_type.price_bands:
            assert_that(price_band.example_seats, is_not(empty()))


@then('each price band has some real seats')
def then_each_price_band_has_some_real_seats(context):
    for ticket_type in context.ticket_types:
        for price_band in ticket_type.price_bands:
            assert_that(price_band.get_seats(), is_not(empty()))
