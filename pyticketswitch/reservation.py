from pyticketswitch.order import Order
from pyticketswitch.status import Status


class Reservation(Status):
    """Describes some tickets currently being held for purchase

    Attributes:
        status (str): the currency status of the transaction.
        reserved_at (datetime.datetime): the date and time when the transaction
            was reserved.
        purchased_at (datetime.datetime): the date and time when the transaction
            was purchased.
        trolley (:class:`Trolley <pyticketswitch.trolley.Trolley>`): the
            contents of the transactions trolley.
        external_sale_page (str): the page that was rendered to the customer
            after the transaction was completed. This is only available if
            it was passed into the API at purchase time.
        languages (list): list of IETF language tags relevant to the
            transaction.
        remote_site (str): the remote site the transaction was reserved and
            purchased under.
        reserve_user (:class:`User <pyticketswitch.user.User>`): the user that
            was used to reserve the transaction.
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

    def __init__(self, unreserved_orders=None,
                 input_contained_unavailable_order=False, *args, **kwargs):

        super(Reservation, self).__init__(*args, **kwargs)
        self.unreserved_orders = unreserved_orders
        self.input_contained_unavailable_order = input_contained_unavailable_order

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

        inst = super(Reservation, cls).from_api_data(data)

        unreserved_orders = []
        raw_unreserved_orders = data.get('unreserved_orders')
        if raw_unreserved_orders:
            unreserved_orders = [
                Order.from_api_data(order)
                for order in raw_unreserved_orders
            ]

        inst.unreserved_orders = unreserved_orders
        inst.input_contained_unavailable_order = data.get(
            'input_contained_unavailable_order', False)

        return inst

    def __repr__(self):
        if self.trolley and self.trolley.transaction_uuid:
            return u'<Reservation {}>'.format(self.trolley.transaction_uuid)
        return super(Reservation, self).__repr__()
