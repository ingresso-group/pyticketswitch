import vcr
from behave import when, then


@when(u'I get the reservation')
@vcr.use_cassette('fixtures/cassettes/get-reserve.yaml', record_mode='new_episodes')
def step_impl(context):
    reservation, _ = context.client.get_reservation(context.transaction_uuid)
    assert reservation
    assert reservation.trolley.transaction_uuid == context.transaction_uuid
    context.get_reservation = reservation


@then(u'the reservation response is the same as the original')
def step_impl(context):
    assert context.reservation
    assert context.get_reservation

    assert context.reservation.status == context.get_reservation.status
    assert context.reservation.trolley.transaction_uuid == context.get_reservation.trolley.transaction_uuid
    assert context.reservation.trolley.order_count == context.get_reservation.trolley.order_count
    assert context.reservation.trolley.minutes_left == context.get_reservation.trolley.minutes_left
    assert context.reservation.trolley.token == context.get_reservation.trolley.token
