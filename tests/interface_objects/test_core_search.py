from __future__ import absolute_import
import pytest
from mock import Mock
import pyticketswitch
from pyticketswitch import core_objects, interface


@pytest.fixture
def mock_core_event():

    class CoreEventFactory:

        def __call__(self, event_id, has_special_offer=False):

            event = Mock(spec=core_objects.Event)
            event.event_id = event_id
            event.event_token = event_id
            event.classes = []
            event.custom_fields = []
            event.custom_filters = []
            event.cost_range = None
            if has_special_offer:
                event.cost_range = Mock(spec=core_objects.CostRange)
                event.cost_range.best_value_offer = {
                    'full_surcharge': '9.5', 'full_combined': '57.0',
                    'offer_combined': '31.0', 'percentage_saving': '46',
                    'full_seatprice': '47.5', 'absolute_saving': '26.0',
                    'offer_surcharge': '0.0', 'offer_seatprice': '31.0'
                }
                event.cost_range.min_seatprice = '19.0'

            return event

    return CoreEventFactory()


@pytest.fixture
def mock_core_api(monkeypatch):
    core_api = Mock(spec=interface.CoreAPI)
    core_api.username = 'test-user'
    core_api.running_user = None
    monkeypatch.setattr(
        'pyticketswitch.interface_objects.Core.get_core_api',
        Mock(return_value=core_api)
    )
    return core_api


@pytest.fixture
def mock_crypto_block(monkeypatch):
    crypto_block = 'xyz123'
    monkeypatch.setattr(
        'pyticketswitch.interface_objects.Core.get_crypto_block',
        Mock(return_value=crypto_block)
    )
    return crypto_block


