# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import six
from copy import deepcopy

import six

from pyticketswitch.api_exceptions import InvalidId
from pyticketswitch.interface_objects import Event, Performance, Review

from .common import InterfaceObjectTestCase


class InvalidEventTests(InterfaceObjectTestCase):

    def setUp(self):

        super(InvalidEventTests, self).setUp()

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

        super(ValidEventTests, self).setUp()

        session = {}
        self.event = Event(
            event_id='6IF', session=session, **self.api_settings)

    def test_string_properties(self):

        for prop_name in (
            'description', 'information', 'venue_desc',
            'venue_info', 'venue_addr', 'supplier_desc',
            'city_code', 'city_desc', 'country_code',
            'country_desc', 'latitude', 'longitude',
            'event_id', 'event_type'
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
            self.assertIsInstance(getattr(self.event, prop_name), six.text_type)

    def test_boolean_properties(self):

        for prop_name in (
            'has_no_perfs', 'is_meta_event'
        ):
            self.assertIsInstance(getattr(self.event, prop_name), bool)

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

        super(EventReviewsTests, self).setUp()

        session = {}
        self.event = Event(
            event_id='6IF', session=session, **self.api_settings)

    def test_critic_review_percent(self):
        self.assertIsInstance(self.event.critic_review_percent, str)

    def test_critic_reviews(self):
        self.assertTrue(self.event.critic_reviews)

    def test_reviews_contains_review(self):
        for r in self.event.critic_reviews:
            self.assertIsInstance(r, Review)


class ReviewTests(InterfaceObjectTestCase):

    def setUp(self):

        super(ReviewTests, self).setUp()

        session = {}
        event = Event(event_id='6IF', session=session, **self.api_settings)

        self.review = event.critic_reviews[0]

    def test_review_is_user_review(self):
        self.assertFalse(self.review.is_user_review)

    def test_review_string_properties(self):

        for prop_name in (
            'title', 'author', 'date_desc', 'time_desc', 'body',
        ):
            self.assertIsInstance(getattr(self.review, prop_name), str)

    def test_date_is_datetime_date(self):
        self.assertIsInstance(self.review.date, datetime.date)

    def test_time_is_datetime_time(self):
        self.assertIsInstance(self.review.time, datetime.time)


class AvailDetailTests(InterfaceObjectTestCase):

    def setUp(self):

        super(AvailDetailTests, self).setUp()

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
                self.assertIsInstance(prop, six.text_type)

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
