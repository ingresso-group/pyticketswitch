from pyticketswitch.interface_objects import Core, Event

from .. import settings_test as settings
from .common import InterfaceObjectTestCase


class CoreTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        self.core = Core(session=session, **self.api_settings)

    def test_search_events_keyword(self):

        events = self.core.search_events(keyword='test')

        self.assertTrue(events)

    def test_search_events_contains_event(self):

        events = self.core.search_events(keyword='test')

        for e in events:
            self.assertIsInstance(e, Event)

    def test_search_events_keyword_paging(self):

        events = self.core.search_events(
            keyword='test', page_length='2', page_number='1'
        )

        self.assertTrue(events)

    def test_search_events_keyword_empty(self):

        events = self.core.search_events(keyword='abc24382hggeouh%$')

        self.assertFalse(events)

    def test_search_events_sort_top(self):

        events = self.core.search_events(
            keyword='test', sort_by='top'
        )

        self.assertTrue(events)

    def test_search_events_sort_user_rating(self):

        events = self.core.search_events(
            keyword='test', sort_by='user_rating'
        )

        self.assertTrue(events)

    def test_search_events_sort_critic_rating(self):

        events = self.core.search_events(
            keyword='test', sort_by='critic_rating'
        )

        self.assertTrue(events)

    def test_search_events_auto_date_range(self):

        for value in settings.AUTO_DATE_RANGE:
            events = self.core.search_events(
                keyword='test', auto_date_range=value
            )

            self.assertTrue(events)

    def test_search_events_cities(self):

        self.core.search_events(keyword='test')

        self.assertIsInstance(self.core.event_cities, dict)
        self.assertIn('london-uk', self.core.event_cities)
        for city, info in self.core.event_cities.items():
            self.assertIsInstance(city, str)
            self.assertIsInstance(info, dict)

            self.assertIn('count', info)
            self.assertIn('description', info)

    def test_search_events_categories(self):

        self.core.search_events(keyword='test')

        self.assertIsInstance(self.core.event_categories, dict)
        self.assertIn('theatre/', self.core.event_categories)
        for cat, info in self.core.event_categories.items():
            self.assertIsInstance(cat, str)
            self.assertIsInstance(info, dict)
            self.assertIn('count', info)
            self.assertIn('category', info)
            self.assertIn('sub_categories', info)

    def test_search_events_countries(self):

        self.core.search_events(keyword='test')

        self.assertIsInstance(self.core.event_countries, dict)
        self.assertIn('uk', self.core.event_countries)
        for country, info in self.core.event_countries.items():
            self.assertIsInstance(country, str)
            self.assertIsInstance(info, dict)

            self.assertIn('count', info)
            self.assertIn('description', info)

    def test_search_events_price_range(self):

        self.core.search_events(keyword='test')

        self.assertTrue(self.core.event_price_range)
        self.assertIsInstance(self.core.event_price_range, list)
        for price in self.core.event_price_range:
            self.assertIsInstance(price, float)
