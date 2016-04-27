# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

import six

from pyticketswitch.interface_objects import Concession, Event, Seat

from .common import InterfaceObjectTestCase


class TicketTypeTests(InterfaceObjectTestCase):

    def setUp(self):

        super(TicketTypeTests, self).setUp()

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
            'surcharge_float', 'price_without_surcharge_float',
            'non_offer_surcharge_float', 'non_offer_seatprice_float',
        ):
            self.assertIsInstance(getattr(self.ticket_type, prop_name), float)

    def test_unicode_properties(self):

        for prop_name in (
            'price_without_surcharge', 'surcharge', 'price_combined',
            'non_offer_combined', 'non_offer_surcharge', 'non_offer_seatprice',
        ):
            self.assertIsInstance(
                getattr(self.ticket_type, prop_name), six.text_type
            )

    def test_int_properties(self):

        for prop_name in (
            'int_percentage_saving', 'number_available',
        ):
            self.assertIsInstance(getattr(self.ticket_type, prop_name), int)

    def test_bool_properties(self):

        for prop_name in (
            'is_offer',
        ):
            self.assertIsInstance(getattr(self.ticket_type, prop_name), bool)

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

        super(TicketTypeConcessionTests, self).setUp()

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
