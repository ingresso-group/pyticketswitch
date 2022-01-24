from pyticketswitch.seat import Seat, SeatBlock


class TestSeatBlock:

    def test_from_api_data(self):

        data = ["D1.12"]

        seat_block = SeatBlock.from_api_data(data, separator='.', restricted_view_seats=[], seats_by_text_message={})

        assert seat_block.length == 1
        assert len(seat_block.seats) == 1
        assert seat_block.seats[0].id == 'D1.12'


class TestSeat:

    def test_from_api_data(self):

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
            'seat_google_pay_urls': {
                'gpay_jwt_url': 'https://google-wallet-api-dev.ticketswitch.io/transactions/googlePayJWT',
                'gpay_save_url': 'https://google-wallet-api-dev.ticketswitch.io/transactions/saveToGooglePay'
            }
        }

        seat = Seat.from_api_data(data)

        assert seat.id == 'GQ361'
        assert seat.column == '361'
        assert seat.row == 'GQ'
        assert seat.separator == '-'
        assert seat.is_restricted is True
        assert seat.seat_text_code == 'NEARTOILET'
        assert seat.barcode == '0987654321'
        assert seat.seat_apple_wallet_urls.apple_wallet_gen_url == 'https://apple-wallet-api-dev.ticketswitch.io/generate_passes'
        assert seat.seat_google_pay_urls.gpay_jwt_url == 'https://google-wallet-api-dev.ticketswitch.io/transactions/googlePayJWT'
        assert seat.seat_google_pay_urls.gpay_save_url == 'https://google-wallet-api-dev.ticketswitch.io/transactions/saveToGooglePay'
        
