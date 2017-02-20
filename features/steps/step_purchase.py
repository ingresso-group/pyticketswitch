import vcr
from behave import given, when, then
from pyticketswitch import Client
from pyticketswitch.payment_methods import CardDetails, RedirectionDetails
from pyticketswitch.customer import Customer
from pyticketswitch.exceptions import PyticketswitchError

@given(u'my account is set up to use a card debitor')
def step_impl(context):
    context.client = Client('demo', 'demopass')

@given(u'my account is set up to use a redirect debitor')
def step_impl(context):
    context.client = Client('demo-redirect', 'demopass')

@given(u'an event with availability')
def step_impl(context):
    context.event_id = '6IF'


@given(u'I have reserved tickets for my customer for this event')
@vcr.use_cassette('fixtures/cassettes/purchase-reservation.yaml', record_mode='new_episodes')
def step_impl(context):
    performances, _ = context.client.list_performances(context.event_id)
    assert performances

    performance = performances[2]
    ticket_types, _ = context.client.get_availability(performance.id)
    assert ticket_types

    ticket_type = ticket_types[0]
    assert ticket_type.price_bands

    price_band = ticket_type.price_bands[0]

    reservation = context.client.make_reservation(
        performance_id=performance.id,
        number_of_seats=2,
        ticket_type_code=ticket_type.code,
        price_band_code=price_band.code,
    )

    assert reservation
    assert reservation.trolley.transaction_uuid
    context.transaction_uuid = reservation.trolley.transaction_uuid


@given(u'my user has provided valid customer information')
def step_impl(context):
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
def step_impl(context):
    context.customer = Customer(
        'Fred',
        'Flinstone',
        ['301 Cobblestone Way'],
        'foobar',
    )


@given(u'my user has provided valid credit card details')
def step_impl(context):
    context.payment_method = CardDetails(
        '4111 1111 1111 1111',
        ccv2='123',
        expiry_month=9,
        expiry_year=2017
    )

@given(u'my user has provided invalid credit card details')
def step_impl(context):
    context.payment_method = CardDetails('LOLWOTISCREDITCARD!')

@when(u'I purchase the tickets')
@vcr.use_cassette('fixtures/cassettes/purchase-purchase.yaml', record_mode='new_episodes')
def step_impl(context):
    client = context.client

    try:
        status = client.make_purchase(
            context.transaction_uuid,
            context.customer,
            payment_method=context.payment_method,
        )
        assert status
        context.exception = None
        context.status = status
    except PyticketswitchError as excp:
        context.exception = excp
        context.status = None



@then(u'the purchase is succesful')
def step_impl(context):
    assert context.exception is None
    assert context.status.status == 'purchased'


@then(u'the purchase fails')
def step_impl(context):
    assert context.exception


@then(u'I get an error indicating that the customer details are incorrect')
def step_impl(context):
    assert context.exception.args[0] == "Country code 'foobar' in customer data is invalid"


@then(u'I get an error indicating that the card details are incorrect')
def step_impl(context):
    assert context.exception.args[0] == "Country code 'foobar' in customer data is invalid"


@then(u'I get a ticketswitch booking reference')
def step_impl(context):
    assert context.status.trolley.transaction_id

@then(u'I get a booking reference from the backend system')
def step_impl(context):
    assert context.status.trolley.bundles[0].orders[0].backend_purchase_reference
