import vcr
from behave import when, then, given
from hamcrest import assert_that, is_not, empty, is_, has_length, equal_to


@given('I have a list of performances for event with id "{event_id}"')
@vcr.use_cassette('fixtures/cassettes/performance-list.yaml', record_mode='new_episodes')
def given_i_have_a_list_of_performances(context, event_id):
    performances, _ = context.client.list_performances(event_id)

    if not hasattr(context, 'event_performances'):
        context.event_performances = {}

    context.event_performances[event_id] = performances


@when('I fetch a specific performance')
@vcr.use_cassette('fixtures/cassettes/get-performance.yaml', record_mode='new_episodes')
def when_i_fetch_a_performance(context):
    context.performance_id = context.event_performances['6IF'][3].id
    context.performance = context.client.get_performance(context.performance_id)


@when('I fetch multiple performances')
@vcr.use_cassette('fixtures/cassettes/get-performance.yaml', record_mode='new_episodes')
def when_i_fetch_multiple_performance(context):
    context.performance_ids = [
        context.event_performances['6IF'][3].id,
        context.event_performances['6IF'][4].id,
    ]
    context.performances = context.client.get_performances(context.performance_ids)


@when('I fetch performances for the event "{event_id}"')
@vcr.use_cassette('fixtures/cassettes/performance-list.yaml', record_mode='new_episodes')
def when_i_fetch_performances_for_the_event(context, event_id):
    performances, meta = context.client.list_performances(event_id)

    context.performances = performances
    context.performance_meta = meta


@then('I get a list of performances')
def then_i_get_performances(context):
    assert_that(context.performances, is_not(empty()))


@then('I get one performance')
def then_i_get_one_performance(context):
    assert_that(context.performances, has_length(1))


@then('I get the performance')
def then_i_get_the_performance(context):
    assert_that(context.performance.id, equal_to(context.performance.id))


@then('I get the performances')
def then_i_get_the_performances(context):
    perf_id = context.performance_ids[0]
    assert_that(context.performances[perf_id].id, equal_to(perf_id))
    perf_id = context.performance_ids[1]
    assert_that(context.performances[perf_id].id, equal_to(perf_id))


@then('I get an indication that the performances have names')
def then_meta_has_names(context):
    assert_that(context.performance_meta.has_names, is_(True))


@then('I get an indication that the performance is auto selected')
def then_meta_auto_select(context):
    assert_that(context.performance_meta.auto_select, is_(True))
