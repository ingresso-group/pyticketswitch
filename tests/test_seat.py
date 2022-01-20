from pyticketswitch.seat import Seat, SeatBlock


class TestSeatBlock:

    def from_api_data(self):

        data = {
            'block_length': 10,
            'id_details': [
                {'full_id': 'D1'},
                {'full_id': 'B2'},
            ]
        }

        seat_block = SeatBlock.from_api_data(data)

        assert seat_block.length == 10
        assert len(seat_block.seats) == 2
        assert seat_block.seats[0].id == 'D1'
        assert seat_block.seats[1].id == 'B2'


class TestSeat:

    def from_api_data(self):

        data = {
            'col_id': '361',
            'full_id': 'GQ361',
            'is_restricted_view': True,
            'row_id': 'GQ',
            'seat_text_code': 'NEARTOILET',
            'separator': '-',
            'barcode': '0987654321',
            'seat_apple_wallet_urls': {
                'apple_wallet_gen_url': 'https://apple-wallet-api-dev.ticketswitch.io/generate_passes'
            },
            'seat_google_wallet_urls': {
                'gpay_jwt_url': 'https://google-wallet-api-dev.ticketswitch.io/transactions/googlePayJWT',
                'gpay_save_url': 'https://google-wallet-api-dev.ticketswitch.io/transactions/saveToGooglePay'
            }
        }

        seat = Seat.from_api_data(data)

        assert seat.id == 'GQ-361'
        assert seat.column == '361'
        assert seat.row == 'GQ'
        assert seat.separator == '-'
        assert seat.is_restricted is True
        assert seat.text_code == 'NEARTOILET'
        assert seat.barcode == '0987654321'
