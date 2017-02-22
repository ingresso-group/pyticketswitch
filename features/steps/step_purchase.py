import vcr
from hashlib import md5
from behave import given, when, then
from hamcrest import assert_that, equal_to, none, not_none
from pyticketswitch import Client
from pyticketswitch.payment_methods import CardDetails, RedirectionDetails
from pyticketswitch.customer import Customer
from pyticketswitch.exceptions import PyticketswitchError


vcr_post = vcr.VCR(match_on=('method', 'scheme', 'host', 'port', 'path', 'query', 'body'))


@given(u'my account is set up to allow a user to buy on credit')
def on_credit_debitor(context):
    context.client = Client('demo', 'demopass')
    context.payment_method = None


@given(u'my account is set up to use a card debitor')
def card_debitor(context):
    context.client = Client('demo-creditcard', 'demopass')


@given(u'my account is set up to use a redirect debitor')
def redirect_debitor(context):
    context.client = Client('demo-redirect', 'demopass')


@given(u'an event with availability')
@vcr_post.use_cassette('fixtures/cassettes/purchase-event-availability.yaml', record_mode='new_episodes')
def event_with_availability(context):
    context.event_id = '6IF'
    performances, _ = context.client.list_performances(context.event_id)
    assert performances

    context.performance = performances[2]
    ticket_types, _ = context.client.get_availability(context.performance.id)
    assert ticket_types

    context.ticket_type = ticket_types[0]
    assert context.ticket_type.price_bands

    context.price_band = context.ticket_type.price_bands[0]


@given(u'I have reserved tickets for my customer for this event')
@vcr_post.use_cassette('fixtures/cassettes/purchase-reservation.yaml', record_mode='new_episodes')
def reserve_tickets_for_this_event(context):

    scenario = context.scenario.name
    key = md5(scenario.encode('utf-8')).hexdigest()

    reservation = context.client.make_reservation(
        performance_id=context.performance.id,
        number_of_seats=2,
        ticket_type_code=context.ticket_type.code,
        price_band_code=context.price_band.code,
        _vcr_scenario_key=key,
    )

    assert reservation
    assert reservation.trolley.transaction_uuid
    context.transaction_uuid = reservation.trolley.transaction_uuid


@given(u'my user has provided valid customer information')
def valid_customer_information(context):
    context.customer = Customer(
        'Fred',
        'Flintstone',
        ['301 Cobblestone Way'],
        'us',
        email='f.flintstone@ingresso.co.uk',
        phone='079000000000',
        post_code='70777',
        town='Bedrock City',
        county='LA',
    )


@given(u'my user has provided invalid customer information')
def invalid_customer_information(context):
    context.customer = Customer(
        'Fred',
        'Flinstone',
        ['301 Cobblestone Way'],
        'foobar',
    )


@given(u'my user has provided valid credit card details')
def valid_credit_card_details(context):
    context.payment_method = CardDetails(
        '4111 1111 1111 1111',
        ccv2='123',
        expiry_month=9,
        expiry_year=17
    )


@given(u'my user has provided invalid credit card details')
def invalid_credit_card_details(context):
    context.payment_method = CardDetails(
        'WOTISCREDITCARD!',
        ccv2='LOL',
        expiry_month=10,
        expiry_year=1,
    )


@when(u'I purchase the tickets')
@vcr_post.use_cassette('fixtures/cassettes/purchase-purchase.yaml', record_mode='new_episodes')
def i_purchase_the_tickets(context):
    client = context.client
    callout = None

    try:
        status, callout = client.make_purchase(
            context.transaction_uuid,
            context.customer,
            payment_method=context.payment_method,
        )
        context.exception = None
        context.status = status
        context.callout = callout
    except PyticketswitchError as excp:
        context.exception = excp
        context.status = None
        context.callout = None


@then(u'the purchase is succesful')
def the_purchase_is_succesful(context):
    assert_that(context.status, not_none())
    assert_that(context.exception, none())
    assert context.status.status == 'purchased'


@then(u'the purchase fails')
def the_purchase_fails(context):
    assert_that(context.status.status, equal_to('failed'))


@then(u'then an exception is raised')
def an_excection_is_raised(context):
    assert_that(context.exception, not_none())


@then(u'I get an error indicating that the customer details are incorrect')
def i_get_an_error_for_bad_customer_details(context):
    assert_that(context.exception.args[0], equal_to("Country code 'foobar' in customer data is invalid"))


@then(u'I get an error indicating that the card details are incorrect')
def i_get_an_error_for_bad_card_details(context):
    assert_that(context.exception.args[0], equal_to("Unknown cards are not accepted"))


@then(u'I get a ticketswitch booking reference')
def i_get_a_ticketswitch_booking_reference(context):
    assert context.status.trolley.transaction_id


@then(u'I get a booking reference from the backend system')
def i_get_a_booking_reference(context):
    assert context.status.trolley.bundles[0].orders[0].backend_purchase_reference


@given(u'I provide a URL and token to return to')
def i_provide_a_return_url_and_token(context):
    context.redirect_counter = 1
    token = '{}.{}'.format(context.transaction_uuid, context.redirect_counter)
    context.this_token = token
    context.payment_method = RedirectionDetails(
        token=token,
        url="https://example.com/{}/".format(token),
        user_agent='iceweasel',
        accept='application/json',
        remote_site='example.com',
    )


@then(u'I get a callout')
def i_get_a_callout(context):
    assert_that(context.exception, none())
    assert_that(context.callout, not_none())


@given(u'I have returned from a successful external payment')
@vcr_post.use_cassette('fixtures/cassettes/purchase-callout.yaml', record_mode='new_episodes')
def i_have_returned_from_a_succesfull_callout(context):
    status, callout = context.client.make_purchase(
        context.transaction_uuid,
        context.customer,
        payment_method=context.payment_method,
    )
    assert_that(status, none())
    assert_that(callout, not_none())

    context.callout = callout
    context.callout_return_params = {'success': 'yes'}


@given(u'I have returned from a failed external payment')
@vcr_post.use_cassette('fixtures/cassettes/purchase-failed-callout.yaml', record_mode='new_episodes')
def i_have_returned_from_a_failed_callout(context):
    status, callout = context.client.make_purchase(
        context.transaction_uuid,
        context.customer,
        payment_method=context.payment_method,
    )
    assert_that(status, none())
    assert_that(callout, not_none())

    context.callout = callout
    context.callout_return_params = {'success': 'no'}


@when(u'I ask for the next redirect')
@vcr_post.use_cassette('fixtures/cassettes/purchase-next-callout.yaml', record_mode='new_episodes')
def i_ask_for_the_next_redirect(context):

    context.redirect_counter += 1
    next_token = '{}.{}'.format(context.transaction_uuid, context.redirect_counter)

    status, callout = context.client.next_callout(
        context.this_token,
        next_token,
        context.callout_return_params
    )

    context.status = status
    context.callout = callout
    context.exception = None
    context.this_token = next_token
