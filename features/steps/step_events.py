import datetime
import vcr
from behave import when, then
from hamcrest import *  # noqa


@when('a search for "{keywords}" keywords is performed')
@vcr.use_cassette('fixtures/cassettes/search-keyword.yaml')
def when_search_by_keyword(context, keywords):
    keywords = keywords.split(', ')
    assert keywords
    context.events = context.client.list_events(keywords=keywords)


@when('a search for events with performances "{start_days}"-"{end_days}" days from now is performed')
@vcr.use_cassette('fixtures/cassettes/search-daterange.yaml')
def when_search_by_daterange(context, start_days, end_days):
    now = datetime.datetime.now()
    start_date = now + datetime.timedelta(days=int(start_days))
    end_date = now + datetime.timedelta(days=int(end_days))
    context.events = context.client.list_events(
        start_date=start_date,
        end_date=end_date
    )


@when(u'a search for events in country with code "{country_code}" is performed')
@vcr.use_cassette('fixtures/cassettes/search-country.yaml')
def when_search_for_country(context, country_code):
    assert country_code
    context.events = context.client.list_events(country_code=country_code)


@when(u'a search for events in city with code "{city}" is performed')
@vcr.use_cassette('fixtures/cassettes/search-city.yaml')
def when_search_for_city(context, city):
    assert city
    context.events = context.client.list_events(city=city)


@when(u'a search for events within "{radius}"km of "{latitude}" lat and "{longitude}" long is performed')
@vcr.use_cassette('fixtures/cassettes/search-geo.yaml')
def when_search_with_geo(context, radius, latitude, longitude):
    assert radius and latitude and longitude
    context.events = context.client.list_events(radius=radius, latitude=latitude, longitude=longitude)


@when(u'a search is performed for page 2 with a page length of 3 is performed')
@vcr.use_cassette('fixtures/cassettes/search-paginated.yaml')
def when_search_with_pages(context):
    context.events = context.client.list_events(page=2, page_length=3)


@when(u'we attempt to fetch events with the ID\'s "{event_ids}"')
@vcr.use_cassette('fixtures/cassettes/get-events-single.yaml')
def when_get_events(context, event_ids):
    event_ids = event_ids.split(', ')
    assert event_ids
    context.events = context.client.get_events(event_ids)


@then('a single event should be returned')
def then_a_single_event(context):
    assert_that(context.events, has_length(1))
    context.event = context.events[0]


@then('a list of "{num}" events should be returned')
def then_a_list_of_num_events(context, num):
    assert_that(context.events, has_length(int(num)))


@then('that event should have the ID of "{event_id}"')
def then_that_event_should_have_the_id_of_event_id(context, event_id):
    assert_that(context.event.id, equal_to(event_id))


@then(u'those events should have the ID\'s "{event_ids}"')
def then_those_events_with_ids(context, event_ids):
    expected_event_ids = event_ids.split(', ')
    actual_event_ids = [event.id for event in context.events]
    for event_id in expected_event_ids:
        assert_that(actual_event_ids, has_item(event_id))
