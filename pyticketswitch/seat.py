from pyticketswitch.mixins import JSONMixin


class SeatBlock(JSONMixin, object):
    """Describes a set of contiguous seats.

    Attributes:
        length (int): the number of seats in the block.
        seats (list): list of :class:`Seats <pyticketswitch.seat.Seat>` in the
            block.

    """

    def __init__(self, length, seats=None):
        self.length = length
        self.seats = seats

    @classmethod
    def from_api_data(cls, block, row_id=None, separator='',
                      restricted_view_seats=None, seats_by_text_message=None):
        """Creates a new Customer object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a seat block.

        Returns:
            :class:`SeatBlock <pyticketswitch.seat.SeatBlock>`: a new
            :class:`SeatBlock <pyticketswitch.seat.SeatBlock>` object
            populated with the data from the api.

        """

        seats = []
        for seat_id in block:

            column = None
            delimiter = separator

            if not delimiter:
                delimiter = row_id

            split_id = seat_id.split(delimiter)
            column = split_id[1]

            restricted = False
            restricted_text = ''

            if seat_id in restricted_view_seats:
                restricted = True

            for seat_text, list_of_seats in seats_by_text_message.items():
                if seat_id in list_of_seats:
                    restricted_text = seat_text
            seat = Seat(
                id_=seat_id, row=row_id, column=column,
                separator=separator, is_restricted=restricted,
                seat_text=restricted_text
            )
            seats.append(seat)

        kwargs = {'seats': seats, 'length': len(seats)}
        return cls(**kwargs)


class Seat(JSONMixin, object):
    """Describes a seat in a venue.

    Attributes:
        id (str): the identifier for the seat.
        column (str): the column of the seat.
        row (str): the row of the seat.
        separator (str): characters that should be used to seperate the column
            and row when presenting seat information.
        is_restricted (bool): indicates that the seat has a restricted view.
        seat_text_code (str): code indicating text that should be displayed
            with the seat when preseting seat information.
        seat_text (str): readable explanation of the seats description

    """

    def __init__(self, id_=None, column=None, row=None, is_restricted=False,
                 seat_text_code=None, seat_text=None, separator=None):
        self.id = id_
        self.column = column
        self.row = row
        self.separator = separator
        self.is_restricted = is_restricted
        self.seat_text = seat_text
        self.seat_text_code = seat_text_code

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Seat object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a seat.

        Returns:
            :class:`Seat <pyticketswitch.seat.Seat>`: a new
            :class:`Seat <pyticketswitch.seat.Seat>` object
            populated with the data from the api.

        """
        kwargs = {
            'id_': data.get('full_id'),
            'column': data.get('col_id'),
            'row': data.get('row_id'),
            'is_restricted': data.get('is_restricted_view', False),
            'seat_text_code': data.get('seat_text_code'),
            'seat_text': data.get('seat_text'),
            'separator': data.get('separator', ''),
        }

        return cls(**kwargs)

    def __repr__(self):
        return u'<Seat {}>'.format(self.id)
