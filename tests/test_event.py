import pytest
from pyticketswitch import exceptions
from pyticketswitch.event import Event
from datetime import datetime
from dateutil.tz import tzoffset


@pytest.fixture
def data():
    return {
        'meta_event_component_events': {
            'event': [{
                'event_id': 'META123'
            }]
        },
        'event_id': 'ABC1',
        'event_status': 'live',
        'event_type': 'simple_ticket',
        'source_desc': 'Super Awesome Ticketer',
        'venue_desc': 'Top Notch Theater',

        'critic_review_percentage': 100,

        'class': [
            {'class_desc': 'Theater'},
            {'class_desc': 'Amazeballs'},
        ],

        #TODO: don't actually know what filters look like yet...
        'filters': [],

        'custom_fields': [
            {'custom_field_name': 'foo_bar'},
            {'custom_field_name': 'lol_beans'},
        ],

        'date_range_start': {
            'iso8601_date_and_time': '2016-07-21T23:57:15+01:00',
        },
        'date_range_end': {
            'iso8601_date_and_time': '2017-09-03T11:30:40+02:00',
        },

        'postcode': 'W6 8DL',
        'city_desc': 'London',
        'country_desc': 'United Kingdom',
        'country_code': 'uk',

        'geo_data': {
            'latitude': 51.49691253,
            'longditude': -0.17223274,
        },

        'max_running_time': 120,
        'min_running_time': 90,

        'has_no_perfs': True,
        'show_perf_time': True,
        'is_seated': True,
        'needs_departure_date': True,
        'needs_duration': True,
        'needs_performance': True,

        'event_upsell_list': {
            'event_id': ['DEF2', 'GHI3', 'JKL4'],
        },
        'cost_range': {
            'max_seatprice': 47,
            'max_surcharge': 0,
            'min_seatprice': 18,
            'min_surcharge': 0,
            'no_singles_cost_range': {
                'max_seatprice': 47,
                'max_surcharge': 0,
                'min_seatprice': 18,
                'min_surcharge': 0,
                'quantity_options': {
                    'valid_quantity_bitmask': 126
                },
                'range_currency': {
                    'currency_code': 'gbp'
                }
            },
            'quantity_options': {
                'valid_quantity_bitmask': 126
            },
            'range_currency': {
                'currency_code': 'gbp'
            }
        },
        'cost_range_details': {
            'ticket_type': [
                {
                    'ticket_type_desc': 'Grand Circle',
                    'price_band': [
                        {
                            'price_band_desc': '',
                            'cost_range': {
                                'quantity_options': {
                                    'valid_quantity_mask': 2046
                                },
                                'max_surcharge': 11.65,
                                'max_seatprice': 59.5,
                                'range_currency': {
                                    'currency_factor': 100,
                                    'currency_places': 2,
                                    'currency_post_symbol': '',
                                    'currency_number': 826,
                                    'currency_pre_symbol': '\xa3',
                                    'currency_code': 'gbp'
                                },
                                'min_surcharge': 11.25,
                                'no_singles_cost_range': {
                                    'quantity_options': {
                                        'valid_quantity_mask': 2046
                                    },
                                    'max_surcharge': 11.65,
                                    'max_seatprice': 59.5,
                                    'range_currency': {
                                        'currency_factor': 100,
                                        'currency_places': 2,
                                        'currency_post_symbol': '',
                                        'currency_number': 826,
                                        'currency_pre_symbol': '\xa3',
                                        'currency_code': 'gbp'
                                    },
                                    'min_surcharge': 11.25,
                                    'min_seatprice': 57.5
                                },
                                'min_seatprice': 57.5
                            },
                            'price_band_code': 'B'
                        },
                    ],
                },
            ],
        },
        'structured_info': {
            'content': {
                'name': 'name',
                'value': 'value',
                'value_html': '<p>value</p>',
            }
        },
        'media': {
            'media_asset': [{
                'caption_html': '',
                'name': 'landscape',
                'secure_complete_url': 'https://d1wx4w35ubmdix.cloudfront.net/shared/event_media/cropper_cloud/24/249fdb60b56ef4217a6049a1ed770f13552bca9c.jpg',
                'supports_http': True,
                'caption': '',
                'host': 'd1wx4w35ubmdix.cloudfront.net',
                'supports_https': True,
                'path': '/shared/event_media/cropper_cloud/24/249fdb60b56ef4217a6049a1ed770f13552bca9c.jpg',
                'insecure_complete_url': 'http://d1wx4w35ubmdix.cloudfront.net/shared/event_media/cropper_cloud/24/249fdb60b56ef4217a6049a1ed770f13552bca9c.jpg'
            }]
        },
        'video_iframe': {
            'video_iframe_host': 'www.youtube.com',
            'video_iframe_supports_http': True,
            'video_iframe_supports_https': True,
            'video_iframe_path': '/embed/-pgZtzDj_7o?list=PL59A1A57EF510F502',
            'video_iframe_caption': '',
            'video_iframe_url_when_insecure': 'http://www.youtube.com/embed/-pgZtzDj_7o?list=PL59A1A57EF510F502',
            'video_iframe_width': 560,
            'video_iframe_height': 315,
            'video_iframe_url_when_secure': 'https://www.youtube.com/embed/-pgZtzDj_7o?list=PL59A1A57EF510F502',
            'video_iframe_caption_html': ''
        },
        'reviews': {
            'review': [
                {
                    'review_body': 'the finest mise-en-sc\xe8ne in the West End',
                    'review_iso8601_date_and_time': '2013-03-30T12:00:00Z',
                    'star_rating': 4,
                    'review_lang': 'en',
                    'review_title': '',
                    'is_user_review': False,
                    'review_date_desc': 'Sat, 30th March 2013',
                    'review_time_desc': '12.00 PM',
                    'review_author': "What's on Stage",
                    'review_original_url': 'http://www.whatsonstage.com/index.php?pg=207&story=E01822737494'
                }
            ]
        },
        'avail_details': {
            'ticket_type': [{
                'ticket_type_desc': 'Grand Circle',
                'price_band': [{
                    'price_band_desc': '',
                    'price_band_code': 'B',
                    'avail_detail': [{
                        'quantity_options': {
                            'valid_quantity_flags': [
                                False,
                                True,
                                True,
                                True,
                                True,
                                True,
                                True,
                                True,
                                True,
                                True,
                                True
                            ]
                        },
                        'available_weekdays': {
                            'wed': True,
                            'sun': True,
                            'fri': True,
                            'tue': True,
                            'mon': False,
                            'thu': True,
                            'sat': True
                        },
                        'available_dates': {
                            'last_yyyymmdd': '20161002',
                            'first_yyyymmdd': '20160906',
                            'nov': {
                                'day_30': False,
                                'day_18': False,
                            },
                            'oct': {
                                'day_30': True,
                                'day_31': False,
                                'day_18': True,
                            },
                        },
                        'avail_currency': {
                            'currency_factor': 100,
                            'currency_places': 2,
                            'currency_post_symbol': '',
                            'currency_number': 826,
                            'currency_pre_symbol': '\xa3',
                            'currency_code': 'gbp'
                        },
                        'seatprice': 57.5,
                        'surcharge': 11.25,
                        'quantity_options': {
                            'valid_quantity_mask': 2046
                        },
                        'day_mask': 21,
                        'available_dates': {
                            'last_yyyymmdd': '20161002',
                            'first_yyyymmdd': '20160906'
                        },
                        'avail_currency': {
                            'currency_factor': 100,
                            'currency_places': 2,
                            'currency_post_symbol': '',
                            'currency_number': 826,
                            'currency_pre_symbol': '\xa3',
                            'currency_code': 'gbp'
                        },
                        'seatprice': 57.5,
                        'surcharge': 11.25
                    }]
                }]
            }]
        }
    }


