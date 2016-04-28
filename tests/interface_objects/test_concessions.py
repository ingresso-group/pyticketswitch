# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import six

import six

from pyticketswitch.interface_objects import Event

from .common import InterfaceObjectTestCase


class ConcessionTests(InterfaceObjectTestCase):

    def setUp(self):

        super(ConcessionTests, self).setUp()

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
            self.assertIsInstance(getattr(self.concession, prop_name), six.string_types)

    def test_unicode_properties(self):

        for prop_name in (
            'ticket_price', 'surcharge', 'seatprice'
        ):
            self.assertIsInstance(getattr(self.concession, prop_name), six.text_type)

    def test_float_properties(self):

        for prop_name in (
            'ticket_price_float', 'surcharge_float', 'seatprice_float'
        ):
            self.assertIsInstance(getattr(self.concession, prop_name), float)
