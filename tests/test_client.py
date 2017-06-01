import pytest
import json
import requests
from datetime import datetime
from mock import Mock
from pyticketswitch.client import Client, POST
from pyticketswitch import exceptions
from pyticketswitch.trolley import Trolley
from pyticketswitch.reservation import Reservation
from pyticketswitch.user import User
from pyticketswitch.customer import Customer
from pyticketswitch.payment_methods import CardDetails, RedirectionDetails
from pyticketswitch.status import Status
from pyticketswitch.callout import Callout


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
    mock_make_request = Mock(return_value=response)
    monkeypatch.setattr(client, 'make_request', mock_make_request)
    return mock_make_request


@pytest.fixture
def mock_make_request_for_events(client, monkeypatch):
    response = {'events_by_id': {}}
    mock_make_request = Mock(return_value=response)
    monkeypatch.setattr(client, 'make_request', mock_make_request)
    return mock_make_request


@pytest.fixture
def mock_make_request_for_performances(client, monkeypatch):
    response = {'performances_by_id': {}}
    mock_make_request = Mock(return_value=response)
    monkeypatch.setattr(client, 'make_request', mock_make_request)
    return mock_make_request


@pytest.fixture
def mock_make_request_for_availability(client, monkeypatch):
    response = {'availability': {}}
    mock_make_request = Mock(return_value=response)
    monkeypatch.setattr(client, 'make_request', mock_make_request)
    return mock_make_request


@pytest.fixture
def mock_make_request_for_trolley(client, monkeypatch):
    response = {'trolley_token': 'ABC123'}
    mock_make_request = Mock(return_value=response)
    monkeypatch.setattr(client, 'make_request', mock_make_request)
    return mock_make_request

class FakeResponse(object):

    def __init__(self, status_code=200, json=None):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json

    @property
    def content(self):
        return json.dumps(self._json)


class FakeResponseRaisesValueError(object):

    def __init__(self, status_code=200, json=None):
        self.status_code = status_code
        self._json = json

    def json(self):
        raise ValueError("ERROR")

    @property
    def content(self):
        return json.dumps(self._json)