class TestEvent:

    BST = tzoffset('BST', 3600)
    DRC = tzoffset('DRC', 7200)

    def test_from_api_data(self, data):

        event = Event.from_api_data(data)
        assert event.id is 'ABC1'
        assert event.status == 'live'

        assert event.description is None

        assert event.source == 'Super Awesome Ticketer'
        assert event.event_type == 'simple_ticket'
        assert event.venue == 'Top Notch Theater'

        assert event.critic_review_percentage == 100

        assert event.classes == ['Theater', 'Amazeballs']
        assert event.filters == []

        assert event.start_date == datetime(2016, 7, 21, 23, 57, 15, tzinfo=self.BST)
        assert event.end_date == datetime(2017, 9, 3, 11, 30, 40, tzinfo=self.DRC)

        assert event.postcode == 'W6 8DL'
        assert event.city == 'London'
        assert event.country == 'United Kingdom'
        assert event.country_code == 'uk'
        assert event.latitude == 51.49691253
        assert event.longditude == -0.17223274

        assert event.max_running_time == 120
        assert event.min_running_time == 90

        assert event.show_performance_time is True
        assert event.has_performances is False
        assert event.is_seated is True
        assert event.needs_departure_date is True
        assert event.needs_duration is True
        assert event.needs_performance is True

        assert event.upsell_list == ['DEF2', 'GHI3', 'JKL4']

        assert len(event.content) == 1

        assert len(event.media) == 2
        assert len(event.reviews) == 1

        assert len(event.meta_events) == 1

        assert len(event.fields) == 2

    def test_from_api_data_with_no_event_id(self):
        data = {
            'foo': 'bar',
        }

        with pytest.raises(exceptions.IntegrityError):
            Event.from_api_data(data)

    def test_from_api_data_with_has_no_perfs(self):
        data = {
            'event_id': 'ABC1',
            'has_no_perfs': True,
        }

        event = Event.from_api_data(data)

        assert event.has_performances is False
