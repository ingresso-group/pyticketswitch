import vcr
from behave import given, when, then
from hamcrest import (
    assert_that, greater_than, has_length, equal_to, has_items, is_, has_item,
    is_not
)

vcr_post = vcr.VCR(match_on=('method', 'scheme', 'host', 'port', 'path', 'query', 'body'))


@given('my customer wants tickets to "{event_id}"')
@vcr.use_cassette('fixtures/cassettes/reserve-availability.yaml', record_mode='new_episodes')
def given_customer_wants_tickets(context, event_id):
    assert event_id
    performances, meta = context.client.list_performances(event_id)

    assert performances

    if event_id == '7AB':
        performance = performances[1]
    else:
        performance = performances[14]

    context.performances = performances
    context.performance_meta = meta
    context.performance = performance
    context.performance_id = performance.id

    ticket_types, meta = context.client.get_availability(
        performance.id, seat_blocks=True
    )

    assert ticket_types
    ticket_type = ticket_types[0]
    context.ticket_type = ticket_type
    context.ticket_type_code = ticket_type.code

    assert ticket_type.price_bands
    price_band = ticket_type.price_bands[0]

    assert price_band

    context.price_band = price_band
    context.price_band_code = price_band.code
    context.no_of_tickets = 2
    context.discounts = None
    context.send_method = None
    context.send_codes = None
    context.seats = None


@given('I have an existing trolley with items from "{event_id}" in it')
@vcr.use_cassette('fixtures/cassettes/trolley-existing.yaml', record_mode='new_episodes')
def given_an_existing_trolley(context, event_id):
    assert event_id
    performances, _ = context.client.list_performances(event_id)

    assert performances

    if event_id == '7AB':
        performance = performances[1]
    else:
        performance = performances[14]

    ticket_types, meta = context.client.get_availability(
        performance.id, seat_blocks=True
    )

    assert ticket_types
    ticket_type = ticket_types[0]

    assert ticket_type.price_bands
    price_band = ticket_type.price_bands[0]

    assert price_band

    trolley_token = None
    if hasattr(context, 'trolley_token'):
        trolley_token = context.trolley_token

    trolley, _ = context.client.get_trolley(
        token=trolley_token,
        performance_id=performance.id,
        ticket_type_code=ticket_type.code,
        price_band_code=price_band.code,
        number_of_seats=2,
    )

    assert trolley
    context.trolley = trolley
    context.trolley_token = trolley.token
    context.price_band_code = None
    context.ticket_type_code = None
    context.performance_id = None
    context.discounts = None
    context.send_method = None
    context.send_codes = None
    context.seats = None
    context.no_of_tickets = None


@given('my customer has requested some discounts')
@vcr.use_cassette('fixtures/cassettes/reserve-discounts.yaml', record_mode='new_episodes')
def given_my_customer_has_requested_some_discounts(context):
    discounts, meta = context.client.get_discounts(
        context.performance.id,
        context.ticket_type.code,
        context.price_band.code,
    )

    assert_that(discounts, has_length(greater_than(1)))
    context.discounts = [discount.code for discount in discounts[:2]]


@given('my customer wants the tickets posted to them')
@vcr.use_cassette('fixtures/cassettes/reserve-send-methods.yaml', record_mode='new_episodes')
def given_my_customer_wants_tickets_posted_to_them(context):
    send_methods, meta = context.client.get_send_methods(
        context.performance.id,
    )

    assert_that(send_methods, has_length(greater_than(1)))
    send_method = send_methods[1]
    assert_that(send_method.code, equal_to('POST'))
    context.send_method = send_method
    context.send_codes = {'ext_test0': send_method.code}


@given('my customer is requesting specific seats')
def given_my_customer_is_requesting_specific_sets(context):
    seats = context.price_band.get_seats()
    context.seats = [seat.id for seat in seats[:2]]


@given('my customer is requesting unavailable specific seats')
def given_my_customer_is_requesting_unavailable_specific_sets(context):
    context.seats = ['foo', 'bar']


@given('my customer is requesting partially unavailable specific seats')
def given_my_customer_is_requesting_partially_specific_sets(context):
    seats = context.price_band.get_seats()
    real_seat = seats[3].id
    context.seats = ['foo', real_seat]
    context.real_seats = [real_seat]


@when('I reserve the tickets')
@vcr_post.use_cassette('fixtures/cassettes/reserve-reserve.yaml', record_mode='new_episodes')
def when_i_reserve_the_tickets(context):

    token = None
    if hasattr(context, 'trolley_token'):
        token = context.trolley_token

    reservation, _ = context.client.make_reservation(
        token=token,
        performance_id=context.performance_id,
        number_of_seats=context.no_of_tickets,
        ticket_type_code=context.ticket_type_code,
        price_band_code=context.price_band_code,
        discounts=context.discounts,
        send_codes=context.send_codes,
        seats=context.seats,
    )

    assert reservation
    context.reservation = reservation
    context.trolley = reservation.trolley
    context.transaction_uuid = reservation.trolley.transaction_uuid


