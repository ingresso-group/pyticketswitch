import datetime

from pyticketswitch.interface_objects import (
    Core, Event, Trolley, Bundle, Order,
)

from .common import InterfaceObjectTestCase


class TrolleyTests(InterfaceObjectTestCase):

    def setUp(self):

        super(TrolleyTests, self).setUp()

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

        super(BundleTests, self).setUp()

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
