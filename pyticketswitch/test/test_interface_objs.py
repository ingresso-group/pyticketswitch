import unittest
import datetime
from copy import deepcopy

from pyticketswitch.interface_objects import (
    Core, Event, Concession, DespatchMethod, TicketType, Performance,
    Trolley, Order, Reservation, Review, Seat, Bundle, Address, Customer,
    Commission, Currency
)
from pyticketswitch.api_exceptions import InvalidId
from pyticketswitch import settings_test as settings


class InterfaceObjectTestCase(unittest.TestCase):
    api_settings = {
        'username': settings.TEST_USERNAME,
        'password': settings.TEST_PASSWORD,
        'url': settings.API_URL,
        'ext_start_session_url': settings.EXT_START_SESSION_URL
    }


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
            keyword='test', page_length='5', page_number='1'
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


class InvalidEventTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        self.event = Event(
            event_id='invalid', session=session, **self.api_settings
        )

    def test_get_details(self):
        self.assertRaises(InvalidId, self.event.get_details)

    def test_get_performances(self):
        self.assertRaises(InvalidId, self.event.get_performances)

    def test_get_valid_months(self):
        self.assertRaises(InvalidId, self.event.get_valid_months)

    def test_property(self):
        self.assertFalse(self.event.description)


class ValidEventTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        self.event = Event(
            event_id='6IF', session=session, **self.api_settings)

    def test_string_properties(self):

        for prop_name in (
            'description', 'information', 'venue_desc',
            'venue_info', 'venue_addr', 'supplier_desc',
            'city_code', 'city_desc', 'country_code',
            'country_desc', 'latitude', 'longitude',
            'event_id',
        ):
            self.assertIsInstance(getattr(self.event, prop_name), str)

    def test_categories(self):

        found = False

        for c in self.event.categories:
            if c.code == 'theatre':
                found = True

        self.assertTrue(
            found,
            msg="'Theatre' category not found in event category list"
        )

    def test_float_properties(self):

        for prop_name in (
            'min_seatprice_float',
        ):
            self.assertIsInstance(getattr(self.event, prop_name), float)

    def test_unicode_properties(self):

        for prop_name in (
            'min_seatprice', 'min_combined_price',
        ):
            self.assertIsInstance(getattr(self.event, prop_name), unicode)

    def test_images(self):

        for img in (
            # 'get_large_image',
            'get_medium_image',
            'get_small_image',
            # 'get_seating_plan',
        ):
            self.assertIsNotNone(getattr(self.event, img))

    def test_performances_is_list(self):
        self.assertIsInstance(self.event.get_performances(), list)

    def test_all_performances(self):
        self.assertTrue(self.event.get_performances())

    def test_performances_contains_performance(self):

        performances = self.event.get_performances()

        for perf in performances:
            self.assertIsInstance(perf, Performance)

    def test_no_performances_old_date(self):

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=-1)
        )

        self.assertFalse(
            self.event.get_performances(
                latest_date=latest_date
            )
        )

    def test_performances_one_week(self):

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=6)
        )

        self.assertTrue(
            self.event.get_performances(
                latest_date=latest_date
            )
        )

    def test_performance_calendar(self):
        self.event.get_performances()

        self.assertTrue(self.event.performance_calendar)

    def test_performance_calendar_empty(self):

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=-1)
        )

        self.event.get_performances(latest_date=latest_date)

        self.assertFalse(self.event.performance_calendar)


class EventReviewsTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        self.event = Event(
            event_id='6IF', session=session, **self.api_settings)

    def test_user_review_percent(self):
        self.assertIsInstance(self.event.user_review_percent, str)

    def test_user_reviews(self):
        self.assertTrue(self.event.user_reviews)

    def test_reviews_contains_review(self):
        for r in self.event.user_reviews:
            self.assertIsInstance(r, Review)


class ReviewTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        self.review = event.user_reviews[0]

    def test_review_is_user_review(self):
        self.assertTrue(self.review.is_user_review)

    def test_review_string_properties(self):

        for prop_name in (
            'title', 'author',
            'date_desc', 'time_desc',
        ):
            self.assertIsInstance(getattr(self.review, prop_name), str)

    def test_review_unicode_properties(self):

        for prop_name in (
            'body',
        ):
            self.assertIsInstance(getattr(self.review, prop_name), unicode)

    def test_date_is_datetime_date(self):
        self.assertIsInstance(self.review.date, datetime.date)

    def test_time_is_datetime_time(self):
        self.assertIsInstance(self.review.time, datetime.time)


class AvailDetailTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        self.avail_detail = event.avail_details[0]

    def test_string_properties(self):

        for prop_name in (
            'ticket_type_code', 'ticket_type_desc',
            'price_band_code', 'price_band_desc',
        ):
            prop = getattr(self.avail_detail, prop_name)
            if prop is not None:
                self.assertIsInstance(prop, str)

    def test_unicode_properties(self):

        for prop_name in (
            'seatprice', 'surcharge', 'price_combined', 'non_offer_seatprice',
            'non_offer_surcharge', 'non_offer_combined', 'absolute_saving',
            'percentage_saving',
        ):
            prop = getattr(self.avail_detail, prop_name)
            if prop is not None:
                self.assertIsInstance(prop, unicode)

    def test_weekday_available(self):
        self.assertIsInstance(self.avail_detail.weekdays_available, list)
        self.assertEqual(len(self.avail_detail.weekdays_available), 7)
        for day in self.avail_detail.weekdays_available:
            self.assertIsInstance(day, bool)

    def test_date_properties(self):

        for prop_name in (
            'available_from_date', 'available_until_date',
        ):
            prop = getattr(self.avail_detail, prop_name)
            if prop is not None:
                self.assertIsInstance(prop, datetime.date)

    def test_float_properties(self):

        for prop_name in (
            'price_combined_float', 'non_offer_combined_float',
            'seatprice_float', 'non_offer_seatprice_float',
            'surcharge_float', 'non_offer_surcharge_float',
            'absolute_saving_float',
        ):
            prop = getattr(self.avail_detail, prop_name)
            if prop is not None:
                self.assertIsInstance(prop, float)

    def test_int_properties(self):

        for prop_name in (
            'int_percentage_saving',
        ):
            prop = getattr(self.avail_detail, prop_name)
            if prop is not None:
                self.assertIsInstance(prop, int)

    def test_bool_properties(self):

        for prop_name in (
            'has_no_booking_fee',
        ):
            prop = getattr(self.avail_detail, prop_name)
            self.assertIsInstance(prop, bool)

    def test_comparison(self):

        avail_detail_dup = deepcopy(self.avail_detail)

        self.assertTrue(
            self.avail_detail.is_same_ticket_and_price(avail_detail_dup)
        )
        avail_detail_dup._ticket_type_desc = 'Test'
        self.assertFalse(
            self.avail_detail.is_same_ticket_and_price(avail_detail_dup)
        )


class PerformanceTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        self.performances = event.get_performances(
            latest_date=latest_date
        )

        self.performance = self.performances[0]

    def test_string_properties(self):

        for prop_name in (
            'date_desc', 'time_desc', 'perf_id'
        ):
            self.assertIsInstance(getattr(self.performance, prop_name), str)

    def test_date_is_datetime_date(self):
        self.assertIsInstance(self.performance.date, datetime.date)

    def test_time_is_datetime_time(self):
        self.assertIsInstance(self.performance.time, datetime.time)

    def test_required_info(self):

        for perf in self.performances:
            if perf.date.weekday() == 2:
                self.assertIsInstance(perf.required_info, str)


class PerformanceAvailabilityTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                self.performance = p
                break

        self.performance.get_availability()

    def test_ticket_types(self):
        self.assertTrue(self.performance.ticket_types)

    def test_ticket_types_contains_ticket_type(self):
        for tt in self.performance.ticket_types:
            self.assertIsInstance(tt, TicketType)

    def test_despatch_methods(self):
        self.assertTrue(self.performance.despatch_methods)

    def test_despatch_methods_contains_despatch_method(self):
        for dm in self.performance.despatch_methods:
            self.assertIsInstance(dm, DespatchMethod)

    def test_valid_ticket_quantities(self):
        self.assertTrue(self.performance.valid_ticket_quantities)

    def test_valid_ticket_quantities_contains_int(self):
        for quantity in self.performance.valid_ticket_quantities:
            self.assertIsInstance(quantity, int)

    def test_availability_returned_event(self):
        self.assertTrue(self.performance.event)

    def test_list_properties(self):
        for prop_name in (
            'ticket_types', 'despatch_methods', 'valid_ticket_quantities',
            'ticket_types_by_combined_price', 'ticket_types_by_saving',
            'unique_combined_prices'
        ):
            self.assertIsInstance(getattr(self.performance, prop_name), list)

    def test_sorted_combined_price(self):
        prev_combined_price = 0
        for tt in self.performance.ticket_types_by_combined_price:
            self.assertGreaterEqual(
                tt.price_combined_float, prev_combined_price
            )

    def test_unique_combined_price(self):
        values = []
        for unique_value in self.performance.unique_combined_prices:
            self.assertNotIn(unique_value, values)
            values.append(unique_value)

