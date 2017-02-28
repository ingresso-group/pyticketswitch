import vcr
from behave import given, when, then
from hamcrest import assert_that, greater_than

vcr_post = vcr.VCR(match_on=('method', 'scheme', 'host', 'port', 'path', 'query', 'body'))


@given('my customer wants tickets to "{event_id}"')
@vcr.use_cassette('fixtures/cassettes/reserve-availability.yaml', record_mode='new_episodes')
def given_customer_wants_tickets(context, event_id):
    assert event_id
    performances, meta = context.client.list_performances(event_id)

    assert performances

    performance = performances[0]

    context.performances = performances
    context.performance_meta = meta
    context.performance = performance

    ticket_types, meta = context.client.get_availability(performance.id)

    assert ticket_types
    ticket_type = ticket_types[0]
    context.ticket_type = ticket_type

    assert ticket_type.price_bands
    context.price_band = ticket_type.price_bands[0]
    context.no_of_tickets = 2

# @given('my customer has requested some discounts')
# @vcr.use_cassette('fixtures/cassettes/reserve-discounts.yaml', record_mode='new_episodes')
# def given_my_customer_has_requested_some_discounts(context):
#     discounts, meta = context.client.get_discounts()


@when('I reserve the tickets')
@vcr_post.use_cassette('fixtures/cassettes/reserve-reserve.yaml', record_mode='new_episodes')
def when_i_reserve_the_tickets(context):
    reservation = context.client.make_reservation(
        performance_id=context.performance.id,
        number_of_seats=context.no_of_tickets,
        ticket_type_code=context.ticket_type.code,
        price_band_code=context.price_band.code,
    )

    assert reservation
    context.reservation = reservation
    context.transaction_uuid = reservation.trolley.transaction_uuid


@then('my reservation is successful')
def then_my_reservation_is_successful(context):
    assert_that(context.reservation.minutes_left, greater_than(0))
