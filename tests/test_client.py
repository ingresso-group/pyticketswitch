import pytest
from datetime import datetime
from mock import Mock
from pyticketswitch.client import TicketSwitch
from pyticketswitch import exceptions
from pyticketswitch.interface.event import Event


@pytest.fixture
def client():
    client = TicketSwitch(user="bilbo", password="baggins")
    return client


@pytest.fixture
def fake_func():
    def wrapper(return_value):
        def fake(*args, **kwargs):
            return return_value
        return fake

    return wrapper


class FakeResponse(object):

    def __init__(self, status_code=200, json=None):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


class TestTicketSwitch:

    def test_get_user_path(self, client):
        user_path = client.get_user_path()
        assert user_path == "/bilbo"

    def test_get_user_path_without_user(self):
        client = TicketSwitch(user="", password="baggins")
        with pytest.raises(exceptions.AuthenticationError):
            client.get_user_path()

    def test_get_user_path_with_subuser(self):
        client = TicketSwitch(user="bilbo", password="baggins", sub_user="frodo")
        user_path = client.get_user_path()
        assert user_path == "/bilbo/frodo"

    def test_get_user_path_with_subuser_and_language(self):
        client = TicketSwitch(
            user="bilbo", password="baggins", sub_user="frodo",
            language='ELV'
        )
        user_path = client.get_user_path()
        assert user_path == "/bilbo/frodo/ELV"

    def test_get_user_path_with_language_and_without_subuser(self):
        client = TicketSwitch(user="bilbo", password="baggins", language='ELV')
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

        mock_make_request.assert_called_with('events', {
            'page_no': 0,
            'page_len': 50
        })

        assert len(events) == 2
        event_one, event_two = events

        assert event_one.event_id =='ABC123'
        assert event_two.event_id == 'DEF456'

    def test_search_events_with_keywords(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(keywords=['awesome', 'stuff'])

        mock_make_request.assert_called_with('events', {
            's_keys': 'awesome,stuff',
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_with_start_date(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(start_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events', {
            's_dates': '20160723:',
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_with_end_date(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(end_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events', {
            's_dates': ':20160723',
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_country_code(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(country_code='fj')

        mock_make_request.assert_called_with('events', {
            's_coco': 'fj',
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_city_code(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(city_code='ldn')

        mock_make_request.assert_called_with('events', {
            's_city': 'ldn',
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_geolocation(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(geolocation='51.52961137:-0.10601562:10')

        mock_make_request.assert_called_with('events', {
            's_geo': '51.52961137:-0.10601562:10',
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_include_dead(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(include_dead=True)

        mock_make_request.assert_called_with('events', {
            'include_dead': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_include_non_live(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(include_non_live=True)

        mock_make_request.assert_called_with('events', {
            'include_non_live': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_order_by_popular(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(order_by_popular=True)

        mock_make_request.assert_called_with('events', {
            's_top': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_extra_info(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_extra_info=True)

        mock_make_request.assert_called_with('events', {
            'req_extra_info': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_reviews(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_reviews=True)

        mock_make_request.assert_called_with('events', {
            'req_reviews': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_media(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_media=True)

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
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_cost_range(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_cost_range=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_cost_range_details(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_cost_range_details=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range_details': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_avail_details(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_avail_details=True)

        mock_make_request.assert_called_with('events', {
            'req_avail_details': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_avail_details_with_perfs(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_avail_details_with_perfs=True)

        mock_make_request.assert_called_with('events', {
            'req_avail_details_with_perfs': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_meta_components(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_meta_components=True)

        mock_make_request.assert_called_with('events', {
            'req_meta_components': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_custom_fields(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_custom_fields=True)

        mock_make_request.assert_called_with('events', {
            'req_custom_fields': True,
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_event_list(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(event_ids=['6IF', '6IE'])

        mock_make_request.assert_called_with('events', {
            'event_id_list': ['6IF', '6IE'],
            'page_no': 0,
            'page_len': 50
        })

    def test_search_events_req_cost_range(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(req_cost_range=True)

        mock_make_request.assert_called_with('events', {
            'req_cost_range': True,
            'page_no': 0,
            'page_len': 50
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

    def test_get_event(self, client, monkeypatch):
        event = Event('ABC1')
        search_events = Mock(return_value=[event])
        monkeypatch.setattr(client, 'search_events', search_events)

        result = client.get_event('ABC1', req_media=True, req_cost_range=True)

        search_events.assert_called_with(
            event_ids=['ABC1'],
            req_media=True,
            req_cost_range=True
        )

        assert result is event

    def test_get_event_with_no_events_returned(self, client, monkeypatch):
        search_events = Mock(return_value=[])
        monkeypatch.setattr(client, 'search_events', search_events)

        result = client.get_event('ABC1', req_media=True, req_cost_range=True)

        search_events.assert_called_with(
            event_ids=['ABC1'],
            req_media=True,
            req_cost_range=True
        )

        assert result is None

    def test_get_event_with_no_event_id(self, client):
        result = client.get_event('', req_media=True, req_cost_range=True)

        assert result is None
