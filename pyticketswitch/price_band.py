from pyticketswitch.cost_range import CostRange
from pyticketswitch.discount import Discount
from pyticketswitch.seat import Seat, SeatBlock
from pyticketswitch.mixins import JSONMixin


class PriceBand(JSONMixin, object):

    def __init__(self, code, default_discount, description=None,
                 cost_range=None, no_singles_cost_range=None,
                 example_seats=None, example_seats_are_real=True,
                 seat_blocks=None):

        self.code = code
        self.description = description
        self.cost_range = cost_range
        self.no_singles_cost_range = no_singles_cost_range
        self.default_discount = default_discount
        self.example_seats = example_seats
        self.example_seats_are_real = example_seats_are_real
        self.seat_blocks = seat_blocks

    @classmethod
    def from_api_data(cls, data):
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
            'code': data.get('price_band_code', None),
            'description': data.get('price_band_desc', None),
            'cost_range': cost_range,
            'no_singles_cost_range': no_singles_cost_range,
            'default_discount': discount,
            'example_seats_are_real': data.get('example_seats_are_real', True),
        }

        example_seats_data = data.get('example_seats')
        if example_seats_data:
            example_seats = [
                Seat.from_api_data(seat)
                for seat in example_seats_data.get('id_details', [])
            ]
            kwargs.update(example_seats=example_seats)

        seat_block_data = data.get('free_seat_blocks')
        if seat_block_data:
            seat_blocks = [
                SeatBlock.from_api_data(seat_block)
                for seat_block in seat_block_data.get('seat_block', [])
            ]
            kwargs.update(seat_blocks=seat_blocks)

        return cls(**kwargs)

    def get_seats(self):

        if not self.seat_blocks:
            return []

        return [
            seat
            for seat_block in self.seat_blocks
            for seat in seat_block.seats or []
        ]