@when('I add the tickets to the trolley')
@vcr.use_cassette('fixtures/cassettes/trolley-trolley.yaml', record_mode='new_episodes')
def when_i_add_tickets_to_my_trolley(context):

    token = None
    if hasattr(context, 'trolley_token'):
        token = context.trolley_token

    trolley, _ = context.client.get_trolley(
        token=token,
        performance_id=context.performance.id,
        number_of_seats=context.no_of_tickets,
        ticket_type_code=context.ticket_type.code,
        price_band_code=context.price_band.code,
        discounts=context.discounts,
        send_codes=context.send_codes,
        seats=context.seats,
    )

    assert trolley
    context.trolley = trolley


@when('I remove some tickets for "{event_id}" from the trolley')
@vcr.use_cassette('fixtures/cassettes/trolley-trolley.yaml', record_mode='new_episodes')
def when_i_remove_some_tickets_from_the_trolley(context, event_id):

    assert context.trolley

    item_number = None
    for bundle in context.trolley.bundles:
        for order in bundle.orders:
            if order.event.id == event_id:
                item_number = order.item

    assert item_number

    trolley, _ = context.client.get_trolley(
        token=context.trolley.token,
        item_numbers_to_remove=[item_number],
    )

    assert trolley
    context.trolley = trolley


@then('my reservation is successful')
def then_my_reservation_is_successful(context):
    assert_that(context.reservation.minutes_left, greater_than(0))


@then('I get a trolley token')
def then_i_get_a_trolley_token(context):
    assert context.trolley.token


@then('my trolley has some discounts')
def then_my_trolley_has_some_discounts(context):
    discounts = [
        ticket_order.code
        for bundle in context.trolley.bundles
        for order in bundle.orders
        for ticket_order in order.ticket_orders
    ]

    assert_that(discounts, has_length(greater_than(1)))


@then('my trolley contains tickets for "{event_id}"')
def then_my_trolley_contains_tickets_for_event(context, event_id):
    events_ids = context.trolley.get_event_ids()
    assert_that(events_ids, has_item(event_id))


@then('my trolley does not contain tickets for "{event_id}"')
def then_my_trolley_does_not_contain_tickets_for_event(context, event_id):
    events_ids = context.trolley.get_event_ids()
    assert_that(events_ids, is_not(has_item(event_id)))


@then('my trolley contains the requested seats')
def then_my_trolley_contains_the_requested_seats(context):
    order = context.trolley.bundles[0].orders[0]
    seat_ids = [seat.id for seat in order.requested_seats]

    assert_that(seat_ids, has_items(*context.seats))


@then('the trolley falls back to best available')
def then_the_trolley_falls_back_to_best_available(context):
    order = context.trolley.bundles[0].orders[0]

    assert_that(order.requested_seats, is_(None))


@then('my send method is the one I requested')
@vcr.use_cassette('fixtures/cassettes/reserve-status.yaml', record_mode='new_episodes')
def then_my_send_method_is_the_one_i_requested(context):

    status, _ = context.client.get_status(
        context.transaction_uuid,
        # FIXME: this is an internal hack to display send codes for the time
        # being until is part of the default behaviour.
        req_internal_codes=1,
    )

    send_method = status.trolley.bundles[0].orders[0].send_method

    assert send_method
    assert_that(send_method.code, equal_to(context.send_method.code))


@then('I get the requested seats')
def then_i_get_the_requested_seats(context):
    order = context.reservation.trolley.bundles[0].orders[0]
    seat_ids = [seat.id for seat in order.get_seats()]

    assert_that(order.seat_request_status, equal_to('got_all'))
    assert_that(seat_ids, has_items(*context.seats))


@then('I get different seats than requested')
def then_i_get_different_seats_than_requested(context):
    order = context.reservation.trolley.bundles[0].orders[0]
    seat_ids = [seat.id for seat in order.get_seats()]

    assert_that(order.seat_request_status, is_not(equal_to('got_all')))
    assert_that(seat_ids, has_length(context.no_of_tickets))


@then('I get any available seats I requested but not the others')
def then_i_get_any_available_seats_i_requested_but_not_the_others(context):
    order = context.reservation.trolley.bundles[0].orders[0]
    seat_ids = [seat.id for seat in order.get_seats()]

    assert_that(order.seat_request_status, equal_to('got_partial'))
    assert_that(seat_ids, has_length(context.no_of_tickets))
    assert_that(seat_ids, has_items(*context.real_seats))
