# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

from pyticketswitch.interface_objects import DespatchMethod, Event, TicketType

from .common import InterfaceObjectTestCase


class PerformanceTests(InterfaceObjectTestCase):

    def setUp(self):

        super(PerformanceTests, self).setUp()

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
            if perf.date.weekday() == 1:
                self.assertIsInstance(perf.required_info, str)


class PerformanceAvailabilityTests(InterfaceObjectTestCase):

    def setUp(self):

        super(PerformanceAvailabilityTests, self).setUp()

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


class DespatchMethodTests(InterfaceObjectTestCase):

    def setUp(self):

        super(DespatchMethodTests, self).setUp()

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

        self.despatch_methods = self.performance.get_despatch_methods()
        self.despatch_method = self.despatch_methods[0]

    def test_despatch_methods(self):
        self.assertTrue(self.despatch_methods)

    def test_despatch_methods_contains_despatch_method(self):
        for dm in self.despatch_methods:
            self.assertIsInstance(dm, DespatchMethod)

    def test_despatch_methods_is_list(self):
        self.assertIsInstance(self.despatch_methods, list)

    def test_despatch_methods_multi_returned(self):
        self.assertGreater(len(self.despatch_methods), 1)

    def test_despatch_returned_event(self):
        self.assertTrue(self.performance.event)

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
