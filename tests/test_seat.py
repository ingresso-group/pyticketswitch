from pyticketswitch.seat import Seat


class TestSeat:

    def from_api_data(self):

        data = {
            'col_id': '361',
            'full_id': 'GQ361',
            'is_restricted_view': True,
            'row_id': 'GQ',
            'seat_text_code': 'NEARTOILET',
            'separator': '-'
        }

        seat = Seat.from_api_data(data)

        assert seat.id == 'GQ-361'
        assert seat.column == '361'
        assert seat.row == 'GQ'
        assert seat.separator == '-'
        assert seat.is_restricted is True
        assert seat.text_code == 'NEARTOILET'
