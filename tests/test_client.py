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

    def test_get_end_point(self, client):
        end_point = client.get_end_point('events')
        assert end_point == '/json_events.exe'

    def test_get_end_point_with_non_existant_method(self, client):
        with pytest.raises(exceptions.EndPointMissingError):
            client.get_end_point('buy_stuff')

    @pytest.mark.integration
    def test_get_url(self, client):
        url = client.get_url('events')
        assert url == 'https://api.ticketswitch.com/cgi-bin/json_events.exe/bilbo/'

    @pytest.mark.integration
    def test_make_request(self, client, monkeypatch):
        fake_response = FakeResponse()
        fake_get = Mock(return_value=fake_response)
        monkeypatch.setattr('requests.get', fake_get)
        params = {
            'foo': 'bar',
        }
        response = client.make_request('events', params)
        assert response is fake_response
        fake_get.assert_called_with(
            'https://api.ticketswitch.com/cgi-bin/json_events.exe/bilbo/',
            params={
                'foo': 'bar',
                'user_passwd': 'baggins',
            }
        )

    def test_get_events(self, client, monkeypatch):
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

        events = client.get_events()

        mock_make_request.assert_called_with('events', {})

        assert len(events) == 2
        event_one, event_two = events

        assert event_one.event_id =='ABC123'
        assert event_two.event_id == 'DEF456'

    def test_get_events_with_keywords(self, client, mock_make_request):
        client.get_events(keywords=['awesome', 'stuff'])

        mock_make_request.assert_called_with('events', {
            's_keys': 'awesome,stuff',
        })

    def test_get_events_with_start_date(self, client, mock_make_request):
        client.get_events(start_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events', {
            's_dates': '20160723:',
        })

    def test_get_events_with_end_date(self, client, mock_make_request):
        client.get_events(end_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events', {
            's_dates': ':20160723',
        })

    def test_get_events_with_start_and_end_date(self, client, mock_make_request):
        client.get_events(
            start_date=datetime(2015, 3, 11, 0, 9, 45),
            end_date=datetime(2016, 7, 23, 0, 7, 25)
        )

        mock_make_request.assert_called_with('events', {
            's_dates': '20150311:20160723',
        })

    def test_get_events_country_code(self, client, mock_make_request):
        client.get_events(country_code='fj')

        mock_make_request.assert_called_with('events', {
            's_coco': 'fj',
        })

    def test_get_events_city_code(self, client, mock_make_request):
        client.get_events(city='ldn')

        mock_make_request.assert_called_with('events', {
            's_city': 'ldn',
        })

    def test_get_events_geolocation(self, client, mock_make_request):
        client.get_events(
            latitude=51.52961137,
            longitude=-0.10601562,
            radius=10
        )

        mock_make_request.assert_called_with('events', {
            's_geo': '51.52961137:-0.10601562:10',
        })

    def test_get_events_invalid_geolocation(self, client):
        with pytest.raises(exceptions.InvalidGeoData):
            client.get_events(
                longitude=-0.10601562,
                radius=10
            )

        with pytest.raises(exceptions.InvalidGeoData):
            client.get_events(
                latitude=51.52961137,
                radius=10
            )

        with pytest.raises(exceptions.InvalidGeoData):
            client.get_events(
                latitude=51.52961137,
                longitude=-0.10601562,
            )

        with pytest.raises(exceptions.InvalidGeoData):
            client.get_events(
                radius=10
            )

    def test_get_events_include_dead(self, client, mock_make_request):
        client.get_events(include_dead=True)

        mock_make_request.assert_called_with('events', {
            'include_dead': True,
        })

    def test_get_events_include_non_live(self, client, mock_make_request):
        client.get_events(include_non_live=True)

        mock_make_request.assert_called_with('events', {
            'include_non_live': True,
        })

    def test_get_events_order_by_popular(self, client, mock_make_request):
        client.get_events(order_by_popular=True)

        mock_make_request.assert_called_with('events', {
            's_top': True,
        })

    def test_get_events_extra_info(self, client, mock_make_request):
        client.get_events(extra_info=True)

        mock_make_request.assert_called_with('events', {
            'req_extra_info': True,
        })

    def test_get_events_reviews(self, client, mock_make_request):
        client.get_events(reviews=True)

        mock_make_request.assert_called_with('events', {
            'req_reviews': True,
        })

    def test_get_events_media(self, client, mock_make_request):
        client.get_events(media=True)

        mock_make_request.assert_called_with('events', {
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
        })

    def test_get_events_cost_range(self, client, mock_make_request):
        client.get_events(cost_range=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range': True,
        })

    def test_get_events_best_value_offer(self, client, mock_make_request):
        client.get_events(best_value_offer=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range': True,
            'req_cost_range_best_value_offer': True,
        })

    def test_get_events_max_saving_offer(self, client, mock_make_request):
        client.get_events(max_saving_offer=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range': True,
            'req_cost_range_max_saving_offer': True,
        })

    def test_get_events_min_cost_offer(self, client, mock_make_request):
        client.get_events(min_cost_offer=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range': True,
            'req_cost_range_min_cost_offer': True,
        })

    def test_get_events_top_price_offer(self, client, mock_make_request):
        client.get_events(top_price_offer=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range': True,
            'req_cost_range_top_price_offer': True,
        })

    def test_get_events_no_singles_data(self, client, mock_make_request):
        client.get_events(no_singles_data=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range': True,
            'req_cost_range_no_singles_data': True,
        })

    def test_get_events_cost_range_details(self, client, mock_make_request):
        client.get_events(cost_range_details=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range_details': True,
        })

    def test_get_events_avail_details(self, client, mock_make_request):
        client.get_events(availability=True)

        mock_make_request.assert_called_with('events', {
            'req_avail_details': True,
        })

    def test_get_events_avail_details_with_perfs(self, client, mock_make_request):
        client.get_events(availability_with_performances=True)

        mock_make_request.assert_called_with('events', {
            'req_avail_details_with_perfs': True,
        })

    def test_get_events_meta_components(self, client, mock_make_request):
        client.get_events(meta_components=True)

        mock_make_request.assert_called_with('events', {
            'req_meta_components': True,
        })

    def test_get_events_event_list(self, client, mock_make_request):
        client.get_events(page=2, page_length=50)

        mock_make_request.assert_called_with('events', {
            'page_no': 2,
            'page_len': 50,
        })

    def test_get_events_pagination(self, client, mock_make_request):
        client.get_events(page=2, page_length=50)

        mock_make_request.assert_called_with('events', {
            'page_no': 2,
            'page_len': 50,
        })

    def test_get_events_misc_kwargs(self, client, mock_make_request):
        client.get_events(foobar='lolbeans')

        mock_make_request.assert_called_with('events', {
            'foobar': 'lolbeans'
        })

    def test_get_events_invalid_response_code(self, client, monkeypatch, fake_func):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=404, json=response)
        monkeypatch.setattr(client, 'make_request', fake_func(fake_response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_events()

    def test_get_events_no_results(self, client, monkeypatch, fake_func):
        response = {}
        fake_response = FakeResponse(status_code=200, json=response)
        monkeypatch.setattr(client, 'make_request', fake_func(fake_response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_events()

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

        mock_make_request.assert_called_with('performances', {
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

        mock_make_request.assert_called_with('performances', {
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

        mock_make_request.assert_called_with('performances', {
            'event_id': 'ABC123',
            'req_cost_range': True
        })

    def test_get_performances_best_value_offer(self, client, mock_make_request):
        client.get_performances('ABC123', best_value_offer=True)

        mock_make_request.assert_called_with('performances', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_best_value_offer': True
        })

    def test_get_performances_max_saving_offer(self, client, mock_make_request):
        client.get_performances('ABC123', max_saving_offer=True)

        mock_make_request.assert_called_with('performances', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_max_saving_offer': True
        })

    def test_get_performances_min_cost_offer(self, client, mock_make_request):
        client.get_performances('ABC123', min_cost_offer=True)

        mock_make_request.assert_called_with('performances', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_min_cost_offer': True
        })

    def test_get_performances_top_price_offer(self, client, mock_make_request):
        client.get_performances('ABC123', top_price_offer=True)

        mock_make_request.assert_called_with('performances', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_top_price_offer': True
        })

    def test_get_performances_no_singles_data(self, client, mock_make_request):
        client.get_performances('ABC123', no_singles_data=True)

        mock_make_request.assert_called_with('performances', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_no_singles_data': True
        })

    def test_get_performances_availability(self, client, mock_make_request):
        client.get_performances('ABC123', availability=True)

        mock_make_request.assert_called_with('performances', {
            'event_id': 'ABC123',
            'req_avail_details': True
        })

    def test_get_performances_misc_kwargs(self, client, mock_make_request):
        client.get_performances('ABC123', foobar='lolbeans')

        mock_make_request.assert_called_with('performances', {
            'event_id': 'ABC123',
            'foobar': 'lolbeans'
        })
