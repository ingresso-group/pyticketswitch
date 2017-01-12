class Seat(object):

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
            'separator': data.get('separator')
        }

        return cls(**kwargs)
