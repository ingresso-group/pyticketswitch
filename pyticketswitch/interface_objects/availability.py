from operator import attrgetter

from base import InterfaceObject, Seat, SeatBlock
from pyticketswitch.util import (
    format_price_with_symbol,
    to_float_or_none, to_float_summed,
    to_int_or_none, resolve_boolean
)


class TicketType(InterfaceObject):
    """Object that represents both a TSW ticket type and price band.

    The TSW ticket type and price band elements are combined into a single
    object here. This was done to simplify the interface and the ticket type
    and price band elements are closely related. It would be rare to require
    information from a ticket type but not the associated price bands.

    Operations and information associated with either element are available
    through this object. However, unlike the Performance and Event objects,
    this object's attributes will not be populated on-demand, so they may
    only have a value if the object has been retrieved through the Performance
    object.

    Args:
        ticket_type_id (string): Id of the TicketType
        settings (kwargs): See Core constructor.
    """

    def __init__(
        self,
        ticket_type_id,
        core_ticket_type=None,
        core_price_band=None,
        core_currency=None,
        **settings
    ):
        self.ticket_type_id = ticket_type_id
        self._core_ticket_type = core_ticket_type
        self._core_price_band = core_price_band
        self._core_currency = core_currency
        self.blanket_discount_only = None
        self.quantity_options = None
        self._example_seats = None
        self._possible_concessions = False
        self._available_seat_blocks = False

        super(TicketType, self).__init__(**settings)

    def _get_cache_key(self):
        return self.ticket_type_id

    def set_valid_quantities(self, valid_quantities):
        """For internal use, sets the valid ticket quantities."""
        self.quantity_options = [
            (v, v) for v in valid_quantities if int(v) <= int(
                self._core_price_band.number_available
            )
        ]

    def get_concessions(
        self, no_of_tickets, despatch_method=None, trolley=None,
        seat_block=None, seat_block_offset=None,
    ):
        """Retrieves the Concession objects for this TicketType.

        Returns the list of Concession objects for each ticket requested,
        so the reponse will be a list of lists that contain Concession
        objects. Internally the 'discount_options' API method is being
        called.

        Args:
            no_of_tickets (int): Number of tickets.
            despatch_method (DespatchMethod): Optional, the DespatchMethod
                object to be used.
            trolley (Trolley): Optional, an existing Trolley that this
                order will be added to.
            seat_block (SeatBlock): Optional, the SeatBlock to reserve seats
                from. Can only be used if returned in the
                'available_seat_blocks' attribute.
            seat_block_offset (int): Optional, the offset into the seat block,
                with 0 being the start of the block. Can only be specified if
                a seat_block is provided.

        Returns:
            list: A list for each ticket requested of Concession objects (
                so a list of lists of Concession objects).
        """

        crypto_block = self._get_crypto_block_for_object(
            method_name='availability_options',
            interface_object=self
        )

        no_of_tickets = str(int(no_of_tickets))

        if despatch_method is not None:
            despatch_id = despatch_method.despatch_id
        else:
            despatch_id = None

        if trolley is not None:
            trolley_id = trolley.trolley_id
        else:
            trolley_id = None

        if seat_block is not None:
            seat_block_id = seat_block.seat_block_id
        else:
            seat_block_id = None

        if seat_block_offset is not None:
            seat_block_offset = str(int(seat_block_offset))

        resp_dict = self.get_core_api().discount_options(
            crypto_block=crypto_block, band_token=self.ticket_type_id,
            no_of_tickets=no_of_tickets,
            despatch_token=despatch_id,
            trolley_token=trolley_id,
            seat_block_token=seat_block_id,
            seat_block_offset=seat_block_offset
        )

        self._set_crypto_block(
            crypto_block=resp_dict['crypto_block'],
            method_name='discount_options'
        )

        if 'blanket_discount_only' in resp_dict:

            ticket_concessions = []

            for discounts in resp_dict['discounts']:
                concessions = []
                for discount in discounts:
                    con = Concession(
                        concession_id=discount.discount_token,
                        core_discount=discount,
                        core_currency=resp_dict['currency'],
                        **self._internal_settings()
                    )
                    concessions.append(con)

                if concessions:
                    ticket_concessions.append(concessions)

                    self._set_crypto_for_objects(
                        crypto_block=resp_dict['crypto_block'],
                        method_name='discount_options',
                        interface_objects=concessions
                    )

            self.blanket_discount_only = resp_dict.get('blanket_discount_only')
            self.ticket_concessions = ticket_concessions

            return ticket_concessions

        else:
            # Backend doesn't support discount codes
            # crypto_block should be passed to create order
            return None

    @property
    def description(self):
        return self._core_ticket_type.ticket_type_desc

    @property
    def code(self):
        return self._core_ticket_type.ticket_type_code

    @property
    def price_without_surcharge(self):
        """Formatted string value of the price excluding surcharge with
        currency symbol."""

        return format_price_with_symbol(
            self._core_price_band.ticket_price,
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

    @property
    def surcharge(self):
        """Formatted string value of the surcharge with currency symbol."""

        return format_price_with_symbol(
            self._core_price_band.surcharge,
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

    @property
    def price_combined_float(self):
        """Float value of the combined price."""
        if self._core_price_band.combined:
            return to_float_or_none(
                self._core_price_band.combined
            )
        else:
            return to_float_summed(
                self._core_price_band.ticket_price,
                self._core_price_band.surcharge
            )

    @property
    def price_combined(self):
        """Formatted string value of the combined price with currency symbol.
        """
        formatted_price = None

        combined_price = str(self.price_combined_float)

        formatted_price = format_price_with_symbol(
            combined_price,
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

        return formatted_price

    @property
    def number_available(self):
        """Number of tickets available for this TicketType."""
        return self._core_price_band.number_available

    @property
    def int_percentage_saving(self):
        """Integer value of the percentage saving."""
        if self._core_price_band.percentage_saving:
            try:
                percent = int(self._core_price_band.percentage_saving)
            except ValueError:
                percent = None

        return percent

    @property
    def percentage_saving(self):
        """Formatted string value of the percentage saving with a '%' symbol.
        """
        per_sav = None

        if self._core_price_band.percentage_saving:
            if self._core_price_band.percentage_saving == '0':

                per_sav = None
            else:

                per_sav = self._core_price_band.percentage_saving + '%'

        return per_sav

    @property
    def non_offer_combined_float(self):
        """Float value of the original combined price (i.e. if there was no
        offer).
        """
        if self._core_price_band.combined:
            return to_float_or_none(
                self._core_price_band.non_offer_combined
            )
        else:
            return to_float_summed(
                self._core_price_band.non_offer_ticket_price,
                self._core_price_band.non_offer_surcharge
            )

    @property
    def non_offer_combined(self):
        """Formatted string value of the original combined price with
        currency symbol (i.e. if there was no offer).
        """
        formatted_price = None

        combined_price = str(self.non_offer_combined_float)

        formatted_price = format_price_with_symbol(
            combined_price,
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

        return formatted_price

    @property
    def example_seats(self):
        """List of Seat objects representing expected/example seats."""
        if self._example_seats is None:

            self._example_seats = []

            for seat in self._core_price_band.example_seats:
                self._example_seats.append(
                    Seat(core_seat=seat)
                )

            self._example_seats.sort(key=attrgetter(
                'column_sort_id', 'row_sort_id'
            ))

        return self._example_seats

    @property
    def example_seats_are_real(self):
        """Boolean to indicate if the example_seats are actual seat numbers.

        If True, the seats in the example_seats list will be the seats that
        are reserved.
        """
        return resolve_boolean(self._core_price_band.example_seats_are_real)

    @property
    def possible_concessions(self):
        """List of Concession objects that are expected for this TicketType.

        Only available if explicitly requested when getting availability.
        """

        if self._possible_concessions is False:

            if self._core_price_band.possible_discounts:
                self._possible_concessions = []

                for disc in self._core_price_band.possible_discounts:

                    self._possible_concessions.append(
                        Concession(
                            core_discount=disc,
                            core_currency=self._core_currency
                        )
                    )

            else:
                self._possible_concessions = None

        return self._possible_concessions

    @property
    def available_seat_blocks(self):
        """List of SeatBlock objects that can be selected from for this
        TicketType.

        Only available if requested at the availability stage with the
        include_available_seat_blocks flag.
        """
        if self._available_seat_blocks is False:

            if self._core_price_band.free_seat_blocks:
                self._available_seat_blocks = []

                for sb in self._core_price_band.free_seat_blocks:

                    self._available_seat_blocks.append(
                        SeatBlock(core_seat_block=sb)
                    )

            else:
                self._available_seat_blocks = None

        return self._available_seat_blocks


class Concession(InterfaceObject):
    """Object that represents a TSW discount.

    Information relating to a TSW discount is accessible with this object.
    Was renamed to Concession as this was felt to be more appropriate in
    most cases.

    Can be constructed with the Id of the Concession. However, unlike the
    Performance and Event objects, this object's attributes will not be
    populated on-demand, so they may only have a value if the object has
    been retrieved through the TicketType object.

    Args:
        concession_id (string): Id of the Concession
        settings (kwargs): See Core constructor.
    """

    def __init__(
        self,
        concession_id=None,
        core_discount=None,
        core_currency=None,
        **settings
    ):
        self.concession_id = concession_id
        self._core_discount = core_discount
        self._core_currency = core_currency
        self._seats = None

        super(Concession, self).__init__(**settings)

    def _get_cache_key(self):
        return self.concession_id

    @property
    def description(self):
        discount_desc = self._core_discount.discount_desc

        if not discount_desc:
            discount_desc = self.settings['default_concession_descr']

        return discount_desc

    @property
    def ticket_price(self):
        """Formatted string value of the combined price with currency symbol.
        """
        return format_price_with_symbol(
            self._core_discount.combined,
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

    @property
    def ticket_price_float(self):
        """Float value of the combined price."""
        return to_float_or_none(
            self._core_discount.combined
        )

    @property
    def no_of_tickets(self):
        return to_int_or_none(
            self._core_discount.no_of_tickets
        )

    @property
    def surcharge(self):
        """Formatted string value of the surcharge with currency symbol.
        """
        return format_price_with_symbol(
            self._core_discount.surcharge,
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

    @property
    def seatprice(self):
        """Formatted string value of the seat price (i.e. without surcharge)
        with currency symbol.
        """
        return format_price_with_symbol(
            self._core_discount.seatprice,
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

    @property
    def seats(self):
        """List of Seat objects for this Concession.

        This attribute will only have a value if the Concession was
        accessed through a Reservation object.
        """
        if self._seats is None:
            self._seats = []

            for seat in self._core_discount.seats:
                self._seats.append(
                    Seat(core_seat=seat)
                )

        return self._seats

    @property
    def seat_ids(self):
        """List of Seat Ids for this Concession.

        This attribute will only have a value if the Concession was
        accessed through a Reservation object.
        """
        return [s.seat_id for s in self.seats]

    @property
    def has_restricted_view(self):
        """Boolean indcating if any seats have a restricted view.

        This attribute will only have a value if the Concession was
        accessed through a Reservation object.
        """
        restricted = False
        for s in self.seats:
            if s.is_restricted_view:
                restricted = True

        return restricted

    @property
    def unique_seat_text(self):
        """Information about this seat, should be displayed if present.

        This attribute will only have a value if the Concession was
        accessed through a Reservation object.
        """
        seat_text = []
        for s in self.seats:
            if s.seat_text and s.seat_text not in seat_text:
                seat_text.append(s.seat_text)

        return seat_text


class DespatchMethod(InterfaceObject):
    """Object that represents a TSW despatch method.

    Information relating to a TSW despatch method is available with
    this object. Can be constructed with the Id of the DespatchMethod
    (the other constructor arguments are for internal use).

    Args:
        despatch_id (string): Id of the DespatchMethod
        settings (kwargs): See Core constructor.
    """

    def __init__(
        self,
        despatch_id=None,
        core_despatch_method=None,
        core_currency=None,
        **settings
    ):
        self.despatch_id = despatch_id
        self._core_despatch_method = core_despatch_method
        self._core_currency = core_currency

        super(DespatchMethod, self).__init__(**settings)

    @property
    def description(self):
        return self._core_despatch_method.despatch_desc

    @property
    def cost(self):
        """Formatted string value of the cost with currency symbol."""
        return format_price_with_symbol(
            self._core_despatch_method.despatch_cost,
            self._core_currency.currency_pre_symbol,
            self._core_currency.currency_post_symbol
        )

    @property
    def cost_float(self):
        """Float value of the cost."""
        return to_float_or_none(
            self._core_despatch_method.despatch_cost
        )

    @property
    def core_currency(self):
        return self._core_currency