class TestClient:

    @pytest.mark.integration
    def test_get_url(self, client):
        url = client.get_url('events.v1')
        assert url == 'https://api.ticketswitch.com/f13/events.v1/'

    @pytest.mark.integration
    def test_make_request(self, client, monkeypatch):
        fake_response = FakeResponse(status_code=200, json={"lol": "beans"})
        fake_get = Mock(return_value=fake_response)
        session = Mock(spec=requests.Session)
        session.get = fake_get
        monkeypatch.setattr(client, 'get_session', Mock(return_value=session))

        params = {
            'foo': 'bar',
        }
        client.language='en-GB'
        response = client.make_request('events.v1', params)
        assert response == {'lol': 'beans'}
        fake_get.assert_called_with(
            'https://api.ticketswitch.com/f13/events.v1/',
            params={
                'foo': 'bar',
                'user_id': 'bilbo',
                'user_passwd': 'baggins',
            },
            headers={
                'Accept-Language': 'en-GB',
            }
        )

    @pytest.mark.integration
    def test_make_request_with_post(self, client, monkeypatch):
        fake_response = FakeResponse(status_code=200, json={"lol": "beans"})
        fake_post = Mock(return_value=fake_response)
        session = Mock(spec=requests.Session)
        session.post = fake_post
        monkeypatch.setattr(client, 'get_session', Mock(return_value=session))

        params = {
            'foo': 'bar',
        }
        client.language='en-GB'
        response = client.make_request('events.v1', params, method=POST)
        assert response == {'lol': 'beans'}
        fake_post.assert_called_with(
            'https://api.ticketswitch.com/f13/events.v1/',
            data={
                'foo': 'bar',
                'user_id': 'bilbo',
                'user_passwd': 'baggins',
            },
            headers={
                'Accept-Language': 'en-GB',
            }
        )

    def test_make_request_with_subuser(self, monkeypatch):
        client = Client(user="beatles", password="lovemedo", sub_user="ringo")
        fake_response = FakeResponse(status_code=200, json={"lol": "beans"})
        fake_get = Mock(return_value=fake_response)
        session = Mock(spec=requests.Session)
        session.get = fake_get
        monkeypatch.setattr(client, 'get_session', Mock(return_value=session))

        params = {
            'foo': 'bar',
        }
        client.language='en-GB'
        response = client.make_request('events.v1', params)
        assert response == {'lol': 'beans'}
        fake_get.assert_called_with(
            'https://api.ticketswitch.com/f13/events.v1/',
            params={
                'foo': 'bar',
                'user_id': 'beatles',
                'user_passwd': 'lovemedo',
                'sub_id': 'ringo',
            },
            headers={
                'Accept-Language': 'en-GB',
            }
        )

    def test_make_request_bad_response_with_auth_error(self, client, monkeypatch):
        fake_response = FakeResponse(status_code=400, json={
            'error_code': 3,
            'error_desc': 'User authorisation failure',
        })
        fake_get = Mock(return_value=fake_response)
        session = Mock(spec=requests.Session)
        session.get = fake_get
        monkeypatch.setattr(client, 'get_session', Mock(return_value=session))

        with pytest.raises(exceptions.APIError) as excinfo:
            client.make_request('test.v1', {})

        assert excinfo.value.msg == 'User authorisation failure'
        assert excinfo.value.code == 3
        assert excinfo.value.response is fake_response

    def test_make_request_bad_response_with_error(self, client, monkeypatch):
        fake_response = FakeResponse(status_code=400, json={
            'error_code': 8,
            'error_desc': 'price_band_code needs /pool or /alloc suffix',
        })
        fake_get = Mock(return_value=fake_response)
        session = Mock(spec=requests.Session)
        session.get = fake_get
        monkeypatch.setattr(client, 'get_session', Mock(return_value=session))
        with pytest.raises(exceptions.APIError) as excinfo:
            client.make_request('trolley.v1', {})

        assert excinfo.value.msg == 'price_band_code needs /pool or /alloc suffix'
        assert excinfo.value.code == 8
        assert excinfo.value.response is fake_response

    def test_make_request_bad_response_without_error(self, client, monkeypatch):
        fake_response = FakeResponse(status_code=400, json={})
        fake_get = Mock(return_value=fake_response)
        session = Mock(spec=requests.Session)
        session.get = fake_get
        monkeypatch.setattr(client, 'get_session', Mock(return_value=session))
        with pytest.raises(exceptions.InvalidResponseError):
            client.make_request('trolley.v1', {})

    def test_make_request_410_gone_response(self, client, monkeypatch):
        response_json = {'error_code': 8, 'error_desc': 'transaction failed'}
        fake_response = FakeResponse(status_code=410, json=response_json)
        fake_get = Mock(return_value=fake_response)
        session = Mock(spec=requests.Session)
        session.get = fake_get
        monkeypatch.setattr(client, 'get_session', Mock(return_value=session))
        with pytest.raises(exceptions.CallbackGoneError):
            client.make_request('callback.v1', {})

    def test_make_request_no_contents_raises(self, client, monkeypatch):
        response_json = {'data': 'some data'}
        fake_response = FakeResponseRaisesValueError(status_code=200, json=response_json)
        fake_get = Mock(return_value=fake_response)
        session = Mock(spec=requests.Session)
        session.get = fake_get
        monkeypatch.setattr(client, 'get_session', Mock(return_value=session))
        with pytest.raises(exceptions.InvalidResponseError):
            client.make_request('test.v1', {})

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

    def test_add_optional_kwargs_source_info(self, client):
        params = {}
        client.add_optional_kwargs(params, source_info=True)

        params == {
            'req_src_info': True,
        }

    def test_list_events(self, client, monkeypatch):
        response = {
            'results': {
                'event': [
                    {'event_id': 'ABC123'},
                    {'event_id': 'DEF456'},
                ],
                'paging_status': {
                    'total_unpaged_results': 10,
                },
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }
        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        events, meta = client.list_events()

        mock_make_request.assert_called_with('events.v1', {})

        assert len(events) == 2
        event_one, event_two = events

        assert event_one.id =='ABC123'
        assert event_two.id == 'DEF456'

        assert meta.total_results == 10
        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_list_events_with_keywords(self, client, mock_make_request):
        client.list_events(keywords=['awesome', 'stuff'])

        mock_make_request.assert_called_with('events.v1', {
            'keywords': 'awesome,stuff',
        })

    def test_list_events_with_start_date(self, client, mock_make_request):
        client.list_events(start_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events.v1', {
            'date_range': '20160723:',
        })

    def test_list_events_with_end_date(self, client, mock_make_request):
        client.list_events(end_date=datetime(2016, 7, 23, 0, 7, 25))

        mock_make_request.assert_called_with('events.v1', {
            'date_range': ':20160723',
        })

    def test_list_events_with_start_and_end_date(self, client, mock_make_request):
        client.list_events(
            start_date=datetime(2015, 3, 11, 0, 9, 45),
            end_date=datetime(2016, 7, 23, 0, 7, 25)
        )

        mock_make_request.assert_called_with('events.v1', {
            'date_range': '20150311:20160723',
        })

    def test_list_events_country_code(self, client, mock_make_request):
        client.list_events(country_code='fj')

        mock_make_request.assert_called_with('events.v1', {
            'country_code': 'fj',
        })

    def test_list_events_city_code(self, client, mock_make_request):
        client.list_events(city_code='london-uk')

        mock_make_request.assert_called_with('events.v1', {
            'city_code': 'london-uk',
        })

    def test_list_events_geolocation(self, client, mock_make_request):
        client.list_events(
            latitude=51.52961137,
            longitude=-0.10601562,
            radius=10
        )

        mock_make_request.assert_called_with('events.v1', {
            'circle': '51.52961137:-0.10601562:10',
        })

    def test_list_events_invalid_geolocation(self, client):
        with pytest.raises(exceptions.InvalidGeoParameters):
            client.list_events(
                longitude=-0.10601562,
                radius=10
            )

        with pytest.raises(exceptions.InvalidGeoParameters):
            client.list_events(
                latitude=51.52961137,
                radius=10
            )

        with pytest.raises(exceptions.InvalidGeoParameters):
            client.list_events(
                latitude=51.52961137,
                longitude=-0.10601562,
            )

        with pytest.raises(exceptions.InvalidGeoParameters):
            client.list_events(
                radius=10
            )

    def test_list_events_include_dead(self, client, mock_make_request):
        client.list_events(include_dead=True)

        mock_make_request.assert_called_with('events.v1', {
            'include_dead': True,
        })

    def test_list_events_sort_order(self, client, mock_make_request):
        client.list_events(sort_order='foobar')

        mock_make_request.assert_called_with('events.v1', {
            'sort_order': 'foobar',
        })

    def test_list_events_pagination(self, client, mock_make_request):
        client.list_events(page=2, page_length=50)

        mock_make_request.assert_called_with('events.v1', {
            'page_no': 2,
            'page_len': 50,
        })

    def test_list_events_no_results(self, client, monkeypatch, fake_func):
        response = {}
        monkeypatch.setattr(client, 'make_request', fake_func(response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.list_events()

    def test_list_events_misc_kwargs(self, client, mock_make_request):
        client.list_events(foobar='lolbeans')

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
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        events, meta = client.get_events(['ABC123', 'DEF456'])

        mock_make_request.assert_called_with(
            'events_by_id.v1',
            {'event_id_list': 'ABC123,DEF456'},
        )

        event_one = events['ABC123']
        event_two = events['DEF456']

        assert event_one.id == 'ABC123'
        assert event_two.id == 'DEF456'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_get_events_event_list(self, client, mock_make_request_for_events):
        client.get_events(['6IF', '25DR', '3ENO'])

        mock_make_request_for_events.assert_called_with('events_by_id.v1', {
            'event_id_list': '6IF,25DR,3ENO',
        })

    def test_get_events_no_results(self, client, monkeypatch, fake_func):
        response = {}
        monkeypatch.setattr(client, 'make_request', fake_func(response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_events(['6IF', '25DR'])

    def test_get_events_misc_kwargs(self, client, mock_make_request_for_events):
        client.get_events([], foobar='lolbeans')

        mock_make_request_for_events.assert_called_with('events_by_id.v1', {
            'foobar': 'lolbeans'
        })

    def test_get_event(self, client, monkeypatch):
        response = {
            'events_by_id': {
                'ABC123': {
                    'event': {'event_id': 'ABC123'},
                },
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        event, meta = client.get_event('ABC123')

        mock_make_request.assert_called_with(
            'events_by_id.v1',
            {'event_id_list': 'ABC123'},
        )
        assert event.id =='ABC123'
        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_get_months(self, client, monkeypatch):
        response = {
            'results': {
                'month': [
                    {'month': 'dec', 'year': 2016},
                    {'month': 'jan', 'year': 2017},
                    {'month': 'feb', 'year': 2017},
                ]
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        months = client.get_months('ABC123')

        mock_make_request.assert_called_with(
            'months.v1',
            {'event_id': 'ABC123'},
        )

        assert len(months) == 3

        assert months[0].month == 12
        assert months[0].year == 2016
        assert months[1].month == 1
        assert months[1].year == 2017
        assert months[2].month == 2
        assert months[2].year == 2017

    def test_get_months_no_results(self, client, monkeypatch, fake_func):
        response = {}
        monkeypatch.setattr(client, 'make_request', fake_func(response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_months('6IF')

    def test_get_months_misc_kwargs(self, client, mock_make_request):
        client.get_months('6IF', foobar='lolbeans')

        mock_make_request.assert_called_with('months.v1', {
            'event_id': '6IF',
            'foobar': 'lolbeans'
        })

    def test_list_performances_no_results(self, client, monkeypatch, fake_func):
        response = {}
        monkeypatch.setattr(client, 'make_request', fake_func(response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.list_performances('6IF')

    def test_list_performances(self, client, monkeypatch):
        response = {
            'results': {
                'has_perf_names': False,
                'events_by_id': {
                    'ABC123': {'event': {'event_id': 'ABC123'}},
                },
                'performance': [
                    {'perf_id': 'ABC123-1', 'event_id': 'ABC123'},
                    {'perf_id': 'ABC123-2', 'event_id': 'ABC123'},
                    {'perf_id': 'ABC123-3', 'event_id': 'ABC123'},
                ],
                'paging_status': {
                    'total_unpaged_results': 10,
                },
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        performances, meta = client.list_performances('ABC123')

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
        })

        assert len(performances) == 3

        performance_one, performance_two, performance_three = performances

        assert performance_one.id == 'ABC123-1'
        assert performance_two.id == 'ABC123-2'
        assert performance_three.id == 'ABC123-3'

        assert performance_one.event_id == 'ABC123'
        assert performance_two.event_id == 'ABC123'
        assert performance_three.event_id == 'ABC123'

        assert meta.has_names is False
        assert meta.total_results == 10

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_list_performances_cost_range(self, client, mock_make_request):
        client.list_performances('ABC123', cost_range=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True
        })

    def test_list_performances_best_value_offer(self, client, mock_make_request):
        client.list_performances('ABC123', best_value_offer=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_best_value_offer': True
        })

    def test_list_performances_max_saving_offer(self, client, mock_make_request):
        client.list_performances('ABC123', max_saving_offer=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_max_saving_offer': True
        })

    def test_list_performances_min_cost_offer(self, client, mock_make_request):
        client.list_performances('ABC123', min_cost_offer=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_min_cost_offer': True
        })

    def test_list_performances_top_price_offer(self, client, mock_make_request):
        client.list_performances('ABC123', top_price_offer=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_top_price_offer': True
        })

    def test_list_performances_no_singles_data(self, client, mock_make_request):
        client.list_performances('ABC123', no_singles_data=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_cost_range': True,
            'req_cost_range_no_singles_data': True
        })

    def test_list_performances_availability(self, client, mock_make_request):
        client.list_performances('ABC123', availability=True)

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_avail_details': True
        })

    def test_list_performances_pagination(self, client, mock_make_request):
        client.list_performances(
            'ABC123',
            availability=True,
            page=3,
            page_length=20,
        )

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'req_avail_details': True,
            'page_no': 3,
            'page_len': 20,
        })

    def test_list_performances_with_start_date(self, client, mock_make_request):
        client.list_performances(
            'ABC123',
            start_date=datetime(2016, 7, 23, 0, 7, 25)
        )

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'date_range': '20160723:',
        })

    def test_list_performancess_with_end_date(self, client, mock_make_request):
        client.list_performances(
            'ABC123',
            end_date=datetime(2016, 7, 23, 0, 7, 25)
        )

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'date_range': ':20160723',
        })

    def test_list_performances_with_start_and_end_date(self, client, mock_make_request):
        client.list_performances(
            'ABC123',
            start_date=datetime(2015, 3, 11, 0, 9, 45),
            end_date=datetime(2016, 7, 23, 0, 7, 25)
        )

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'date_range': '20150311:20160723',
        })

    def test_list_performances_misc_kwargs(self, client, mock_make_request):
        client.list_performances('ABC123', foobar='lolbeans')

        mock_make_request.assert_called_with('performances.v1', {
            'event_id': 'ABC123',
            'foobar': 'lolbeans',
        })

    def test_get_performances(self, client, monkeypatch):
        response = {
            'performances_by_id': {
                'ABC123-1': {
                    'perf_id': 'ABC123-1',
                    'event_id': 'ABC123',
                },
                'DEF456-2': {
                    'perf_id': 'DEF456-2',
                    'event_id': 'DEF456',
                }
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        performances, meta = client.get_performances(['ABC123-1', 'DEF456-2'])

        mock_make_request.assert_called_with('performances_by_id.v1', {
            'perf_id_list': 'ABC123-1,DEF456-2',
        })

        performance_one = performances['ABC123-1']
        performance_two = performances['DEF456-2']

        assert performance_one.id == 'ABC123-1'
        assert performance_two.id == 'DEF456-2'

        assert performance_one.event_id == 'ABC123'
        assert performance_two.event_id == 'DEF456'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_get_performances_no_performances(self, client, monkeypatch, fake_func):
        response = {}
        monkeypatch.setattr(client, 'make_request', fake_func(response))

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_performances(['6IF-1', '6IF-2'])

    def test_get_performances_misc_kwargs(self, client, mock_make_request_for_performances):
        client.get_performances(['6IF-1', '25DR-2'], foobar='lolbeans')

        mock_make_request_for_performances.assert_called_with('performances_by_id.v1', {
            'perf_id_list': '6IF-1,25DR-2',
            'foobar': 'lolbeans',
        })

    def test_get_performance(self, client, monkeypatch):
        response = {
            'performances_by_id': {
                'ABC123-1': {
                    'perf_id': 'ABC123-1',
                    'event_id': 'ABC123',
                },
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        performance, meta = client.get_performance('ABC123-1')

        mock_make_request.assert_called_with(
            'performances_by_id.v1',
            {'perf_id_list': 'ABC123-1'},
        )
        assert performance.id =='ABC123-1'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_get_availability(self, client, monkeypatch):
        response = {
            'availability': {
                'ticket_type': [
                    {
                        'ticket_type_code': 'CIRCLE',
                        'price_band': [
                            {
                                'price_band_code': 'A',
                            },
                            {
                                'price_band_code': 'B',
                                'allows_leaving_single_seats': 'if_necessary',
                            },
                        ]
                    },
                    {
                        'ticket_type_code': 'STALLS',
                        'price_band': [
                            {
                                'price_band_code': 'C',
                                'allows_leaving_single_seats': 'always',
                            },
                            {
                                'price_band_code': 'D',
                                'allows_leaving_single_seats': 'never',
                            },
                        ]
                    }
                ]
            },

            'backend_is_broken': False,
            'backend_is_down': False,
            'backend_throttle_failed': False,
            'contiguous_seat_selection_only': True,
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            },
            'valid_quantities': [2, 3, 4, 5, 6, 7],
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        availability, meta = client.get_availability('ABC123-1')

        mock_make_request.assert_called_with('availability.v1', {
            'perf_id': 'ABC123-1',
        })

        assert meta.contiguous_seat_selection_only is True
        assert meta.default_currency_code == 'gbp'
        assert meta.valid_quantities == [2, 3, 4, 5, 6, 7]

        assert len(availability) == 2

        ticket_type_one = availability[0]
        assert ticket_type_one.code == 'CIRCLE'

        assert len(ticket_type_one.price_bands) == 2

        price_band_one = ticket_type_one.price_bands[0]
        assert price_band_one.code == 'A'

        price_band_two = ticket_type_one.price_bands[1]
        assert price_band_two.code == 'B'
        assert price_band_two.allows_leaving_single_seats == 'if_necessary'

        ticket_type_two = availability[1]
        assert ticket_type_two.code == 'STALLS'

        assert len(ticket_type_two.price_bands) == 2

        price_band_three = ticket_type_two.price_bands[0]
        assert price_band_three.code == 'C'
        assert price_band_three.allows_leaving_single_seats == 'always'

        price_band_four = ticket_type_two.price_bands[1]
        assert price_band_four.code == 'D'
        assert price_band_four.allows_leaving_single_seats == 'never'

    def test_get_availability_with_number_of_seats(self, client, mock_make_request_for_availability):
        client.get_availability('6IF-1', number_of_seats=2)

        mock_make_request_for_availability.assert_called_with('availability.v1', {
            'perf_id': '6IF-1',
            'no_of_seats': 2,
        })

    def test_get_availability_with_discounts(self, client, mock_make_request_for_availability):
        client.get_availability('6IF-1', discounts=True)

        mock_make_request_for_availability.assert_called_with('availability.v1', {
            'perf_id': '6IF-1',
            'add_discounts': True
        })

    def test_get_availability_with_example_seats(self, client, mock_make_request_for_availability):
        client.get_availability('6IF-1', example_seats=True)

        mock_make_request_for_availability.assert_called_with('availability.v1', {
            'perf_id': '6IF-1',
            'add_example_seats': True
        })

    def test_get_availability_with_seat_blocks(self, client, mock_make_request_for_availability):
        client.get_availability('6IF-1', seat_blocks=True)

        mock_make_request_for_availability.assert_called_with('availability.v1', {
            'perf_id': '6IF-1',
            'add_seat_blocks': True
        })

    def test_get_availability_with_user_commission(self, client, mock_make_request_for_availability):
        client.get_availability('6IF-1', user_commission=True)

        mock_make_request_for_availability.assert_called_with('availability.v1', {
            'perf_id': '6IF-1',
            'add_user_commission': True,
        })

    def test_get_availability_no_availability(self, client, monkeypatch):
        response = {
            'backend_is_broken': False,
            'backend_is_down': False,
            'backend_throttle_failed': False,
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        with pytest.raises(exceptions.InvalidResponseError):
            _, _ = client.get_availability('ABC123-1')

    def test_get_send_methods(self, client, monkeypatch):
        response = {
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            },
            'send_methods': {
                'send_method': [
                    {'send_code': 'COBO'},
                    {'send_code': 'POST'}
                ]
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        send_methods, meta = client.get_send_methods('ABC123-1')

        mock_make_request.assert_called_with('send_methods.v1', {
            'perf_id': 'ABC123-1',
        })

        assert len(send_methods) == 2
        assert send_methods[0].code == 'COBO'
        assert send_methods[1].code == 'POST'

        assert meta.get_currency().code == 'gbp'

    def test_get_send_methods_bad_data(self, client, monkeypatch):
        mock_make_request = Mock(return_value={})
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_send_methods('ABC123-1')

    def test_get_discounts(self, client, monkeypatch):
        response = {
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            },
            'discounts': {
                'discount': [
                    {'discount_code': 'ADULT'},
                    {'discount_code': 'CHILD'}
                ]
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        discounts, meta = client.get_discounts('ABC123-1', 'STALLS', 'A/pool')

        mock_make_request.assert_called_with('discounts.v1', {
            'perf_id': 'ABC123-1',
            'ticket_type_code': 'STALLS',
            'price_band_code': 'A/pool',
        })

        assert len(discounts) == 2
        assert discounts[0].code == 'ADULT'
        assert discounts[1].code == 'CHILD'

        assert meta.get_currency().code == 'gbp'

    def test_get_discounts_bad_data(self, client, monkeypatch):
        mock_make_request = Mock(return_value={})
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        with pytest.raises(exceptions.InvalidResponseError):
            client.get_discounts('ABC123-1', 'STALLS', 'A/pool')

    def test_trolley_params_with_trolley_token(self, client):
        params = client._trolley_params(token='DEF456')

        assert params == {'trolley_token': 'DEF456'}

    def test_trolley_params_with_performance_id(self, client):
        params = client._trolley_params(performance_id='6IF-A8B')

        assert params == {'perf_id': '6IF-A8B'}

    def test_trolley_params_with_number_of_seats(self, client):
        params = client._trolley_params(number_of_seats=3)

        assert params == {'no_of_seats': 3}

    def test_trolley_params_with_ticket_type_code(self, client):
        params = client._trolley_params(ticket_type_code='STALLS')

        assert params == {'ticket_type_code': 'STALLS'}

    def test_trolley_params_with_price_band_code(self, client):
        params = client._trolley_params(price_band_code='A')

        assert params == {
            'price_band_code': 'A'
        }

    def test_trolley_params_with_item_numbers_to_remove(self, client):
        params = client._trolley_params(item_numbers_to_remove=[1, 2, 3], token='ABC123')

        assert params == {
            'trolley_token': 'ABC123',
            'remove_items_list': '1,2,3'
        }

    def test_trolley_params_with_item_numbers_to_remove_with_no_token(self, client):
        with pytest.raises(exceptions.InvalidParametersError):
            client._trolley_params(item_numbers_to_remove=[1, 2, 3])

    def test_trolley_params_with_seats(self, client):
        params = client._trolley_params(seats=['A12', 'B13', 'C14'])

        assert params == {
            'seat0': 'A12',
            'seat1': 'B13',
            'seat2': 'C14',
        }

    def test_trolley_params_with_discounts(self, client):
        params = client._trolley_params(discounts=['ADULT', 'CHILD', 'SENIOR'])

        assert params == {
            'disc0': 'ADULT',
            'disc1': 'CHILD',
            'disc2': 'SENIOR',
        }

    def test_trolley_params_with_send_codes(self, client):
        params = client._trolley_params(send_codes={'nimax': 'POST', 'see': 'COBO'})

        assert params == {
            'nimax_send_code': 'POST',
            'see_send_code': 'COBO'
        }

    def test_trolley_params_with_invalid_send_codes(self, client):
        with pytest.raises(exceptions.InvalidParametersError):
            client._trolley_params(send_codes=['POST', 'COBO'])

    def test_get_trolley(self, client, monkeypatch):
        response = {
            'trolley_contents': {},
            'trolley_token': 'DEF456',
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        trolley, meta = client.get_trolley()

        mock_make_request.assert_called_with('trolley.v1', {})

        assert isinstance(trolley, Trolley)
        assert trolley.token == 'DEF456'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_make_reservation(self, client, monkeypatch):
        response = {
            'reserved_trolley': {
                'transaction_uuid': 'DEF456'
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        reservation, meta = client.make_reservation()

        mock_make_request.assert_called_with('reserve.v1', {}, method=POST)

        assert isinstance(reservation, Reservation)
        assert reservation.trolley.transaction_uuid == 'DEF456'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_get_status(self, client, monkeypatch):
        response = {
            'trolley_contents': {
                'transaction_uuid': 'DEF456'
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        status, meta = client.get_status(
            transaction_uuid='DEF456',
            customer=True,
            external_sale_page=True,
        )

        mock_make_request.assert_called_with('status.v1', {
            'transaction_uuid': 'DEF456',
            'add_customer': True,
            'add_external_sale_page': True,
        })

        assert isinstance(status, Status)
        assert status.trolley.transaction_uuid == 'DEF456'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_get_status_with_trans(self, client, monkeypatch):
        response = {
            'trolley_contents': {
                'transaction_id': 'DEF456'
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        status, meta = client.get_status(
            transaction_id='DEF456',
            customer=True,
            external_sale_page=True,
        )

        mock_make_request.assert_called_with('trans_id_status.v1', {
            'transaction_id': 'DEF456',
            'add_customer': True,
            'add_external_sale_page': True,
        })

        assert isinstance(status, Status)
        assert status.trolley.transaction_id == 'DEF456'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_test(self, client, monkeypatch):
        response = {'user_id': 'foobar'}

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        user = client.test()

        mock_make_request.assert_called_with('test.v1', {})

        assert isinstance(user, User)
        assert user.id == 'foobar'

    def test_release_reservation(self, client, monkeypatch):
        response = {'released_ok': True}

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        released = client.release_reservation('abc123')

        mock_make_request.assert_called_with('release.v1', {
            'transaction_uuid': 'abc123',
        }, method=POST)

        assert released is True

    def test_make_purchase_card_details(self, client, monkeypatch):
        response = {
            'transaction_status': 'purchased',
            'trolley_contents': {
                'transaction_uuid': 'DEF456'
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        customer = Customer('fred', 'flintstone', ['301 cobblestone way'], 'us')
        card_details = CardDetails(
            '4111 1111 1111 1111',
            expiry_year=17,
            expiry_month=3,
        )
        status, callout, meta = client.make_purchase(
            'abc123',
            customer,
            payment_method=card_details
        )

        expected_params = {
            'transaction_uuid': 'abc123',
            'first_name': 'fred',
            'last_name': 'flintstone',
            'address_line_one': '301 cobblestone way',
            'country_code': 'us',
            'card_number': '4111 1111 1111 1111',
            'expiry_date': '0317',
            'supplier_can_use_customer_data': False,
            'user_can_use_customer_data': False,
            'world_can_use_customer_data': False,
            'send_confirmation_email': True,
        }

        mock_make_request.assert_called_with(
            'purchase.v1',
            expected_params,
            method=POST
        )

        assert callout is None
        assert isinstance(status, Status)
        assert status.trolley.transaction_uuid == 'DEF456'
        assert status.status == 'purchased'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_make_purchase_redirection(self, client, monkeypatch):
        response = {
            "callout": {
                "bundle_source_code": "ext_test0",
            },
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        customer = Customer('fred', 'flintstone', ['301 cobblestone way'], 'us')

        redirection_details = RedirectionDetails(
            token='abc123',
            url='https://myticketingco.biz/confirmation/abc123',
            user_agent='Mozilla/5.0',
            accept='text/html,text/plain,application/json',
            remote_site='myticketingco.biz',
        )

        status, callout, meta = client.make_purchase(
            'abc123',
            customer,
            payment_method=redirection_details
        )

        expected_params = {
            'transaction_uuid': 'abc123',
            'first_name': 'fred',
            'last_name': 'flintstone',
            'address_line_one': '301 cobblestone way',
            'country_code': 'us',
            'return_token': 'abc123',
            'return_url': 'https://myticketingco.biz/confirmation/abc123',
            'client_http_user_agent': 'Mozilla/5.0',
            'client_http_accept': 'text/html,text/plain,application/json',
            'remote_site': 'myticketingco.biz',
            'supplier_can_use_customer_data': False,
            'user_can_use_customer_data': False,
            'world_can_use_customer_data': False,
            'send_confirmation_email': True,
        }

        mock_make_request.assert_called_with(
            'purchase.v1',
            expected_params,
            method=POST
        )

        assert status is None
        assert isinstance(callout, Callout)
        assert callout.code == 'ext_test0'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code is None

    def test_make_purchase_credit(self, client, monkeypatch):
        response = {
            'transaction_status': 'purchased',
            'trolley_contents': {
                'transaction_uuid': 'DEF456'
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        customer = Customer('fred', 'flintstone', ['301 cobblestone way'], 'us')

        status, callout, meta = client.make_purchase('abc123', customer)

        expected_params = {
            'transaction_uuid': 'abc123',
            'first_name': 'fred',
            'last_name': 'flintstone',
            'address_line_one': '301 cobblestone way',
            'country_code': 'us',
            'supplier_can_use_customer_data': False,
            'user_can_use_customer_data': False,
            'world_can_use_customer_data': False,
            'send_confirmation_email': True,
        }

        mock_make_request.assert_called_with(
            'purchase.v1',
            expected_params,
            method=POST
        )

        assert callout is None
        assert isinstance(status, Status)
        assert status.trolley.transaction_uuid == 'DEF456'
        assert status.status == 'purchased'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_make_purchase_opting_out_of_confirmation_email(self, client, monkeypatch):
        response = {
            'transaction_status': 'purchased',
            'trolley_contents': {
                'transaction_uuid': 'DEF456'
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        customer = Customer('fred', 'flintstone', ['301 cobblestone way'], 'us')

        status, callout, meta = client.make_purchase(
            'abc123',
            customer,
            send_confirmation_email=False
        )

        expected_params = {
            'transaction_uuid': 'abc123',
            'first_name': 'fred',
            'last_name': 'flintstone',
            'address_line_one': '301 cobblestone way',
            'country_code': 'us',
            'supplier_can_use_customer_data': False,
            'user_can_use_customer_data': False,
            'world_can_use_customer_data': False,
        }

        mock_make_request.assert_called_with(
            'purchase.v1',
            expected_params,
            method=POST
        )

        assert callout is None
        assert isinstance(status, Status)
        assert status.trolley.transaction_uuid == 'DEF456'
        assert status.status == 'purchased'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_next_callout(self, client, monkeypatch):
        response = {
            'transaction_status': 'purchased',
            'trolley_contents': {
                'transaction_uuid': 'DEF456'
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        status, callout, meta = client.next_callout(
            'abc123',
            'def456',
            {'foo': 'bar'},
            lol='beans',
        )

        expected_params = {
            'foo': 'bar',
            'lol': 'beans',
        }

        mock_make_request.assert_called_with(
            'callback.v1/this.abc123/next.def456',
            expected_params,
            method=POST
        )

        assert callout is None
        assert isinstance(status, Status)
        assert status.trolley.transaction_uuid == 'DEF456'
        assert status.status == 'purchased'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'

    def test_next_callout_with_additional_callout(self, client, monkeypatch):
        response = {
            "callout": {
                "bundle_source_code": "ext_test0",
            },
            'currency_code': 'gbp',
            'currency_details': {
                'gbp': {
                    'currency_code': 'gbp',
                }
            }
        }

        mock_make_request = Mock(return_value=response)
        monkeypatch.setattr(client, 'make_request', mock_make_request)

        status, callout, meta = client.next_callout(
            'abc123',
            'def456',
            {'foo': 'bar'},
            lol='beans',
        )

        expected_params = {
            'foo': 'bar',
            'lol': 'beans',
        }

        mock_make_request.assert_called_with(
            'callback.v1/this.abc123/next.def456',
            expected_params,
            method=POST
        )

        assert status is None
        assert isinstance(callout, Callout)
        assert callout.code == 'ext_test0'

        assert 'gbp' in meta.currencies
        assert meta.default_currency_code == 'gbp'
