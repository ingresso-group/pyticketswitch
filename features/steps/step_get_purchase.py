import vcr
from behave import when, then


@when(u'I get the purchase')
@vcr.use_cassette('fixtures/cassettes/get-purchase.yaml', record_mode='new_episodes')
def when_I_get_the_purchase(context):
    purchase, _, _ = context.client.get_purchase(context.transaction_uuid)
    assert purchase
    assert purchase.trolley.transaction_uuid == context.transaction_uuid
    context.get_purchase = purchase


@then(u'the purchase response is the same as the original')
def then_the_purchase_response_is_the_same_as_the_original(context):
    assert context.status
    assert context.get_purchase

    assert context.status.status == context.get_purchase.status
    assert context.status.trolley.transaction_uuid == context.get_purchase.trolley.transaction_uuid
    assert context.status.trolley.order_count == context.get_purchase.trolley.order_count
    assert context.status.trolley.token == context.get_purchase.trolley.token