class TestSearch:

    def test_search(
        self, monkeypatch, mock_core_api, mock_crypto_block, mock_core_event
    ):
        mock_core_event_one = mock_core_event('6IF')
        mock_core_event_two = mock_core_event('6IE')
        core_search_result_dict = {
            'crypto_block': 'xxxxxx',
            'event': [mock_core_event_one, mock_core_event_two]
        }
        mock_search_result = Mock(return_value=core_search_result_dict)
        mock_core_api.event_search = mock_search_result

        core = pyticketswitch.Core()
        keyword = 'pyticketswitch test'
        events = core.search_events(keyword=keyword)

        mock_core_api.event_search.assert_called_once_with(
            crypto_block=mock_crypto_block, event_token_list=None,
            mime_text_type=None, page_length=None, page_number=None,
            request_avail_details=None, request_cost_range=True,
            request_custom_fields=True, request_extra_info=None,
            request_media=[
                'square', 'landscape', 'triplet_one', 'triplet_two',
                'triplet_three', 'triplet_four', 'triplet_five', 'marquee',
                'seating_plan', 'supplier'
            ],
            request_reviews=None, request_source_info=None,
            request_video_iframe=None, s_airport=None, s_area=None,
            s_auto_range=None, s_city=None, s_class=None, s_coco=None,
            s_critic_rating=None, s_cust_fltr=None, s_dates=None, s_eve=None,
            s_geo_lat=None, s_geo_long=None, s_geo_rad_km=None,
            s_keys=keyword, s_src=None, s_top=None, s_user_rating=None,
            s_ven=None, upfront_data_token=None, request_meta_components=None,
            s_excluded_events=None,
        )
        assert len(events) == 2
        assert events[0].event_id == '6IF'
        assert events[1].event_id == '6IE'

    def test_special_offer_search(
        self, monkeypatch, mock_core_api, mock_crypto_block, mock_core_event
    ):
        # Only 3 out of 5 events have special offer
        mock_core_event_one = mock_core_event('6IF', True)
        mock_core_event_two = mock_core_event('6IE', True)
        mock_core_event_three = mock_core_event('6IG', True)
        mock_core_event_four = mock_core_event('6IA')
        mock_core_event_five = mock_core_event('6IB')
        core_search_result_dict = {
            'crypto_block': 'xxxxxx',
            'event': [
                mock_core_event_one, mock_core_event_two,
                mock_core_event_three, mock_core_event_four,
                mock_core_event_five,
            ]
        }
        mock_search_result = Mock(return_value=core_search_result_dict)
        mock_core_api.event_search = mock_search_result

        core = pyticketswitch.Core()
        keyword = 'pyticketswitch test'
        events = core.search_events(
            keyword=keyword, special_offer_only=True,
        )

        mock_core_api.event_search.assert_called_once_with(
            crypto_block=mock_crypto_block, event_token_list=None,
            mime_text_type=None, page_length=None, page_number=0,
            request_avail_details=None, request_cost_range=True,
            request_custom_fields=True, request_extra_info=None,
            request_media=[
                'square', 'landscape', 'triplet_one', 'triplet_two',
                'triplet_three', 'triplet_four', 'triplet_five', 'marquee',
                'seating_plan', 'supplier'
            ],
            request_reviews=None, request_source_info=None,
            request_video_iframe=None, s_airport=None, s_area=None,
            s_auto_range=None, s_city=None, s_class=None, s_coco=None,
            s_critic_rating=None, s_cust_fltr=None, s_dates=None, s_eve=None,
            s_geo_lat=None, s_geo_long=None, s_geo_rad_km=None,
            s_keys=keyword, s_src=None, s_top=None, s_user_rating=None,
            s_ven=None, upfront_data_token=None, request_meta_components=None,
            s_excluded_events=None,
        )
        assert len(events) == 3
        assert events[0].event_id == '6IF'
        assert events[1].event_id == '6IE'
        assert events[2].event_id == '6IG'

    def test_special_offer_search_multiple_searches_required(
        self, monkeypatch, mock_core_api, mock_crypto_block, mock_core_event
    ):
        """
        Test searching for special offers when number of results required is
        greater than the number returned in the intitial search. This should
        result in 4 core searches (3 small and 1 full search). This test is
        just for testing that the special offer search is doing what is
        expected (the number and size of searches is pretty arbitrary) 4 core
        searches (3 small and 1 full search). This test is
        just for testing that the special offer search is doing what is
        expected (the number and size of searches is pretty arbitrary) 4 core
        searches (3 small and 1 full search). This test is
        just for testing that the special offer search is doing what is
        expected (the number and size of searches is pretty arbitrary) 4 core
        searches (3 small and 1 full search). This test is
        just for testing that the special offer search is doing what is
        expected (the number and size of searches is pretty arbitrary)
        """

        # Only 2 out of 5 events have special offer
        mock_core_event_one = mock_core_event('6IF', True)
        mock_core_event_two = mock_core_event('6IE', True)
        mock_core_event_three = mock_core_event('6IG')
        mock_core_event_four = mock_core_event('6IA')
        mock_core_event_five = mock_core_event('6IB')
        mock_core_event_six = mock_core_event('6IC')
        core_search_result_dict = {
            'crypto_block': 'xxxxxx',
            'event': [
                mock_core_event_one, mock_core_event_two,
                mock_core_event_three, mock_core_event_four,
                mock_core_event_five, mock_core_event_six,
            ]
        }
        mock_search_result = Mock(return_value=core_search_result_dict)
        mock_core_api.event_search = mock_search_result

        core = pyticketswitch.Core()
        keyword = 'pyticketswitch test'
        events = core.search_events(
            keyword=keyword, special_offer_only=True, page_length=3
        )

        mock_core_api.event_search.assert_any_call(
            crypto_block=mock_crypto_block, event_token_list=None,
            mime_text_type=None, page_length=6, page_number=0,
            request_avail_details=None, request_cost_range=True,
            request_custom_fields=True, request_extra_info=None,
            request_media=[
                'square', 'landscape', 'triplet_one', 'triplet_two',
                'triplet_three', 'triplet_four', 'triplet_five', 'marquee',
                'seating_plan', 'supplier'
            ],
            request_reviews=None, request_source_info=None,
            request_video_iframe=None, s_airport=None, s_area=None,
            s_auto_range=None, s_city=None, s_class=None, s_coco=None,
            s_critic_rating=None, s_cust_fltr=None, s_dates=None, s_eve=None,
            s_geo_lat=None, s_geo_long=None, s_geo_rad_km=None,
            s_keys=keyword, s_src=None, s_top=None, s_user_rating=None,
            s_ven=None, upfront_data_token=None, request_meta_components=None,
            s_excluded_events=None,
        )
        assert mock_core_api.event_search.call_count == 4
        assert len(events) == 2
        assert events[0].event_id == '6IF'
        assert events[1].event_id == '6IE'
