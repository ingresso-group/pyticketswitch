from behave import when, then
from hamcrest import (
    assert_that, has_item, is_not
)


@when('I fetch related events for my trolley')
def when_i_fetch_related_events_for_my_trolley(context):
    token = None
    if hasattr(context, 'trolley_token'):
        token = context.trolley_token

    addon_events, upsell_events, _, _ = context.client.get_related_events(
        token=token,
    )

    context.addon_events = addon_events
    context.upsell_events = upsell_events


@when('I fetch related events for the list of event IDs "{event_ids}"')
def when_i_fetch_related_events_for_the_list_of_event_ids(context, event_ids):
    ids = event_ids.split(',')
    addon_events, upsell_events, _, _ = context.client.get_related_events(
        event_ids=ids,
    )

    context.addon_events = addon_events
    context.upsell_events = upsell_events


@then('I get a list of addon events')
def then_i_get_get_a_list_of_addon_events(context):
    assert context.addon_events


@then('I get a list of upsell events')
def then_i_get_get_a_list_of_upsell_events(context):
    assert context.upsell_events


@then('the upsell event list contains "{event_id}"')
def then_the_upsell_event_list_contains_event(context, event_id):
    events = context.upsell_events
    event_ids = [event.id for event in events]
    assert_that(event_ids, has_item(event_id))


@then('the upsell event list does not contain "{event_id}"')
def then_the_upsell_event_list_does_not_contain_event(context, event_id):
    events = context.upsell_events
    event_ids = [event.id for event in events]
    assert_that(event_ids, is_not(has_item(event_id)))
