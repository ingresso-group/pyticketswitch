# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

import six

from pyticketswitch.interface_objects import (
    Concession, Core, DespatchMethod, Event, Performance
)

from .common import InterfaceObjectTestCase


class OrderTests(InterfaceObjectTestCase):

    def setUp(self):

        super(OrderTests, self).setUp()

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
                getattr(self.order, prop_name), six.string_types
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
                getattr(self.order, prop_name), six.text_type
            )

    def test_performance(self):
        self.assertIsInstance(self.order.performance, Performance)

    def test_event(self):
        self.assertIsInstance(self.order.event, Event)

    def test_concession(self):
        self.assertIsInstance(self.order.concessions[0], Concession)

    def test_despatch_method(self):
        self.assertIsInstance(self.order.despatch_method, DespatchMethod)
