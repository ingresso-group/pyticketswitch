from pyticketswitch.mixins import JSONMixin


class SeatBlock(JSONMixin, object):

    def __init__(self, length, seats=None):

        self.length = length
        self.seats = seats

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'length': data.get('block_length'),
        }

        seats_data = data.get('id_details')
        if seats_data:
            seats = [
                Seat.from_api_data(seat)
                for seat in seats_data
            ]
            kwargs.update(seats=seats)

        return cls(**kwargs)


class Seat(JSONMixin, object):

    def __init__(self, id_=None, column=None, row=None, is_restricted=False,
                 seat_text_code=None, separator=None):
        self.id = id_
        self.column = column
        self.row = row
        self.separator = separator
        self.is_restricted = is_restricted
        self.seat_text_code = seat_text_code

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'id_': data.get('full_id'),
            'column': data.get('col_id'),
            'row': data.get('row_id'),
            'is_restricted': data.get('is_restricted', False),
            'seat_text_code': data.get('seat_text_code'),
            'separator': data.get('separator', ''),
        }

        return cls(**kwargs)
