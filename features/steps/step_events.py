import datetime
import json
import vcr
from behave import when, then
from hamcrest import (assert_that, has_length, equal_to, has_item,
                      greater_than_or_equal_to, less_than_or_equal_to)


@when('a search for "{keywords}" keywords is performed')
@vcr.use_cassette('fixtures/cassettes/search-keyword.yaml', record_mode='new_episodes')
def when_search_by_keyword(context, keywords):
    keywords = keywords.split(', ')
    assert keywords
    context.events = context.client.list_events(keywords=keywords)


@when('a search for "{keywords}" keywords requesting availability is performed')
@vcr.use_cassette('fixtures/cassettes/search-keyword.yaml', record_mode='new_episodes')
def when_search_by_keyword_with_availability(context, keywords):
    keywords = keywords.split(', ')
    assert keywords
    context.events = context.client.list_events(
        keywords=keywords,
        availability=True,
    )


@when('a search for "{keywords}" keywords requesting availability with performances is performed')
@vcr.use_cassette('fixtures/cassettes/search-keyword.yaml', record_mode='new_episodes')
def when_search_by_keyword_with_availability_with_performances(context, keywords):
    keywords = keywords.split(', ')
    assert keywords
    context.events = context.client.list_events(
        keywords=keywords,
        availability_with_performances=True,
    )


@when('a search for "{keywords}" keywords requesting extra info is performed')
@vcr.use_cassette('fixtures/cassettes/search-keyword.yaml', record_mode='new_episodes')
def when_search_by_keyword_with_extra_info(context, keywords):
    keywords = keywords.split(', ')
    assert keywords
    context.events = context.client.list_events(
        keywords=keywords,
        extra_info=True,
    )


@when('a search for "{keywords}" keywords requesting reviews is performed')
@vcr.use_cassette('fixtures/cassettes/search-keyword.yaml', record_mode='new_episodes')
def when_search_by_keyword_with_reviews(context, keywords):
    keywords = keywords.split(', ')
    assert keywords
    context.events = context.client.list_events(
        keywords=keywords,
        reviews=True,
    )


@when('a search for "{keywords}" keywords requesting media is performed')
@vcr.use_cassette('fixtures/cassettes/search-keyword.yaml', record_mode='new_episodes')
def when_search_by_keyword_with_media(context, keywords):
    keywords = keywords.split(', ')
    assert keywords
    context.events = context.client.list_events(
        keywords=keywords,
        media=True,
    )


