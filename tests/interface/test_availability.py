from pyticketswitch.interface.availability import Availability


class TestAvailability:

    def test_from_api_data(self):

        data ={
            'quantity_options': {
                'valid_quantity_mask': 2046
            },
            'day_mask': 21,
            'available_dates': {
                'last_yyyymmdd': '20161002',
                'first_yyyymmdd': '20160906'
            },
            'avail_currency': {
                'currency_factor': 100,
                'currency_places': 2,
                'currency_post_symbol': '',
                'currency_number': 826,
                'currency_pre_symbol': '\xa3',
                'currency_code': 'gbp'
            },
            'seatprice': 57.5,
            'surcharge': 11.25,
        }
        availability = Availability.from_api_data(data)

        assert availability.valid_quantity_mask == 2046
        assert availability.first_date.day == 6
        assert availability.first_date.month == 9
        assert availability.first_date.year == 2016
        assert availability.last_date.day == 2
        assert availability.last_date.month == 10
        assert availability.last_date.year == 2016
        assert availability.currency.code == 'gbp'
