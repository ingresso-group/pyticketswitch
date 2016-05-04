# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

import six

from pyticketswitch.interface_objects import Core, Event, Reservation, Trolley

from .common import InterfaceObjectTestCase


class ReservationTests(object):

    def test_reservation_is_reservation(self):
        self.assertIsInstance(self.reservation, Reservation)

    def test_string_properties(self):

        for prop_name in (
            'transaction_id',
        ):
            self.assertIsInstance(
                getattr(self.reservation, prop_name), six.string_types
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

        super(MakeReservationTests, self).setUp()

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

        super(CombinedOrderReservationTests, self).setUp()

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