@when('a search for events with performances "{start_days}"-"{end_days}" days from now is performed')
@vcr.use_cassette('fixtures/cassettes/search-daterange.yaml', record_mode='new_episodes')
def when_search_by_daterange(context, start_days, end_days):
    now = datetime.datetime.now()
    start_date = now + datetime.timedelta(days=int(start_days))
    end_date = now + datetime.timedelta(days=int(end_days))
    context.events = context.client.list_events(
        start_date=start_date,
        end_date=end_date,
        extra_info=True,
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
@vcr.use_cassette('fixtures/cassettes/get-events-single.yaml', record_mode='new_episodes')
def when_get_events(context, event_ids):
    event_ids = event_ids.split(', ')
    assert event_ids
    context.events = context.client.get_events(event_ids)


@when(u'we attempt to fetch events with the ID\'s "{event_ids}" requesting availability')
@vcr.use_cassette('fixtures/cassettes/get-events-single.yaml', record_mode='new_episodes')
def when_get_events_with_availability(context, event_ids):
    event_ids = event_ids.split(', ')
    assert event_ids
    context.events = context.client.get_events(
        event_ids,
        availability=True,
    )


@when(u'we attempt to fetch events with the ID\'s "{event_ids}" requesting availability with performances')
@vcr.use_cassette('fixtures/cassettes/get-events-single.yaml', record_mode='new_episodes')
def when_get_events_with_availability_with_performances(context, event_ids):
    event_ids = event_ids.split(', ')
    assert event_ids
    context.events = context.client.get_events(
        event_ids,
        availability_with_performances=True,
    )


@when(u'we attempt to fetch events with the ID\'s "{event_ids}" requesting extra info')
@vcr.use_cassette('fixtures/cassettes/get-events-single.yaml', record_mode='new_episodes')
def when_get_events_with_extra_info(context, event_ids):
    event_ids = event_ids.split(', ')
    assert event_ids
    context.events = context.client.get_events(event_ids, extra_info=True)


@when(u'we attempt to fetch events with the ID\'s "{event_ids}" requesting reviews')
@vcr.use_cassette('fixtures/cassettes/get-events-single.yaml', record_mode='new_episodes')
def when_get_events_with_reviews(context, event_ids):
    event_ids = event_ids.split(', ')
    assert event_ids
    context.events = context.client.get_events(event_ids, reviews=True)


@when(u'we attempt to fetch events with the ID\'s "{event_ids}" requesting media')
@vcr.use_cassette('fixtures/cassettes/get-events-single.yaml', record_mode='new_episodes')
def when_get_events_with_media(context, event_ids):
    event_ids = event_ids.split(', ')
    assert event_ids
    context.events = context.client.get_events(event_ids, media=True)


@then('a single event should be returned')
def then_a_single_event(context):
    assert_that(context.events, has_length(1))
    if isinstance(context.events, dict):
        context.event = [event for event in context.events.values()][0]
    else:
        context.event = context.events[0]


@then('a list of "{num}" events should be returned')
def then_a_list_of_num_events(context, num):
    assert_that(context.events, has_length(int(num)))


@then('the events all have a performance between "{start}" and "{end}" days from now')
def then_events_have_performance_between_days(context, start, end):
    assert len(context.events) > 0
    now = datetime.datetime.now()
    start_date = now + datetime.timedelta(days=int(start))
    end_date = now + datetime.timedelta(days=int(end))

    for event in context.events:
        performances = context.client.get_performances(event.id, page_length=100, page=0)

        if any(performance.date_time >= start_date and
               performance.date_time <= end_date
               for performance in performances):
            continue

        raise Exception('Event with id %s does not have a performance inside the given date range' % event.id)



@then('that event should have the ID of "{event_id}"')
def then_that_event_should_have_the_id_of_event_id(context, event_id):
    assert_that(context.event.id, equal_to(event_id))


@then(u'those events should have the ID\'s "{event_ids}"')
def then_those_events_with_ids(context, event_ids):
    expected_event_ids = event_ids.split(', ')
    if isinstance(context.events, dict):
        actual_event_ids = [event.id for event in context.events.values()]
    else:
        actual_event_ids = [event.id for event in context.events]

    for event_id in expected_event_ids:
        assert_that(actual_event_ids, has_item(event_id))


@then('the event has availability details')
def then_the_event_has_availability(context):
    assert context.event.availability_details
    context.availability_details = context.event.availability_details


@then('the availability details have performance information')
def then_the_availability_details_has_performance_info(context):
    now = datetime.datetime.now()
    next_month = now + datetime.timedelta(days=30)
    details = context.availability_details
    print(details[0]._calendar_masks)
    assert details[0].get_month_mask(
        next_month.year,
        next_month.month,
    )


@then(u'the event has content information')
def then_the_event_has_content_info(context):
    assert context.event.content
    content = context.event.content
    expected = json.loads(context.text)
    for key, values in expected.items():
        assert_that(content, has_item(key))
        value = content[key]
        expected_value = values['value']
        expected_value_html = values['value_html']
        assert_that(value.value, equal_to(expected_value))
        assert_that(value.value_html, equal_to(expected_value_html))


@then(u'the event has event information')
def then_the_event_has_event_info(context):
    assert context.event.event_info
    assert context.event.event_info_html
    expected = json.loads(context.text)
    assert_that(context.event.event_info, equal_to(expected['value']))
    assert_that(context.event.event_info_html, equal_to(expected['value_html']))


@then(u'the event has event information starting with')
def then_the_event_has_event_info_starting_with(context):
    assert context.event.event_info
    assert context.event.event_info_html
    expected = json.loads(context.text)
    sample_size = len(expected['value'])
    assert_that(context.event.event_info[:sample_size], equal_to(expected['value']))
    sample_size = len(expected['value_html'])
    assert_that(context.event.event_info_html[:sample_size], equal_to(expected['value_html']))


@then(u'the event has venue information')
def then_the_event_has_venue_info(context):
    assert context.event.venue_addr
    assert context.event.venue_addr_html
    expected = json.loads(context.text)
    assert_that(context.event.venue_addr, equal_to(expected['value']))
    assert_that(context.event.venue_addr_html, equal_to(expected['value_html']))


@then(u'the event has "{reviews}" reviews')
def then_the_event_has_reviews(context, reviews):
    assert context.event.reviews
    assert_that(context.event.reviews, has_length(int(reviews)))


@then(u'the event has media')
def then_the_event_has_media(context):
    assert context.event.media
    media = context.event.media
    expected = json.loads(context.text)
    for key, values in expected.items():
        assert_that(media, has_item(key))
        item = media[key]
        assert_that(item.caption, equal_to(values['caption']))
        assert_that(item.caption_html, equal_to(values['caption_html']))
        assert_that(item.name, equal_to(values['name']))
        assert_that(item.url, equal_to(values['url']))
        assert_that(item.secure, equal_to(values['secure']))
        assert_that(item.width, equal_to(values['width']))
        assert_that(item.height, equal_to(values['height']))
