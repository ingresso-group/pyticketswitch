from pyticketswitch.trolley import Trolley
from pyticketswitch.address import Address
from pyticketswitch.country import Country
from pyticketswitch.order import Order
from pyticketswitch.mixins import JSONMixin


class Reservation(JSONMixin, object):
    """Describes some tickets currently being held for purchase

    Attributes:
        trolley (:class:`Trolley <pyticketswitch.trolley.Trolley`): the contents
            of the reservation trolley.
        unreserved_orders (list): list of :class:`Orders
            <pyticketswitch.order.Order`>` that failed to reserve.
        prefilled_address (:class:`Address <pyticketswitch.address.Address>`):
            some address information that should be used to prefill any
            customer address fields. This is primarily used on B2B accounts.
        needs_payment_card (bool): When :obj:`True` indicates that this
            reservation will require :class:`CardDetails
            <pyticketswitch.payment_methods.CardDetails>` as the payment method
            at purchase time.
        needs_email_address (bool): When :obj:`True` indicates that the
            customer needs to provide a valid email address at purchase time.
        needs_agent_reference (bool): When :obj:`True` indicates that an agent
            reference should be provided at purchase time.
        can_edit_address (bool): When :obj:`False` indicates that the prefilled
            customer address provided by **prefilled_address** should not be
            edited.
        allowed_countries (list): list of :class:`Countries
            <pyticketswitch.country.Country>` that are acceptable for the
            customers postal address to be from.
        minutes_left (float): the number of minutes left before a reservation
            expires.

    """

    def __init__(self, trolley=None, unreserved_orders=None, prefilled_address=None,
                 needs_payment_card=False, needs_email_address=False,
                 needs_agent_reference=False, can_edit_address=False,
                 allowed_countries=None, minutes_left=None):

        self.trolley = trolley
        self.unreserved_orders = unreserved_orders
        self.prefilled_address = prefilled_address
        self.needs_payment_card = needs_payment_card
        self.needs_email_address = needs_email_address
        self.needs_agent_reference = needs_agent_reference
        self.can_edit_address = can_edit_address
        self.allowed_countries = allowed_countries
        self.minutes_left = minutes_left

    @classmethod
    def from_api_data(cls, data):
        """Creates a new **Reservation** object from ticketswitch API data.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a reservation.

        Returns:
            :class:`Reservation <pyticketswitch.order.Reservation>`: a new
            :class:`Reservation <pyticketswitch.order.Reservation>` object
            populated with the data from the api.

        """

        kwargs = {
            'can_edit_address': data.get('can_edit_address'),
            'needs_agent_reference': data.get('needs_agent_reference'),
            'needs_email_address': data.get('needs_email_address'),
            'needs_payment_card': data.get('needs_payment_card'),
            'minutes_left': data.get('minutes_left_on_reserve'),
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

    def __repr__(self):
        if self.trolley and self.trolley.transaction_uuid:
            return u'<Reservation {}>'.format(self.trolley.transaction_uuid)
        return super(Reservation, self).__repr__()