# Need tests for usage date/departure date somewhere


class PerformanceDespatchTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        self.performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(self.performances):
            if p.date.weekday() != 5:
                self.performance = p
                break

    def test_despatch_methods(self):
        self.assertTrue(self.performance.get_despatch_methods())

    def test_despatch_methods_contains_despatch_method(self):
        for dm in self.performance.get_despatch_methods():
            self.assertIsInstance(dm, DespatchMethod)

    def test_despatch_methods_is_list(self):
        self.assertIsInstance(self.performance.get_despatch_methods(), list)

    def test_despatch_methods_multi_returned(self):
        self.assertGreater(len(self.performance.get_despatch_methods()), 1)

    def test_despatch_returned_event(self):
        self.performance.get_despatch_methods()

        self.assertTrue(self.performance.event)


class TicketTypeTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_types = performance.get_availability(
            include_user_commission=True
        )

        self.ticket_type = ticket_types[0]

    def test_quantity_options(self):
        self.assertIsInstance(self.ticket_type.quantity_options, list)

        for option in self.ticket_type.quantity_options:
            self.assertIsInstance(option, tuple)

            for item in option:
                self.assertIsInstance(item, str)

    def test_string_properties(self):

        for prop_name in (
            'description', 'ticket_type_id',
        ):
            self.assertIsInstance(getattr(self.ticket_type, prop_name), str)

    def test_float_properties(self):

        for prop_name in (
            'non_offer_combined_float', 'price_combined_float',
        ):
            self.assertIsInstance(getattr(self.ticket_type, prop_name), float)

    def test_unicode_properties(self):

        for prop_name in (
            'price_without_surcharge', 'surcharge', 'price_combined',
            'non_offer_combined'
        ):
            self.assertIsInstance(
                getattr(self.ticket_type, prop_name), unicode
            )

    def test_int_properties(self):

        for prop_name in (
            'int_percentage_saving', 'number_available',
        ):
            self.assertIsInstance(getattr(self.ticket_type, prop_name), int)

    def test_example_seats(self):
        self.assertIsInstance(self.ticket_type.example_seats, list)

        for ex in self.ticket_type.example_seats:
            self.assertIsInstance(ex, Seat)

    # def test_user_commission(self):
    #     user_commission = self.ticket_type.user_commission
    #     self.assertIsInstance(user_commission, Commission)
    #     self.assertIsInstance(user_commission.amount_excluding_vat, float)
    #     self.assertIsInstance(user_commission.amount_including_vat, float)
    #     self.assertIsInstance(user_commission.commission_currency, Currency)


class TicketTypeConcessionTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_types = performance.get_availability()

        self.ticket_type = ticket_types[0]

        self.ticket_type.get_concessions(
            no_of_tickets=1,
            despatch_method=performance.despatch_methods[0]
        )

    def test_blanket_discount_only(self):
        self.assertIsInstance(self.ticket_type.blanket_discount_only, str)

    def test_ticket_concessions(self):
        self.assertIsInstance(self.ticket_type.ticket_concessions, list)

        for concessions in self.ticket_type.ticket_concessions:
            self.assertIsInstance(concessions, list)

            for concession in concessions:
                self.assertIsInstance(concession, Concession)


class ConcessionTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_types = performance.get_availability()

        ticket_type = ticket_types[0]

        ticket_concessions = ticket_type.get_concessions(
            no_of_tickets=1,
            despatch_method=performance.despatch_methods[0]
        )

        concessions = ticket_concessions[0]

        self.concession = concessions[0]

    def test_string_properties(self):

        for prop_name in (
            'concession_id', 'description',
        ):
            self.assertIsInstance(getattr(self.concession, prop_name), str)

    def test_unicode_properties(self):

        for prop_name in (
            'ticket_price', 'surcharge', 'seatprice'
        ):
            self.assertIsInstance(getattr(self.concession, prop_name), unicode)

    # def test_seat_codes(self):

    #     self.assertIsInstance(self.concession.seat_codes, list)

    #     for seat_id in self.concession.seat_codes:
    #         self.assertIsInstance(seat_id, str)


class DespatchMethodTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        despatch_methods = performance.get_despatch_methods()

        self.despatch_method = despatch_methods[0]

    def test_string_properties(self):

        for prop_name in (
            'description', 'despatch_id',
        ):
            self.assertIsInstance(
                getattr(self.despatch_method, prop_name), str
            )

    def test_unicode_properties(self):

        for prop_name in (
            'cost',
        ):
            self.assertIsInstance(
                getattr(self.despatch_method, prop_name), unicode
            )


class OrderTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_types = performance.get_availability()

        ticket_type = ticket_types[0]

        despatch_method = performance.despatch_methods[0]

        ticket_concessions = ticket_type.get_concessions(
            no_of_tickets=1,
            despatch_method=despatch_method
        )

        concessions = ticket_concessions[0]

        concession = concessions[0]

        concession_list = [concession]

        core = Core(session=session, **self.api_settings)

        self.order = core.create_order(
            concessions=concession_list,
            despatch_method=despatch_method,
        )

    def test_string_properties(self):

        for prop_name in (
            'event_desc', 'venue_desc',
            'ticket_type_desc', 'order_id',
        ):
            self.assertIsInstance(
                getattr(self.order, prop_name), str
            )

    def test_int_properties(self):

        for prop_name in (
            'item_number',
        ):
            self.assertIsInstance(
                getattr(self.order, prop_name), int
            )

    def test_unicode_properties(self):

        for prop_name in (
            'total_combined',
        ):
            self.assertIsInstance(
                getattr(self.order, prop_name), unicode
            )

    def test_performance(self):
        self.assertIsInstance(self.order.performance, Performance)

    def test_event(self):
        self.assertIsInstance(self.order.event, Event)

    def test_concession(self):
        self.assertIsInstance(self.order.concessions[0], Concession)

    def test_despatch_method(self):
        self.assertIsInstance(self.order.despatch_method, DespatchMethod)


