import pytest
from datetime import datetime
from mock import Mock
from pyticketswitch.client import Client
from pyticketswitch import exceptions


@pytest.fixture
def client():
    client = Client(user="bilbo", password="baggins")
    return client


@pytest.fixture
def fake_func():
    def wrapper(return_value):
        def fake(*args, **kwargs):
            return return_value
        return fake

    return wrapper


@pytest.fixture
def mock_make_request(client, monkeypatch):
    response = {'results': {}}
    fake_response = FakeResponse(status_code=200, json=response)
    mock_make_request = Mock(return_value=fake_response)
    monkeypatch.setattr(client, 'make_request', mock_make_request)
    return mock_make_request

@pytest.fixture
def mock_make_request_for_events(client, monkeypatch):
    response = {'events_by_id': {}}
    fake_response = FakeResponse(status_code=200, json=response)
    mock_make_request = Mock(return_value=fake_response)
    monkeypatch.setattr(client, 'make_request', mock_make_request)
    return mock_make_request


class FakeResponse(object):

    def __init__(self, status_code=200, json=None):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


class TestClient:

    def test_get_user_path(self, client):
        user_path = client.get_user_path()
        assert user_path == "/bilbo"

    def test_get_user_path_without_user(self):
        client = Client(user="", password="baggins")
        with pytest.raises(exceptions.AuthenticationError):
            client.get_user_path()

    def test_get_user_path_with_subuser(self):
        client = Client(user="bilbo", password="baggins", sub_user="frodo")
        user_path = client.get_user_path()
        assert user_path == "/bilbo/frodo"

    def test_get_user_path_with_subuser_and_language(self):
        client = Client(
            user="bilbo", password="baggins", sub_user="frodo",
            language='ELV'
        )
        user_path = client.get_user_path()
        assert user_path == "/bilbo/frodo/ELV"

    def test_get_user_path_with_language_and_without_subuser(self):
        client = Client(user="bilbo", password="baggins", language='ELV')
        user_path = client.get_user_path()
        assert user_path == "/bilbo/-/ELV"

    @pytest.mark.integration
    def test_get_url(self, client):
        url = client.get_url('events.v1')
        assert url == 'https://api.ticketswitch.com/f13/events.v1/bilbo/'

    @pytest.mark.integration
    def test_make_request(self, client, monkeypatch):
        fake_response = FakeResponse()
        fake_get = Mock(return_value=fake_response)
        monkeypatch.setattr('requests.get', fake_get)
        params = {
            'foo': 'bar',
        }
        response = client.make_request('events.v1', params)
        assert response is fake_response
        fake_get.assert_called_with(
            'https://api.ticketswitch.com/f13/events.v1/bilbo/',
            params={
                'foo': 'bar',
                'user_passwd': 'baggins',
            }
        )

    def test_add_optional_kwargs_extra_info(self, client):
        params = {}
        client.add_optional_kwargs(params, extra_info=True)

        assert params == {'req_extra_info': True}

    def test_add_optional_kwargs_reviews(self, client):
        params = {}
        client.add_optional_kwargs(params, reviews=True)

        assert params == {'req_reviews': True}

    def test_add_optional_kwargs_media(self, client):
        params = {}
        client.add_optional_kwargs(params, media=True)

        assert params == {
            'req_media_triplet_one': True,
            'req_media_triplet_two': True,
            'req_media_triplet_three': True,
            'req_media_triplet_four': True,
            'req_media_triplet_five': True,
            'req_media_seating_plan': True,
            'req_media_square': True,
            'req_media_landscape': True,
            'req_media_marquee': True,
            'req_video_iframe': True,
        }

    def test_add_optional_kwargs_cost_range(self, client):
        params = {}
        client.add_optional_kwargs(params, cost_range=True)

        assert params == {'req_cost_range': True}

    def test_add_optional_kwargs_best_value_offer(self, client):
        params = {}
        client.add_optional_kwargs(params, best_value_offer=True)

        assert params == {
            'req_cost_range': True,
            'req_cost_range_best_value_offer': True,
        }

    def test_add_optional_kwargs_max_saving_offer(self, client):
        params = {}
        client.add_optional_kwargs(params, max_saving_offer=True)

        assert params == {
            'req_cost_range': True,
            'req_cost_range_max_saving_offer': True,
        }

    def test_add_optional_kwargs_min_cost_offer(self, client):
        params = {}
        client.add_optional_kwargs(params, min_cost_offer=True)

        assert params == {
            'req_cost_range': True,
            'req_cost_range_min_cost_offer': True,
        }

    def test_add_optional_kwargs_top_price_offer(self, client):
        params = {}
        client.add_optional_kwargs(params, top_price_offer=True)

        params == {
            'req_cost_range': True,
            'req_cost_range_top_price_offer': True,
        }

    def test_add_optional_kwargs_no_singles_data(self, client):
        params = {}
        client.add_optional_kwargs(params, no_singles_data=True)

        assert params == {
            'req_cost_range': True,
            'req_cost_range_no_singles_data': True,
        }

    def test_add_optional_kwargs_cost_range_details(self, client):
        params = {}
        client.add_optional_kwargs(params, cost_range_details=True)

        assert params == {
            'req_cost_range_details': True,
        }

    def test_add_optional_kwargs_avail_details(self, client):
        params = {}
        client.add_optional_kwargs(params, availability=True)

        params == {
            'req_avail_details': True,
        }

    def test_add_optional_kwargs_avail_details_with_perfs(self, client):
        params = {}
        client.add_optional_kwargs(params, availability_with_performances=True)

        params == {
            'req_avail_details_with_perfs': True,
        }

    def test_add_optional_kwargs_meta_components(self, client):
        params = {}
        client.add_optional_kwargs(params, meta_components=True)

        params == {'req_meta_components': True}

    def test_search_events(self, client, monkeypatch):
        response = {
            'results': {
                'event': [
                    {'event_id': 'ABC123'},
                    {'event_id': 'DEF456'},
                ],
            },
        }
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        events = client.search_events()

        mock_make_request.assert_called_with('events.v1', {})

        assert len(events) == 2
        event_one, event_two = events

        assert event_one.event_id =='ABC123'
        assert event_two.event_id == 'DEF456'

    def test_search_events_with_keywords(self, client, mock_make_request):
        client.search_events(keywords=['awesome', 'stuff'])

        mock_make_request.assert_called_with('events.v1', {
            's_keys': 'awesome,stuff',
        })

    def test_search_events_with_start_date(self, client, mock_make_request):
        client.search_events(start_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events.v1', {
            's_dates': '20160723:',
        })

    def test_search_events_with_end_date(self, client, mock_make_request):
        client.search_events(end_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events.v1', {
            's_dates': ':20160723',
        })

    def test_search_events_with_start_and_end_date(self, client, mock_make_request):
        client.search_events(
            start_date=datetime(2015, 3, 11, 0, 9, 45),
            end_date=datetime(2016, 7, 23, 0, 7, 25)
        )

        mock_make_request.assert_called_with('events.v1', {
            's_dates': '20150311:20160723',
        })

    def test_search_events_country_code(self, client, mock_make_request):
        client.search_events(country_code='fj')

        mock_make_request.assert_called_with('events.v1', {
            's_coco': 'fj',
        })

    def test_search_events_city_code(self, client, mock_make_request):
        client.search_events(city='ldn')

        mock_make_request.assert_called_with('events.v1', {
            's_city': 'ldn',
        })

    def test_search_events_geolocation(self, client, mock_make_request):
        client.search_events(
            latitude=51.52961137,
            longitude=-0.10601562,
            radius=10
        )

        mock_make_request.assert_called_with('events.v1', {
            's_geo': '51.52961137:-0.10601562:10',
        })

    def test_search_events_invalid_geolocation(self, client):
        with pytest.raises(exceptions.InvalidGeoData):
            client.search_events(
                longitude=-0.10601562,
                radius=10
            )

        with pytest.raises(exceptions.InvalidGeoData):
            client.search_events(
                latitude=51.52961137,
                radius=10
            )

        with pytest.raises(exceptions.InvalidGeoData):
            client.search_events(
                latitude=51.52961137,
                longitude=-0.10601562,
            )

        with pytest.raises(exceptions.InvalidGeoData):
            client.search_events(
                radius=10
            )

    def test_search_events_include_dead(self, client, mock_make_request):
        client.search_events(include_dead=True)

        mock_make_request.assert_called_with('events.v1', {
            'include_dead': True,
        })

    def test_search_events_include_non_live(self, client, mock_make_request):
        client.search_events(include_non_live=True)

        mock_make_request.assert_called_with('events.v1', {
            'include_non_live': True,
        })

    def test_search_events_order_by_popular(self, client, mock_make_request):
        client.search_events(order_by_popular=True)

        mock_make_request.assert_called_with('events.v1', {
            's_top': True,
        })

    def test_search_events_pagination(self, client, mock_make_request):
        client.search_events(page=2, page_length=50)

        mock_make_request.assert_called_with('events.v1', {
            'page_no': 2,
            'page_len': 50,
        })

    def test_search_events_invalid_response_code(self, client, monkeypatch, fake_func):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=404, json=response)
        monkeypatch.setattr(client, 'make_request', fake_func(fake_response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.search_events()

    def test_search_events_no_results(self, client, monkeypatch, fake_func):
        response = {}
        fake_response = FakeResponse(status_code=200, json=response)
        monkeypatch.setattr(client, 'make_request', fake_func(fake_response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.search_events()

    def test_search_events_misc_kwargs(self, client, mock_make_request):
        client.search_events(foobar='lolbeans')

        mock_make_request.assert_called_with('events.v1', {
            'foobar': 'lolbeans'
        })

    def test_get_events(self, client, monkeypatch):
        response = {
            'events_by_id': {
                'ABC123': {
                    'event': {'event_id': 'ABC123'},
                },
                'DEF456': {
                    'event': {'event_id': 'DEF456'},
                }
            },
        }

        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        events = client.get_events(['ABC123', 'DEF456'])

        mock_make_request.assert_called_with(
            'events_by_id.v1',
            {'event_id_list': 'ABC123,DEF456'},
        )

        event_one = events['ABC123']
        event_two = events['DEF456']

        assert event_one.event_id =='ABC123'
        assert event_two.event_id == 'DEF456'

    def test_get_events_event_list(self, client, mock_make_request_for_events):
        client.get_events(['6IF', '25DR', '3ENO'])

        mock_make_request_for_events.assert_called_with('events_by_id.v1', {
            'event_id_list': '6IF,25DR,3ENO',
        })

    def test_get_events_misc_kwargs(self, client, mock_make_request_for_events):
        client.get_events([], foobar='lolbeans')

        mock_make_request_for_events.assert_called_with('events_by_id.v1', {
            'foobar': 'lolbeans'
        })

    def test_get_performances_with_meta_event(self, client, monkeypatch):
        response = {
            'results': {
                'events_by_id': {
                    'ABC123': {'event': {'event_id': 'ABC123'}},
                    'DEF456': {'event': {'event_id': 'DEF456'}},
                },
                'performance': [
                    {'perf_id': 'ABC123-1', 'event_id': 'ABC123'},
                    {'perf_id': 'DEF456-1', 'event_id': 'DEF456'},
                    {'perf_id': 'ABC123-2', 'event_id': 'ABC123'},
                ]
            },
        }

        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        performances = client.get_performances('GHI789')

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'GHI789',
        })

        assert len(performances) == 3

        performance_one, performance_two, performance_three = performances

        assert performance_one.performance_id == 'ABC123-1'
        assert performance_two.performance_id == 'DEF456-1'
        assert performance_three.performance_id == 'ABC123-2'

        assert performance_one.event.event_id == 'ABC123'
        assert performance_two.event.event_id == 'DEF456'
        assert performance_three.event.event_id == 'ABC123'

        assert performance_one.event is performance_three.event

    def test_get_performances_invalid_response_code(self, client, monkeypatch, fake_func):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=404, json=response)
        monkeypatch.setattr(client, 'make_request', fake_func(fake_response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_performances('6IF')

    def test_get_performances_no_results(self, client, monkeypatch, fake_func):
        response = {}
        fake_response = FakeResponse(status_code=200, json=response)
        monkeypatch.setattr(client, 'make_request', fake_func(fake_response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_performances('6IF')

    def test_get_performances(self, client, monkeypatch):
        response = {
            'results': {
                'events_by_id': {
                    'ABC123': {'event': {'event_id': 'ABC123'}},
                },
                'performance': [
                    {'perf_id': 'ABC123-1', 'event_id': 'ABC123'},
                    {'perf_id': 'ABC123-2', 'event_id': 'ABC123'},
                    {'perf_id': 'ABC123-3', 'event_id': 'ABC123'},
                ]
            },
        }

        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        performances = client.get_performances('ABC123')

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
        })

        assert len(performances) == 3

        performance_one, performance_two, performance_three = performances

        assert performance_one.performance_id == 'ABC123-1'
        assert performance_two.performance_id == 'ABC123-2'
        assert performance_three.performance_id == 'ABC123-3'

        assert performance_one.event.event_id == 'ABC123'
        assert performance_two.event.event_id == 'ABC123'
        assert performance_three.event.event_id == 'ABC123'

    def test_get_performances_cost_range(self, client, mock_make_request):
        client.get_performances('ABC123', cost_range=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True
        })

    def test_get_performances_best_value_offer(self, client, mock_make_request):
        client.get_performances('ABC123', best_value_offer=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_best_value_offer': True
        })

    def test_get_performances_max_saving_offer(self, client, mock_make_request):
        client.get_performances('ABC123', max_saving_offer=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_max_saving_offer': True
        })

    def test_get_performances_min_cost_offer(self, client, mock_make_request):
        client.get_performances('ABC123', min_cost_offer=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_min_cost_offer': True
        })

    def test_get_performances_top_price_offer(self, client, mock_make_request):
        client.get_performances('ABC123', top_price_offer=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_top_price_offer': True
        })

    def test_get_performances_no_singles_data(self, client, mock_make_request):
        client.get_performances('ABC123', no_singles_data=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_no_singles_data': True
        })

    def test_get_performances_availability(self, client, mock_make_request):
        client.get_performances('ABC123', availability=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_avail_details': True
        })

    def test_get_performances_misc_kwargs(self, client, mock_make_request):
        client.get_performances('ABC123', foobar='lolbeans')

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'foobar': 'lolbeans'
        })
