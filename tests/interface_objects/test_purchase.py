import datetime

from pyticketswitch.interface_objects import (
    Core, Event, Trolley, Address, Customer,
)

from .common import InterfaceObjectCreditUserTestCase


class PurchaseReservationOnCreditTests(InterfaceObjectCreditUserTestCase):

    def setUp(self):

        super(PurchaseReservationOnCreditTests, self).setUp()

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