class TrolleyTests(InterfaceObjectTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_types = performance.get_availability()

        ticket_type = ticket_types[0]

        despatch_method = performance.despatch_methods[0]

        ticket_concessions = ticket_type.get_concessions(
            no_of_tickets=1,
            despatch_method=despatch_method
        )

        concessions = ticket_concessions[0]

        concession = concessions[0]

        concession_list = [concession]

        core = Core(session=session, **self.api_settings)

        order = core.create_order(
            concessions=concession_list,
            despatch_method=despatch_method,
        )

        self.trolley = Trolley(session=session, **self.api_settings)

        self.trolley.add_order(order)

    def test_string_properties(self):

        for prop_name in (
            'trolley_id',
        ):
            self.assertIsInstance(
                getattr(self.trolley, prop_name), str
            )

    def test_int_properties(self):

        for prop_name in (
            'order_count',
        ):
            self.assertIsInstance(
                getattr(self.trolley, prop_name), int
            )

    def test_update(self):
        session = {}
        new_trolley = Trolley(
            trolley_id=self.trolley.trolley_id,
            session=session,
            **self.api_settings
        )

        new_trolley.update()

        self.assertTrue(new_trolley.order_count)

    def test_bundles(self):

        self.assertIsInstance(self.trolley.bundles, list)

        for o in self.trolley.bundles:
            self.assertIsInstance(o, Bundle)

    def test_orders(self):

        self.assertIsInstance(self.trolley.orders, list)

        for o in self.trolley.orders:
            self.assertIsInstance(o, Order)


class BundleTests(InterfaceObjectTestCase):

    def get_order(self, event_id):
        session = {}
        event = Event(event_id=event_id, session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_type = performance.get_availability()[0]

        despatch_method = performance.despatch_methods[0]

        concession = ticket_type.get_concessions(
            no_of_tickets=1,
            despatch_method=despatch_method
        )[0][0]

        concession_list = [concession]

        core = Core(session=session, **self.api_settings)

        return core.create_order(
            concessions=concession_list,
            despatch_method=despatch_method,
        )

    def setUp(self):

        order1 = self.get_order('6IF')
        order2 = self.get_order('6L9')

        session = {}
        self.trolley = Trolley(session=session, **self.api_settings)

        self.trolley.add_order(order1)
        self.trolley.add_order(order2)

    def test_string_properties(self):

        for prop_name in (
            'source_description', 'source_code',
        ):
            self.assertIsInstance(
                getattr(self.trolley.bundles[0], prop_name), str
            )

    def test_unicode_properties(self):

        for prop_name in (
            'total_seatprice', 'total_surcharge',
            'total_despatch', 'total_cost',
        ):
            self.assertIsInstance(
                getattr(self.trolley.bundles[0], prop_name), unicode
            )

    def test_int_properties(self):

        for prop_name in (
            'order_count',
        ):
            self.assertIsInstance(
                getattr(self.trolley.bundles[0], prop_name), int
            )

    def test_float_properties(self):

        for prop_name in (
            'total_cost_float',
        ):
            self.assertIsInstance(
                getattr(self.trolley.bundles[0], prop_name), float
            )

    def test_bundles_count(self):

        self.assertEqual(
            len(self.trolley.bundles),
            2,
        )


class ReservationTests(object):

    def test_reservation_is_reservation(self):
        self.assertIsInstance(self.reservation, Reservation)

    def test_string_properties(self):

        for prop_name in (
            'transaction_id',
        ):
            self.assertIsInstance(
                getattr(self.reservation, prop_name), str
            )

    def test_bool_properties(self):

        for prop_name in (
            'need_payment_card',
            'needs_email_address', 'supports_billing_address',
            'needs_agent_reference',

        ):
            self.assertIsInstance(
                getattr(self.reservation, prop_name), bool
            )

    def test_get_details(self):
        session = {}
        new_reservation = Reservation(
            transaction_id=self.reservation.transaction_id,
            session=session,
            **self.api_settings
        )

        trolley = new_reservation.get_details()

        self.assertIsInstance(trolley, Trolley)


class MakeReservationTests(InterfaceObjectTestCase, ReservationTests):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_types = performance.get_availability()

        ticket_type = ticket_types[0]

        despatch_method = performance.despatch_methods[0]

        ticket_concessions = ticket_type.get_concessions(
            no_of_tickets=1,
            despatch_method=despatch_method
        )

        concessions = ticket_concessions[0]

        concession = concessions[0]

        concession_list = [concession]

        core = Core(session=session, **self.api_settings)

        order = core.create_order(
            concessions=concession_list,
            despatch_method=despatch_method,
        )

        self.trolley = Trolley(session=session, **self.api_settings)

        self.trolley.add_order(order)

        self.reservation = self.trolley.get_reservation()


class CombinedOrderReservationTests(InterfaceObjectTestCase, ReservationTests):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_types = performance.get_availability()

        ticket_type = ticket_types[0]

        despatch_method = performance.despatch_methods[0]

        ticket_concessions = ticket_type.get_concessions(
            no_of_tickets=1,
            despatch_method=despatch_method
        )

        concessions = ticket_concessions[0]

        concession = concessions[0]

        concession_list = [concession]

        core = Core(session=session, **self.api_settings)

        self.reservation = core.create_reservation(
            concessions=concession_list,
            despatch_method=despatch_method,
        )


class InterfaceObjectCreditUserTestCase(unittest.TestCase):
    api_settings = {
        'username': settings.TEST_CREDIT_USERNAME,
        'password': settings.TEST_CREDIT_PASSWORD,
        'url': settings.API_URL,
        'ext_start_session_url': settings.EXT_START_SESSION_URL
    }


class PurchaseReservationOnCreditTests(InterfaceObjectCreditUserTestCase):

    def setUp(self):
        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        latest_date = (
            datetime.date.today() +
            datetime.timedelta(days=7)
        )

        performances = event.get_performances(
            latest_date=latest_date
        )

        for p in reversed(performances):
            if p.date.weekday() != 5:
                performance = p
                break

        ticket_types = performance.get_availability()

        ticket_type = ticket_types[0]

        despatch_method = performance.despatch_methods[0]

        ticket_concessions = ticket_type.get_concessions(
            no_of_tickets=1,
            despatch_method=despatch_method
        )

        concessions = ticket_concessions[0]

        concession = concessions[0]

        concession_list = [concession]

        core = Core(session=session, **self.api_settings)

        order = core.create_order(
            concessions=concession_list,
            despatch_method=despatch_method,
        )

        self.trolley = Trolley(session=session, **self.api_settings)

        self.trolley.add_order(order)

        self.reservation = self.trolley.get_reservation()

        customer_address = Address(
            address_line_one='1 Test Lane',
            address_line_two=None,
            town='Test Town',
            county='County',
            postcode='AB12 3CD',
            country_code='GB'
        )

        customer = Customer(
            title='Mr',
            first_name='Test',
            last_name='User',
            email_address='test@test.com',
            home_phone='01234567890',
            work_phone='01234567890',
            address=customer_address,
            user_can_use_data=True,
            supplier_can_use_data=False,
            world_can_use_data=False
        )

        self.purchase_response = self.reservation.purchase_reservation(
            customer=customer,
        )

    def test_purchase_succeeded(self):
        self.assertTrue(self.reservation.is_purchased)
