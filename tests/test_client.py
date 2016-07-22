import pytest
from datetime import datetime
from mock import Mock
from pyticketswitch.client import TicketSwitch
from pyticketswitch import exceptions


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

        mock_make_request.assert_called_with('events', {})

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
            's_keys': 'awesome,stuff'
        })

    def test_search_events_with_start_date(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(start_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events', {
            's_dates': '20160723:'
        })

    def test_search_events_with_end_date(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(end_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events', {
            's_dates': ':20160723'
        })

    def test_search_events_country_code(self, client, monkeypatch):
        response = {'results': {}}
        fake_response = FakeResponse(status_code=200, json=response)
        mock_make_request = Mock(return_value=fake_response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        client.search_events(country_code='fj')

        mock_make_request.assert_called_with('events', {'s_coco': 'fj'})

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
