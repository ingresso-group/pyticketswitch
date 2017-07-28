from pyticketswitch.cost_range import CostRange
from pyticketswitch.discount import Discount
from pyticketswitch.seat import Seat, SeatBlock
from pyticketswitch.commission import Commission
from pyticketswitch.mixins import JSONMixin, SeatPricingMixin


class PriceBand(SeatPricingMixin, JSONMixin, object):
    """Describes a set of tickets with the same ticket type and price.

    Attributes:
        code (str): the price band identifier.
        default_discount (:class:`Discount <pyticketswitch.discount.Discount>`):
            this is the discount that will be assumed if no other discount
            is specified at reservation time. It holds the prices for the price
            band.
        allows_leaving_single_seats (str): indicates if this price band will
            allow customers to leave a single seat with no neighbours. Values
            are 'always', 'never', or 'if_necessary'.
        description (str): human readable description of the price band if
            available.
        cost_range (:class:`CostRange <pyticketswitch.cost_range.CostRange>`):
            summary data for the price band including offers.
        no_singles_cost_range (:class:`CostRange <pyticketswitch.cost_range.CostRange>`):
            summary data for the price band including offers.
        example_seats (list): list of :class:`Seats <pyticketswitch.seat.Seat>`
            that can be used as examples of what the user might get when they
            reserved tickets in this price band.
        example_seats_are_real (bool): when :obj:`True` this field indicates
            that the example seats are in fact real seats and will be the ones
            we attempt to reserve at the reservation stage. When :obj:`False`
            these seats merely examples retrieved from cached data, and have
            likely already been purchased.
        seat_blocks (list): list of
            :class:`SeatBlocks <pyticketswitch.seat.SeatBlock>`. When available
            this are the contiguous seats that are available for purchase.
            :class:`SeatBlocks <pyticketswitch.seat.SeatBlock>` contain
            :class:`Seats <pyticketswitch.seat.Seat>`.
        user_commission (:class:`Commission <pyticketswitch.commission.Commission>`):
            the commission payable to the user on the sale of tickets in this
            price band. Only available when requested.
        gross_commission (:class:`Commission <pyticketswitch.commission.Commission>`):
            the gross commission payable. This is not generally available.
        availability (int): the number of tickets/seats available in this price
            band.

    """

    def __init__(self, code, default_discount, description=None, cost_range=None,
                 no_singles_cost_range=None, example_seats=None,
                 example_seats_are_real=True, seat_blocks=None, user_commission=None,
                 discounts=None, allows_leaving_single_seats=None, availability=None,
                 seatprice=None, surcharge=None, non_offer_seatprice=None,
                 non_offer_surcharge=None, percentage_saving=0, absolute_saving=0):

        self.code = code
        self.description = description
        self.cost_range = cost_range
        self.allows_leaving_single_seats = allows_leaving_single_seats
        self.no_singles_cost_range = no_singles_cost_range
        self.default_discount = default_discount
        self.example_seats = example_seats
        self.example_seats_are_real = example_seats_are_real
        self.seat_blocks = seat_blocks
        self.user_commission = user_commission
        self.discounts = discounts
        self.availability = availability
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.non_offer_seatprice = non_offer_seatprice
        self.non_offer_surcharge = non_offer_surcharge
        self.percentage_saving = percentage_saving
        self.absolute_saving = absolute_saving

    @classmethod
    def from_api_data(cls, data):
        """Creates a new **PriceBand** object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a price band.

        Returns:
            :class:`PriceBand <pyticketswitch.order.PriceBand>`: a new
            :class:`PriceBand <pyticketswitch.order.PriceBand>` object
            populated with the data from the api.

        """
        api_cost_range = data.get('cost_range', {})
        api_no_singles_cost_range = api_cost_range.get('no_singles_cost_range', {})
        cost_range = None
        no_singles_cost_range = None

        if api_cost_range:
            api_cost_range['singles'] = True
            cost_range = CostRange.from_api_data(api_cost_range)

        if api_no_singles_cost_range:
            api_no_singles_cost_range['singles'] = False
            no_singles_cost_range = CostRange.from_api_data(
                api_no_singles_cost_range)

        discount = Discount.from_api_data(data)

        kwargs = {
            'code': data.get('price_band_code'),
            'description': data.get('price_band_desc'),
            'availability': data.get('number_available'),
            'cost_range': cost_range,
            'no_singles_cost_range': no_singles_cost_range,
            'default_discount': discount,
            'example_seats_are_real': data.get('example_seats_are_real', True),
            'allows_leaving_single_seats': data.get('allows_leaving_single_seats'),
        }

        example_seats_data = data.get('example_seats')
        if example_seats_data:
            example_seats = [
                Seat.from_api_data(seat)
                for seat in example_seats_data
            ]
            kwargs.update(example_seats=example_seats)

        seat_block_data = data.get('free_seat_blocks')

        if seat_block_data:
            separators_by_row = seat_block_data.get('separators_by_row')
            restricted_view_seats = seat_block_data.get('restricted_view_seats')
            seats_by_text_message = seat_block_data.get('seats_by_text_message')
            blocks_by_row = seat_block_data.get('blocks_by_row')

            seat_blocks = []
            if blocks_by_row:
                for row_id, row in blocks_by_row.items():
                    for block in row:
                        separator = separators_by_row.get(row_id)
                        seat_block = SeatBlock.from_api_data(
                            block=block,
                            row_id=row_id,
                            separator=separator,
                            restricted_view_seats=restricted_view_seats,
                            seats_by_text_message=seats_by_text_message,
                        )
                        seat_blocks.append(seat_block)

            kwargs.update(seat_blocks=seat_blocks)

        user_commission_data = data.get('predicted_user_commission')
        if user_commission_data:
            user_commission = Commission.from_api_data(user_commission_data)
            kwargs.update(user_commission=user_commission)

        discounts_data = data.get('possible_discounts', {}).get('discount')
        if discounts_data:
            discounts = [
                Discount.from_api_data(discount_data)
                for discount_data in discounts_data
            ]
            kwargs.update(discounts=discounts)

        kwargs.update(SeatPricingMixin.kwargs_from_api_data(data))

        return cls(**kwargs)

    def get_seats(self):
        """Get all seats in child seat blocks

        Returns:
            list: list of :class:`Seats <pyticketswitch.seat.Seat>`.

        """
        if not self.seat_blocks:
            return []

        return [
            seat
            for seat_block in self.seat_blocks
            for seat in seat_block.seats or []
        ]

    def __repr__(self):
        if self.description:
            return u'<PriceBand {}:{}>'.format(
                self.code, self.description.encode('ascii', 'ignore'))
        return u'<PriceBand {}>'.format(self.code)
