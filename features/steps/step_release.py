import vcr
from behave import when, then

vcr_post = vcr.VCR(match_on=('method', 'scheme', 'host', 'port', 'path', 'query', 'body'))


@when('I release the reservation')
@vcr_post.use_cassette('fixtures/cassettes/release.yaml', record_mode='new_episodes')
def when_i_release_the_reservation(context):
    assert context.transaction_uuid
    success = context.client.release_reservation(context.transaction_uuid)

    context.release_success = success


@then('the reservation is successfully released')
def the_reservation_is_successfully_released(context):
    assert context.release_success
