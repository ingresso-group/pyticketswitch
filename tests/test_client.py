import pytest
from mock import Mock
from pyticketswitch.client import TicketSwitch
from pyticketswitch import exceptions


@pytest.fixture
def client():
    client = TicketSwitch(user="bilbo", password="baggins")
    return client


class FakeResponse(object):

    def __init__(self):
        self.json = None
        self.status_code = 200


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

    def test_search_events(self, client):
        response = client.search_events()
        assert response is None
