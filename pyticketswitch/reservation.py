from pyticketswitch.trolley import Trolley
from pyticketswitch.address import Address
from pyticketswitch.country import Country
from pyticketswitch.order import Order


class Reservation(object):

    def __init__(self, trolley, unreserved_orders=None, prefilled_address=None,
                 needs_payment_card=False, needs_email_address=False,
                 needs_agent_reference=False, minutes_left=None,
                 can_edit_address=False, allowed_countries=None):

        self.trolley = trolley
        self.unreserved_orders = unreserved_orders
        self.prefilled_address = prefilled_address
        self.needs_payment_card = needs_payment_card
        self.needs_email_address = needs_email_address
        self.needs_agent_reference = needs_agent_reference
        self.minutes_left = minutes_left
        self.can_edit_address = can_edit_address
        self.allowed_countries = allowed_countries

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'can_edit_address': data.get('can_edit_address'),
            'needs_agent_reference': data.get('needs_agent_reference'),
            'needs_email_address': data.get('needs_email_address'),
            'needs_payment_card': data.get('needs_payment_card'),
        }

        allowed_countries = data.get('allowed_countries')
        if allowed_countries is not None:
            countries = [
                Country(key, description=description)
                for key, description in allowed_countries.items()
            ]
            countries.sort(key=lambda x: x.code)
            kwargs.update(allowed_countries=countries)

        address = data.get('prefilled_address')
        if address is not None:
            kwargs.update(prefilled_address=Address.from_api_data(address))

        minutes = data.get('minutes_left_on_reserve')
        if minutes is not None:
            kwargs.update(minutes_left=float(minutes))

        trolley = Trolley.from_api_data(data)
        kwargs.update(trolley=trolley)

        raw_unreserved_orders = data.get('unreserve_orders')
        if raw_unreserved_orders:
            unreserved_orders = [
                Order.from_api_data(order)
                for order in raw_unreserved_orders
            ]
            kwargs.update(unreserved_orders=unreserved_orders)

        return cls(**kwargs)
